from typing import List
from typing import Dict
import copy
import traceback

from django.db.models import Q
from django.db import transaction
from loguru import logger

from dj_jenkins.models import PipelineModel


class PipelineUtil:

    @staticmethod
    def get_pipeline_objs(pipeline_fullnames: List[str] = None):
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if pipeline_fullnames:
            q.children.append(("pipeline_name__in", pipeline_fullnames))
        qs = PipelineModel.objects.filter(q)

        return qs

    @staticmethod
    def get_pipeline_obj(pipeline_fullname: str = ""):
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if pipeline_fullname:
            q.children.append(("fullname", pipeline_fullname))
        qs = PipelineModel.objects.filter(q).first()

        return qs

    @staticmethod
    def is_pipeline_exists(pipeline_fullname):
        ret = (PipelineModel.objects.
               filter(is_deleted=False, fullname=pipeline_fullname).
               exists())

        return ret

    @staticmethod
    def sync(pipeline_fullnames: List[str] = None, update: bool = True) -> Dict:
        from dj_jenkins.utils import JPipelineUtil
        from dj_jenkins.utils import TimeUtil
        pipeline_objs = JPipelineUtil.get_j_pipeline_objs(fullnames=pipeline_fullnames)
        db_pipeline_objs = PipelineUtil.get_pipeline_objs()
        db_job_dict = {db_job_obj.fullname: db_job_obj for db_job_obj in db_pipeline_objs}
        db_job_dict_dup = copy.deepcopy(db_job_dict)
        added = 0
        updated = 0
        try:
            new_pipeline_objs = []
            with transaction.atomic():
                for job_obj in pipeline_objs:
                    logger.info(f"{TimeUtil.get_log_timestamp()} syncing job: {job_obj.fullname}")
                    model_pipeline_obj = job_obj.to_model()
                    if job_obj.fullname not in db_job_dict:
                        new_pipeline_objs.append(model_pipeline_obj)
                        added += 1
                    else:
                        if update:
                            model_pipeline_obj.save()
                            updated += 1
                            db_job_dict_dup.pop(job_obj.fullname)
            if new_pipeline_objs:
                PipelineModel.objects.bulk_create(new_pipeline_objs)
            return {
                "result": True,
                "detail": {
                    "added": added,
                    "updated": updated
                }
            }
        except:
            traceback.print_exc()
        return {
            "result": False,
            "detail": {
                "added": added,
                "updated": updated
            }
        }

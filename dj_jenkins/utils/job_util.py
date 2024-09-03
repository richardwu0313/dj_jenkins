from typing import Dict
from typing import List
import copy
import traceback

from django.db import transaction
from loguru import logger

from dj_jenkins.models import JobModel


class JobUtil:

    @staticmethod
    def get_jobs():
        qs = (JobModel.objects.
              filter(is_deleted=False).
              values("name", "url", "description"))
        return qs

    @staticmethod
    def get_job_objs():
        qs = (JobModel.objects.
              filter(is_deleted=False))
        return qs

    @staticmethod
    def get_job_obj(job_fullname):
        job_obj = (JobModel.objects.
                   filter(is_deleted=False,
                          fullname=job_fullname).
                   first())

        return job_obj

    @staticmethod
    def is_job_exists(job_fullname):
        ret = (JobModel.objects.
               filter(is_deleted=False,
                      fullname=job_fullname).
               exists())

        return ret

    @staticmethod
    def sync(job_fullnames: List[str] = None, update: bool = True) -> Dict:
        from dj_jenkins.utils.j_job_util import JJobUtil
        from dj_jenkins.utils.time_util import TimeUtil
        job_objs = JJobUtil.get_j_job_objs(fullnames=job_fullnames)
        db_job_objs = JobUtil.get_job_objs()
        db_job_dict = {db_job_obj.fullname: db_job_obj for db_job_obj in db_job_objs}
        db_job_dict_dup = copy.deepcopy(db_job_dict)
        added = 0
        updated = 0
        try:
            new_job_objs = []
            with transaction.atomic():
                for job_obj in job_objs:
                    logger.info(f"{TimeUtil.get_log_timestamp()} syncing job: {job_obj.fullname}")
                    model_job_obj = job_obj.to_model()
                    if job_obj.fullname not in db_job_dict:
                        new_job_objs.append(model_job_obj)
                        added += 1
                    else:
                        if update:
                            model_job_obj.save()
                            updated += 1
                            db_job_dict_dup.pop(job_obj.fullname)
            if new_job_objs:
                JobModel.objects.bulk_create(new_job_objs)
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



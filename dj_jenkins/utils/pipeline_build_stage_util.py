from typing import Dict
from typing import List
import copy
import traceback

from loguru import logger
from django.db.models import Q
from django.db import transaction

from dj_jenkins.models.pipeline_build_stage import PipelineBuildStageModel
from dj_jenkins.utils.j_pipeline_build_util import JPipelineBuildUtil
from dj_jenkins.utils.time_util import TimeUtil


class PipelineBuildStageUtil:

    @staticmethod
    def get_stages(pipeline_fullname: str = "", build_number: int = 0):
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if pipeline_fullname:
            q.children.append(("pipeline_build__pipeline__fullname", pipeline_fullname))
        if build_number:
            q.children.append(("pipeline_build__number", build_number))
        qs = PipelineBuildStageModel.objects.filter(q)

        return qs

    @staticmethod
    def sync_pipeline_build(pipeline_fullname: str = "", build_number: int = 0, update: bool = True) -> Dict:
        from dj_jenkins.utils.j_pipeline_build_stage_util import JPipelineBuildStageUtil
        stage_objs = JPipelineBuildStageUtil.get_stage_objs(
           pipeline_fullname=pipeline_fullname,
           build_number=build_number)
        db_stage_objs = PipelineBuildStageModel.objects.filter(
           pipeline_build__pipeline__fullname=pipeline_fullname,
           pipeline_build__number=build_number
        )
        db_build_dict = {stage_obj.name: stage_obj for stage_obj in db_stage_objs}
        db_build_dict_dup = copy.deepcopy(db_build_dict)
        added = 0
        updated = 0
        try:
            new_stage_objs = []
            with transaction.atomic():
                for stage_obj in stage_objs:
                    model_stage_obj = stage_obj.to_model()
                    if stage_obj.name not in db_build_dict:
                        new_stage_objs.append(model_stage_obj)
                        added += 1
                    else:
                        if update:
                            model_stage_obj.save()
                            updated += 1
                            db_build_dict_dup.pop(stage_obj.name)
                if new_stage_objs:
                    PipelineBuildStageModel.objects.bulk_create(new_stage_objs)
                return {
                    "result": True,
                    "detail": {
                        "added": added,
                        "updated": updated,
                    }
               }
        except:
            traceback.print_exc()
        return {
            "result": True,
            "detail": {
                "added": added,
                "updated": updated,
            }
        }

    @staticmethod
    def sync(pipeline_fullnames: List = None, update: bool = True, force: bool = False) -> Dict:
        from dj_jenkins.utils.j_pipeline_util import JPipelineUtil
        from dj_jenkins.utils.pipeline_build_util import PipelineBuildUtil
        result = True
        added = 0
        updated = 0
        if not pipeline_fullnames:
            pipeline_fullnames = JPipelineUtil.get_j_pipeline_fullnames()
        pipeline_number_pairs = []
        for pipeline_fullname in pipeline_fullnames:
            if not force:
                latest_build_obj = (PipelineBuildUtil.get_pipeline_build_objs(pipeline_fullname=pipeline_fullname).
                                    order_by("-id").first())
                if latest_build_obj:
                    latest_build_number = latest_build_obj.number
                else:
                    latest_build_number = -1
            else:
                latest_build_number = -1
            numbers = JPipelineBuildUtil.get_build_numbers(
                pipeline_fullname=pipeline_fullname,
                next_sync_build_number=latest_build_number
            )
            pipeline_number_pairs.extend([(pipeline_fullname, number) for number in numbers])
        for p_n in pipeline_number_pairs:
            logger.info(f"{TimeUtil.get_log_timestamp()} syncing stages of pipeline: {p_n[0]}, build: {p_n[1]}")
            p_n_result = PipelineBuildStageUtil.sync_pipeline_build(
                pipeline_fullname=p_n[0],
                build_number=p_n[1],
                update=update
            )
            result &= p_n_result["result"]
            added += p_n_result["detail"]["added"]
            updated += p_n_result["detail"]["updated"]
        return {
            "result": result,
            "detail": {
                "added": added,
                "updated": updated,
            }
        }

    @staticmethod
    def get_pipeline_build_stage_results(pipeline_fullname: str, year: int, month: int, day: int) -> Dict:
        qs = (PipelineBuildStageModel.objects.
              filter(pipeline_build__pipeline__fullname=pipeline_fullname,
                     pipeline_build__timestamp__year=year,
                     pipeline_build__timestamp__month=month,
                     pipeline_build__timestamp__day=day).
              order_by("pipeline_build_id", "start_time"))
        result_dict = {}
        for item in qs:
            key = pipeline_fullname + " < #" + str(item.pipeline_build_id)
            if key not in result_dict:
                result_dict[key] = {}
            result_dict[key][item.name] = item.result
        return result_dict

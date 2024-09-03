from typing import Dict
from typing import List
import traceback
import copy

from django.db.models import Q
from django.db import transaction
from loguru import logger

from dj_jenkins.models import PipelineBuildModel


class PipelineBuildUtil:

    @staticmethod
    def get_pipeline_build_objs(pipeline_fullname: str = ""):
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if pipeline_fullname:
            q.children.append(("pipeline__fullname", pipeline_fullname))
        pipeline_build_list = (PipelineBuildModel.objects.
                               filter(q))
        return pipeline_build_list

    @staticmethod
    def get_pipeline_build(pipeline_fullname, build_number):
        ret = PipelineBuildModel.objects.filter(
            is_deleted=False,
            pipeline__fullname=pipeline_fullname,
            number=build_number).exists()

        return ret

    @staticmethod
    def get_pipeline_build_number(pipeline_fullname: str,
                                  src_branch: str,
                                  dst_branch: str,
                                  repository_name: str,
                                  team_name: str):
        pl_bld_obj = PipelineBuildModel.objects.filter(
            is_deleted=False,
            pipeline__fullname=pipeline_fullname,
            src_branch=src_branch,
            dst_branch=dst_branch,
            repository=repository_name,
            team=team_name).first()
        if pl_bld_obj:
            return pl_bld_obj.number

        return None

    @staticmethod
    def is_pipeline_build_exists(pipeline_fullname, build_number):
        ret = PipelineBuildModel.objects. \
            filter(is_deleted=False,
                   pipeline__name=pipeline_fullname,
                   number=build_number).exists()

        return ret

    @staticmethod
    def sync_pipeline_builds(pipeline_fullname: str, update: bool = True, force: bool = False) -> Dict:
        from dj_jenkins.utils.j_pipeline_build_util import JPipelineBuildUtil
        if not force:
            latest_pipeline_build_obj = PipelineBuildUtil.get_pipeline_build_objs(pipeline_fullname=pipeline_fullname).order_by("-id").first()
            if latest_pipeline_build_obj:
                latest_pipeline_build_number = latest_pipeline_build_obj.number
            else:
                latest_pipeline_build_number = -1
        else:
            latest_pipeline_build_number = -1
        build_objs = JPipelineBuildUtil.get_build_objs(
            pipeline_fullname=pipeline_fullname,
            next_build_number=latest_pipeline_build_number,
        )
        db_build_objs = PipelineBuildUtil.get_pipeline_build_objs(pipeline_fullname)
        db_build_dict = {build_obj.number: build_obj for build_obj in db_build_objs}
        db_build_dict_dup = copy.deepcopy(db_build_dict)
        added = 0
        updated = 0
        try:
            new_build_objs = []
            with transaction.atomic():
                for build_obj in build_objs:
                    model_build_obj = build_obj.to_model()
                    if build_obj.number not in db_build_dict:
                        new_build_objs.append(model_build_obj)
                        added += 1
                    else:
                        if update:
                            model_build_obj.save()
                            updated += 1
                            db_build_dict_dup.pop(build_obj.number)
                if new_build_objs:
                    PipelineBuildModel.objects.bulk_create(new_build_objs)
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
            "result": False,
            "detail": {
                "added": added,
                "updated": updated,
            }
        }

    @staticmethod
    def sync(pipeline_fullnames: List = None, update: bool = True, force: bool = False) -> Dict:
        from dj_jenkins.utils.time_util import TimeUtil
        from dj_jenkins.utils.j_pipeline_util import JPipelineUtil
        if not pipeline_fullnames:
            pipeline_fullnames = JPipelineUtil.get_j_pipeline_fullnames()
        result = True
        added = 0
        updated = 0
        for fullname in pipeline_fullnames:
            logger.info(f"{TimeUtil.get_log_timestamp()} syncing builds of pipeline: {fullname}")
            build_result = PipelineBuildUtil.sync_pipeline_builds(
                pipeline_fullname=fullname,
                update=update,
                force=force
            )
            result &= build_result["result"]
            added += build_result["detail"]["added"]
            updated += build_result["detail"]["updated"]
        return {
            "result": result,
            "detail": {
                "added": added,
                "updated": updated,
            }
        }

    @staticmethod
    def get_day_results(pipeline_fullnames: List = None, year: int = None, month: int = None, day: int = None) -> Dict:
        from dj_jenkins.utils import TimeUtil
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if pipeline_fullnames:
            q.children.append(("pipeline__fullname__in", pipeline_fullnames))
        if year is not None:
            q.children.append(("timestamp__year", year))
        if month is not None:
            q.children.append(("timestamp__month", month))
        if day is not None:
            q.children.append(("timestamp__day", day))
        qs = (PipelineBuildModel.objects.
              filter(q).
              order_by("timestamp"))
        result = {}
        for item in qs:
            if item.pipeline.fullname not in result:
                result[item.pipeline.fullname] = {}
            day = TimeUtil.date2str(item.timestamp.date())
            result[item.pipeline.fullname][day] = item.result
        return result




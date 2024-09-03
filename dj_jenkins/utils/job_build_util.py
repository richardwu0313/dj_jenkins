import traceback
import copy
from typing import Dict
from typing import List
from loguru import logger

from django.db import transaction
from django.db.models import Q

from dj_jenkins.models import JobBuildModel


class JobBuildUtil:

    @staticmethod
    def get_job_builds(job_fullname: str = ""):
        q = Q()
        q.connector = "AND"
        q.children.append(("is_deleted", False))
        if job_fullname:
            q.children.append(("job__fullname", job_fullname))
        qs = JobBuildModel.objects.filter(q)

        return qs

    @staticmethod
    def is_job_build_exists(job_fullname, build_number):
        ret = (JobBuildModel.objects.
               filter(is_deleted=False,
                      job__fullname=job_fullname,
                      number=build_number).
               exists())

        return ret

    @staticmethod
    def get_job_build(job_fullname, build_number):
        job_bld_obj = (JobBuildModel.objects.
                       filter(is_deleted=False,
                              job__fullname=job_fullname,
                              number=build_number).
                       first())

        return job_bld_obj

    @staticmethod
    def sync_job_builds(job_fullname: str, update: bool = True, force: bool = False) -> Dict:
        from dj_jenkins.utils.j_job_build_util import JJobBuildUtil
        if not force:
            latest_build_obj = JobBuildUtil.get_job_builds(job_fullname=job_fullname).order_by("-id").first()
            if latest_build_obj:
                latest_build_number = latest_build_obj.number
            else:
                latest_build_number = -1
        else:
            latest_build_number = -1
        build_objs = JJobBuildUtil.get_j_job_build_objs(
            job_fullname=job_fullname,
            next_sync_build_number=latest_build_number)
        db_build_objs = JobBuildUtil.get_job_builds(job_fullname)
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
                    JobBuildModel.objects.bulk_create(new_build_objs)
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

    @staticmethod
    def sync(job_fullnames: List[str] = None, update: bool = True, force: bool = False) -> Dict:
        from dj_jenkins.utils.j_job_util import JJobUtil
        from dj_jenkins.utils.time_util import TimeUtil
        result = True
        added = 0
        updated = 0
        if not job_fullnames:
            job_fullnames = JJobUtil.get_j_job_fullnames()
        for job_fullname in job_fullnames:
            logger.info(f"{TimeUtil.get_log_timestamp()} syncing builds of job: {job_fullname}")
            job_result = JobBuildUtil.sync_job_builds(
                job_fullname=job_fullname,
                update=update,
                force=force
            )
            if not job_result["result"]:
                result &= False
            added += job_result["detail"]["added"]
            updated += job_result["detail"]["updated"]
        return {
            "result": result,
            "detail": {
                "added": added,
                "updated": updated
            }
        }


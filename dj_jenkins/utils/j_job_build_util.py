from typing import List

from dj_jenkins.core import JJenkins
from dj_jenkins.core import JJobBuild
from dj_jenkins.core import JJob


class JJobBuildUtil:

    @staticmethod
    def get_j_job_build_objs(job_fullname: str, next_sync_build_number: int = -1) -> List[JJobBuild]:
        jenkins = JJenkins()
        job_obj = JJob(server=jenkins.server,
                       fullname=job_fullname,
                       init=True)
        return job_obj.builds(next_build_number=next_sync_build_number)

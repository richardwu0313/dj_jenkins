from typing import List

from dj_jenkins.core import JJenkins
from dj_jenkins.core import JPipelineBuild
from dj_jenkins.core import JPipelineBuildStage


class JPipelineBuildStageUtil:

    @staticmethod
    def get_stage_objs(pipeline_fullname: str, build_number: int) -> List[JPipelineBuildStage]:
        jenkins = JJenkins()
        build_obj = JPipelineBuild(server=jenkins.server,
                                   pipeline_fullname=pipeline_fullname,
                                   number=build_number,
                                   init=True)
        stage_objs = build_obj.stages()
        return stage_objs

from typing import List

from dj_jenkins.core import JJenkins
from dj_jenkins.core import JPipeline
from dj_jenkins.core import JPipelineBuild


class JPipelineBuildUtil:

    @staticmethod
    def get_build_objs(pipeline_fullname: str, next_build_number: int = -1) -> List[JPipelineBuild]:
        jenkins = JJenkins()
        pipeline_obj = JPipeline(server=jenkins.server,
                                 fullname=pipeline_fullname,
                                 init=True)
        build_objs = pipeline_obj.builds(next_build_number=next_build_number)
        return build_objs

    @staticmethod
    def get_build_numbers(pipeline_fullname: str, next_sync_build_number: int = -1) -> List[int]:
        jenkins = JJenkins()
        pipeline_obj = JPipeline(server=jenkins.server,
                                 fullname=pipeline_fullname,
                                 init=True)
        if next_sync_build_number != -1:
            build_numbers = [number for number in pipeline_obj.build_numbers if number >= next_sync_build_number]
        else:
            build_numbers = pipeline_obj.build_numbers
        return build_numbers

from typing import Dict
from typing import List

from dj_jenkins.models.pipeline_build import PipelineBuildModel
from dj_jenkins.models.pipeline import PipelineModel
from dj_jenkins.utils.time_util import TimeUtil
from dj_jenkins.core.j_pipeline_build_stage import JPipelineBuildStage


class JPipelineBuild:
    def __init__(self,
                 server,
                 pipeline_fullname: str,
                 number: int,
                 data: Dict = None,
                 init: bool = False):
        self._server = server
        self.pipeline_fullname = pipeline_fullname
        self.number = number
        self._data = data
        if data:
            self.init_from_data()
        elif init:
            self.init_from_cloud()

    def init_from_data(self):
        raise NotImplementedError

    def init_from_cloud(self):
        info = self._server.get_build_info(self.pipeline_fullname, self.number)
        self.description = info.get("description", "") if info["description"] else ""
        self.display_name = info.get("displayName", "")
        display_name_lst = self.display_name.split("-")
        if len(display_name_lst) < 2:
            self.submitter = ""
        else:
            if display_name_lst[1].strip() == "<Unknown>":
                self.submitter = "timer"
            else:
                self.submitter = display_name_lst[1].strip().strip("<").strip(">")
        self.duration = info.get("duration", 0) / 1000
        self.duration_estimated_seconds = info.get("estimatedDuration", 0) / 1000
        self.display_fullname = info.get("fullDisplayName", "")
        self.result = info.get("result", "") if info["result"] else ""
        self.timestamp = TimeUtil.jenkins_timestamp2datetime(info.get("timestamp", 0))
        self.url = info.get("url", "")

    def stages(self) -> List[JPipelineBuildStage]:
        info = self._server.get_build_stages(self.pipeline_fullname, self.number)
        objs = []
        for item in info.get("stages", []):
            obj = JPipelineBuildStage(
                server=self._server,
                pipeline_fullname=self.pipeline_fullname,
                number=self.number,
                name=item.get("name", ""),
                data=item)
            objs.append(obj)
        return objs

    def to_model(self) -> PipelineBuildModel:
        if not PipelineBuildModel.objects.filter(
                is_deleted=False,
                pipeline__fullname=self.pipeline_fullname,
                number=self.number).exists():
            obj = PipelineBuildModel(
                pipeline=PipelineModel.objects.filter(
                    is_deleted=False,
                    fullname=self.pipeline_fullname).first(),
                number=self.number,
                url=self.url,
                description=self.description,
                display_name=self.display_name,
                display_fullname=self.display_fullname,
                duration=self.duration,
                duration_estimated_seconds=self.duration_estimated_seconds,
                result=self.result,
                submitter=self.submitter,
                timestamp=self.timestamp)
        else:
            obj = PipelineBuildModel.objects.filter(
                is_deleted=False,
                pipeline__fullname=self.pipeline_fullname,
                number=self.number).first()
            obj.url = self.url
            obj.description = self.description
            obj.display_name = self.display_name
            obj.display_fullname = self.display_fullname
            obj.duration = self.duration
            obj.duration_estimated_seconds = self.duration_estimated_seconds
            obj.result = self.result
            obj.submitter = self.submitter
            obj.timestamp = self.timestamp
        return obj
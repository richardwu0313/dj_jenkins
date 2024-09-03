from typing import Dict

from dj_jenkins.utils.time_util import TimeUtil
from dj_jenkins.models.pipeline_build import PipelineBuildModel
from dj_jenkins.models.pipeline_build_stage import PipelineBuildStageModel


class JPipelineBuildStage:
    def __init__(self, server,
                 pipeline_fullname: str,
                 number: int,
                 name: str,
                 data: Dict = None) -> None:
        self._server = server
        self.pipeline_fullname = pipeline_fullname
        self.number = number
        self.name = name
        self.result = ""
        self.start_time = ""
        self.duration = ""
        self._data = data
        if self._data:
            self.init_from_data()

    def init_from_data(self) -> None:
        self.id = self._data.get("id", None)
        self.name = self._data.get("name", None)
        self.result = self._data.get("status", None)
        self.start_time = TimeUtil.jenkins_timestamp2datetime(self._data.get("startTimeMillis", None))
        self.duration = self._data.get("durationMillis", 0) / 1000

    def init_from_cloud_data(self) -> None:
        raise NotImplementedError

    def to_model(self) -> PipelineBuildStageModel:
        if not PipelineBuildStageModel.objects.\
                filter(is_deleted=False,
                       pipeline_build__pipeline__fullname=self.pipeline_fullname,
                       pipeline_build__number=self.number,
                       name=self.name).exists():
            obj = PipelineBuildStageModel(
                pipeline_build=PipelineBuildModel.objects.\
                    filter(is_deleted=False,
                           pipeline__fullname=self.pipeline_fullname,
                           number=self.number).first(),
                name=self.name,
                result=self.result,
                duration=self.duration,
                start_time=self.start_time)
        else:
            obj = (PipelineBuildStageModel.objects.\
                   filter(is_deleted=False,
                          pipeline_build__pipeline__fullname=self.pipeline_fullname,
                          pipeline_build__number=self.number,
                          name=self.name).first())
            obj.result = self.result
            obj.duration = self.duration
            obj.start_time = self.start_time
        return obj

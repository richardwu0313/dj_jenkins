from typing import Dict

from dj_jenkins.common.enums import JenkinsType
from dj_jenkins.utils.time_util import TimeUtil
from dj_jenkins.models.job import JobModel
from dj_jenkins.models.job_build import JobBuildModel


class JJobBuild:
    def __init__(self,
                 server,
                 job_fullname: str,
                 build_number: int,
                 data: Dict = None,
                 init: bool = False):
        self._server = server
        self._class = JenkinsType.JOB_BUILD.value
        self._data = data
        self.url = ""
        self.number = build_number
        self.node = ""
        self.result = None
        self.duration = 0
        self.building = False
        self.start_at = None
        self.end_at = None
        self.author = None
        self.job_fullname = job_fullname
        if self._data:
            self.init_from_data()
        elif init:
            self.init_from_cloud()

    def init_from_data(self):
        raise NotImplementedError

    def init_from_cloud(self):
        info = self._server.get_build_info(self.job_fullname, self.number)
        self.number = info.get("number", 0)
        self.description = info.get("description", "")
        self.display_name = info.get("displayName", "")
        display_name_lst = self.display_name.split("-")
        if len(display_name_lst) == 2:
            if display_name_lst[1].strip() == "<Unknown>":
                self.submitter = "timer"
            else:
                self.submitter = display_name_lst[1].strip().strip("<").strip(">")
        else:
            self.submitter = ""
        self.duration = info.get("duration", 0)
        self.duration_estimated = info.get("estimatedDuration", 0)
        self.display_fullname = info.get("fullDisplayName", "")
        self.result = info.get("result", "")
        self.timestamp = TimeUtil.jenkins_timestamp2datetime(info.get("timestamp", 0))
        self.url = info.get("url", "")
        self.next_build_number = info.get("nextBuild", 0)
        self.previous_build_number = info.get("previousBuild", 0)

    def to_model(self) -> JobBuildModel:
        if not JobBuildModel.objects.filter(
                is_deleted=False,
                job__fullname=self.job_fullname,
                number=self.number).exists():
            obj = JobBuildModel(
                job=JobModel.objects.get(
                    is_deleted=False,
                    fullname=self.job_fullname),
                number=self.number,
                description=self.description,
                display_name=self.display_name,
                duration=self.duration,
                duration_estimated=self.duration_estimated,
                result=self.result,
                url=self.url,
                next_build_number=self.next_build_number,
                previous_build_number=self.previous_build_number,
                timestamp=self.timestamp)
        else:
            obj = JobBuildModel.objects.filter(
                is_deleted=False,
                job__fullname=self.job_fullname,
                number=self.number).first()
            obj.job = JobModel.objects.get(
                is_deleted=False,
                fullname=self.job_fullname)
            obj.number = self.number
            obj.description = self.description
            obj.display_name = self.display_name
            obj.duration = self.duration
            obj.duration_estimated = self.duration_estimated
            obj.result = self.result
            obj.url = self.url
            obj.next_build_number = self.next_build_number
            obj.previous_build_number = self.previous_build_number
            obj.timestamp = self.timestamp
        return obj
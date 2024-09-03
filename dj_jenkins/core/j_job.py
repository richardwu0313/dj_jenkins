from typing import List

from dj_jenkins.common.enums import JenkinsType
from dj_jenkins.models.job import JobModel
from dj_jenkins.core.j_job_build import JJobBuild


class JJob:
    def __init__(self,
                 server,
                 fullname: str,
                 data: dict = None,
                 init: bool = False):
        self._server = server
        self._class = JenkinsType.JOB.value
        self.name = fullname.split('/')[-1]
        self.prefix = fullname.split('/')[:-1]
        self.fullname = fullname
        self.url = ""
        self.color = ""
        self.next_build_number = 0
        self.build_numbers = []
        self.first_build = None
        self.last_build = None
        self.last_completed_build = None
        self.last_failed_build = None
        self.last_stable_build = None
        self.last_successful_build = None
        self.last_unsuccessful_build = None
        self.last_unstable_build = None
        self.in_queue = False
        self.description = ""
        self.downstream_jobs = []
        self.upstream_jobs = []
        self.status = ""
        self._data = data
        if self._data:
            self.init_from_data()
        elif init:
            self.init_from_cloud()

    def init_from_data(self):
        self.name = self._data.get("name", "")
        self.url = self._data.get("url", "")
        self.color = self._data.get("color", "")
        self.fullname = self._data.get("fullname", "")

    def init_from_cloud(self):
        info = self._server.get_job_info(self.fullname)
        self.description = info.get("description", "")
        self.display_name = info.get("displayName", "")
        self.display_fullname = info.get("fullDisplayName", "")
        self.name = info.get("name", "")
        self.url = info.get("url", "")
        self.buildable = info.get("buildable", False)
        for bld in info.get("builds", []):
            self.build_numbers.append(bld.get("number", 0))
        self.color = info.get("color", "")
        self.first_build_number = info.get("firstBuild", {}).get("number", 0) if info.get("firstBuild") else 0
        self.in_queue = info.get("inQueue", False)
        self.last_build_number = info.get("lastBuild", {}).get("number", 0) if info.get("lastBuild") else 0
        self.last_completed_build_number = info.get("lastCompletedBuild", {}).get("number", 0) if info.get("lastCompletedBuild") else 0
        self.last_failed_build_number = info.get("lastFailedBuild", {}).get("number", 0) if info.get("lastFailedBuild", {}) else 0
        self.last_stable_build_number = info.get("lastStableBuild", {}).get("number", 0) if info.get("lastStableBuild", {}) else 0
        self.last_successful_build_number = info.get("lastSuccessfulBuild", {}).get("number", 0) if info.get("lastSuccessfulBuild", {}) else 0
        self.last_unstable_build_number = info.get("lastUnstableBuild", {}).get("number", 0) if info.get("lastUnstableBuild", {}) else 0
        self.last_unsuccessful_build_number = info.get("lastUnsuccessfulBuild", {}).get("number", 0) if info.get("lastUnsuccessfulBuild", {}) else 0
        self.next_build_number = info.get("nextBuildNumber", 0) if info.get("nextBuildNumber", 0) else 0

    def builds(self, next_build_number: int = -1) -> List[JJobBuild]:
        objs = []
        for bld in self.build_numbers:
            if next_build_number == -1 or (next_build_number != -1 and bld >= next_build_number):
                obj = JJobBuild(self._server,
                                self.fullname,
                                bld,
                                init=True)
                objs.append(obj)
        return objs

    def to_model(self) -> JobModel:
        if not JobModel.objects.filter(is_deleted=False,
                                       fullname=self.fullname).exists():
            obj = JobModel(
                fullname=self.fullname,
                name=self.name,
                url=self.url,
                display_name=self.display_name,
                display_fullname=self.display_fullname,
                description=self.description,
                color=self.color,
                next_build_number=self.next_build_number,
                first_build_number=self.first_build_number,
                last_build_number=self.last_build_number,
                last_stable_build_number=self.last_stable_build_number,
                last_unstable_build_number=self.last_unstable_build_number,
                last_completed_build_number=self.last_completed_build_number,
                last_failed_build_number=self.last_failed_build_number,
                last_successful_build_number=self.last_successful_build_number,
                last_unsuccessful_build_number=self.last_unsuccessful_build_number)
        else:
            obj = JobModel.objects.filter(fullname=self.fullname).first()
            obj.name = self.name
            obj.fullname = self.fullname
            obj.url = self.url
            obj.display_fullname = self.display_fullname
            obj.display_name = self.display_name
            obj.description = self.description
            obj.color = self.color
            obj.next_build_number = self.next_build_number
            obj.first_build_number = self.first_build_number
            obj.last_build_number = self.last_build_number
            obj.last_stable_build_number = self.last_stable_build_number
            obj.last_unstable_build_number = self.last_unstable_build_number
            obj.last_completed_build_number = self.last_completed_build_number
            obj.last_failed_build_number = self.last_failed_build_number
            obj.last_successful_build_number = self.last_successful_build_number
            obj.last_unsuccessful_build_number = self.last_unsuccessful_build_number
        return obj

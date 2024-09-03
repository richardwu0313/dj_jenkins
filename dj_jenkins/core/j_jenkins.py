import jenkins as std_jenkins
from typing import List
from loguru import logger

from settings import JENKINS


from dj_jenkins.common.enums import Timeout
from dj_jenkins.common.enums import JenkinsType


class JJenkins:
    def __init__(self,
                 url=JENKINS.get("URL"),
                 username=JENKINS.get("USERNAME"),
                 password=JENKINS.get("PASSWORD"),
                 timeout=Timeout.XShort):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.server = None
        self.init()

    def init(self):
        try:
            self.server = std_jenkins.Jenkins(
                url=self.url,
                username=self.username,
                password=self.password,
                timeout=self.timeout)
            self.server.get_whoami()
        except std_jenkins.JenkinsException as ex:
            logger.error(f"failed to connect to Jenkins server {self.url}, message: {ex}")
        except Exception as ex:
            logger.error(f"failed to connect to Jenkins server {self.url}, message: {ex}")

    @property
    def version(self) -> str:
        return self.server.get_version()

    @property
    def plugins(self):
        return self.server.get_plugins()

    @property
    def jobs(self) -> List:
        jobs = self.server.get_all_jobs()
        return jobs

    @property
    def running_jobs(self):
        jobs = self.server.get_running_jobs()
        return jobs

    @property
    def queuing_jobs(self):
        jobs = self.server.get_queued_items()
        return jobs

    def get_job_info(self, job_fullname: str) -> dict:
        data = self.server.get_job_info(name=job_fullname)
        return data

    def get_build_info(self, job_fullname: str, build_number: int) -> dict:
        data = self.server.get_build_info(name=job_fullname, number=build_number)
        return data

    @property
    def folders(self) -> List:
        from dj_jenkins.core.j_folder import JFolder
        folder_objs = []
        data = self.server.get_all_jobs()
        for item in data:
            if item.get("_class") == JenkinsType.FOLDER.value:
                folder_obj = JFolder(server=self.server,
                                     fullname=item.get("fullname", ""),
                                     init=True)
                folder_objs.append(folder_obj)
        return folder_objs

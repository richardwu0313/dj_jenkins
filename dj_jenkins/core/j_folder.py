from dj_jenkins.common.enums import JenkinsType


class JFolder:
    def __init__(self,
                 server,
                 fullname: str,
                 data: dict = None,
                 init: bool = False):
        self._server = server
        self._class = JenkinsType.FOLDER.value
        self.name = ""
        self.fullname = fullname
        self._data = data
        if self._data:
            self.init_from_data()
        elif init:
            self.init_from_cloud()

    def init_from_data(self):
        self.name = self._data.get("name", "")
        self.url = self._data.get("url", "")

    def init_from_cloud(self):
        info = self._server.get_job_info(self.fullname)
        self.name = info.get("name", "")
        self.url = info.get("url", "")


from typing import List

from dj_jenkins.common.enums import JenkinsType
from dj_jenkins.core import JJob
from dj_jenkins.core import JJenkins


class JJobUtil:

    @staticmethod
    def recursive_job(server, data: List):
        jobs = []
        for item in data:
            if item.get("_class") == JenkinsType.FOLDER.value:
                jobs.extend(JJobUtil.recursive_job(server, item.get("jobs")))
            elif item.get("_class") == JenkinsType.JOB.value:
                jobs.append(JJob(server=server,
                                 fullname=item.get("fullname"),
                                 data=item))
            elif item.get("_class") == JenkinsType.PIPELINE.value:
                continue
            else:
                raise Exception("unknown jenkins job type")
        return jobs

    @staticmethod
    def get_j_jobs():
        jen = JJenkins()
        jobs = jen.jobs
        job_list = []
        for job in jobs:
            if job["_class"] == JenkinsType.JOB.value:
                job_list.append(job)

        return job_list

    @staticmethod
    def get_j_running_jobs():
        jen = JJenkins()
        job_list = jen.running_jobs

        return job_list

    @staticmethod
    def get_j_running_job_names():
        jen = JJenkins()
        job_list = jen.running_jobs
        names = []
        for job in job_list:
            names.append(job["name"])

        return names

    @staticmethod
    def get_j_queuing_jobs():
        jen = JJenkins()
        jobs = jen.queuing_jobs
        queuing_jobs = []
        for job in jobs:
            queuing_jobs.append(job["task"]["name"])

        return queuing_jobs

    @staticmethod
    def get_j_job_next_build_number(job_fullname):
        jen = JJenkins()
        job_obj = jen.get_job_info(job_fullname=job_fullname)
        build_number = job_obj.next_build_number()

        return build_number

    @staticmethod
    def get_j_job(job_fullname):
        jen = JJenkins()
        job_info = jen.get_job_info(job_fullname=job_fullname)

        return job_info

    @staticmethod
    def get_j_job_build_info(job_fullname, build_number):
        from dj_jenkins.utils.time_util import TimeUtil
        jen = JJenkins()
        info = jen.get_build_info(job_fullname=job_fullname,
                                  build_number=build_number)

        return {"name": info.name,
                "url": info.url,
                "number": info.number,
                "result": info.result,
                "duration": info.duration,
                "building": info.building,
                "start_at": TimeUtil.timestamp2datetime(timestamp=info.start_at)}

    @staticmethod
    def get_j_job_fullnames() -> List[str]:
        server = JJenkins()
        jobs = server.jobs
        fullnames = []
        for item in jobs:
            if item.get("_class") == JenkinsType.JOB.value:
                fullnames.append(item.get("fullname", ""))
        return fullnames

    @staticmethod
    def get_j_job_objs(fullnames: List[str] = None) -> List[JJob]:
        server = JJenkins()
        jobs = server.jobs
        job_objs = []
        for item in jobs:
            if item.get("_class") == JenkinsType.JOB.value and \
                    (not fullnames or item.get("fullname") in fullnames):
                job_obj = JJob(server=server,
                               fullname=item.get("fullname", ""),
                               init=True)
                job_objs.append(job_obj)
        return job_objs

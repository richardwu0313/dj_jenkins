from typing import List

from dj_jenkins.common.enums import JenkinsType
from dj_jenkins.core import JPipeline
from dj_jenkins.core import JJenkins
from dj_jenkins.models import PipelineModel


class JPipelineUtil:

    @staticmethod
    def recursive_pipeline(server, data: List):
        pipelines = []
        for item in data:
            if item.get("_class") == JenkinsType.FOLDER.value:
                pipelines.extend(JPipelineUtil.recursive_pipeline(server, item.get("jobs")))
            elif item.get("_class") == JenkinsType.JOB.value:
                continue
            elif item.get("_class") == JenkinsType.PIPELINE.value:
                pipelines.append(JPipeline(server=server,
                                           fullname=item.get("fullname"),
                                           data=item))
            else:
                raise Exception("unknown jenkins pipeline type")
        return pipelines

    @staticmethod
    def get_j_pipelines():
        jen = JJenkins()
        jobs = jen.jobs
        pipelines = []
        for item in jobs:
            if item.get("_class") == JenkinsType.PIPELINE.value:
                pipelines.append(item)
        return pipelines

    @staticmethod
    def get_j_running_pipeline_names():
        jen = JJenkins()
        jobs = jen.running_jobs
        pl_list = []
        for job in jobs:
            if job["_class"] == JenkinsType.PIPELINE.value:
                pl_list.append(job)

        return pl_list

    @staticmethod
    def get_j_pipeline_first_job(pipeline_name):
        jen = JJenkins()
        pl_config = jen.server.get_view_config(name=pipeline_name)
        pl_obj = JPipeline(server=jen.server,
                           fullname=pipeline_name,
                           init=False)
        pl_obj.init_config(pl_config)
        first_job = pl_obj.first_job

        return first_job

    @staticmethod
    def get_j_pipeline_number(pipeline_name):
        jen = JJenkins()
        pl_config = jen.server.get_view_config(name=pipeline_name)
        pl_obj = JPipeline(server=jen.server,
                           fullname=pipeline_name,
                           init=False)
        pl_obj.init_config(pl_config)
        first_job = pl_obj.first_job
        job_info = jen.get_job_info(name=first_job)
        build_number = job_info.next_build_number
        return build_number

    @staticmethod
    def trigger_pipeline(pipeline_name, param_dict):
        jen = JJenkins()
        pl_config = jen.server.get_view_config(name=PIPELINE[pipeline_name])
        pl_obj = JPipeline()
        pl_obj.init_config(pl_config)
        first_job = pl_obj.first_job
        ret = jen.trigger_job(name=first_job, param_dict=param_dict)

        return ret

    @staticmethod
    def add_pipeline(pipeline_name):
        jen = JJenkins()
        pl_config = jen.server.get_view_config(name=pipeline_name)
        pl_info = JPipeline()
        pl_info.init_config(pl_config)
        pl_obj = PipelineModel()
        pl_obj.name = pipeline_name
        pl_obj.desc = pl_info.description
        pl_obj.save()

        return pl_obj

    @staticmethod
    def get_j_pipeline_objs(fullnames: List[str] = None) -> List[JPipeline]:
        jenkins = JJenkins()
        jobs = jenkins.jobs
        pipeline_objs = []
        for item in jobs:
            if item.get("_class") == JenkinsType.PIPELINE.value and \
                    (not fullnames or item.get("fullname") in fullnames):
                pp_obj = JPipeline(server=jenkins.server,
                                   fullname=item.get("fullname", ""),
                                   init=True)
                pipeline_objs.append(pp_obj)
        return pipeline_objs

    @staticmethod
    def get_j_pipeline_fullnames() -> List[str]:
        pipeline_objs = JPipelineUtil.get_j_pipeline_objs()
        fullnames = []
        for obj in pipeline_objs:
            fullnames.append(obj.fullname)
        return fullnames

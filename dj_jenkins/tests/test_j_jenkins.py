from dj_jenkins.utils import JPipelineUtil
from dj_jenkins.utils import JJobUtil


class TestJJenkins:

    def test_j_jobs(self):
        jobs = JJobUtil.get_j_jobs()
        assert jobs

    def test_j_job_fullnames(self):
        fullnames = JJobUtil.get_j_job_fullnames()
        assert fullnames

    def test_j_job_objs(self):
        jobs = JJobUtil.get_j_job_objs()
        assert jobs

    def test_j_pipelines(self):
        pipelines = JPipelineUtil.get_j_pipelines()
        assert pipelines

    def test_j_pipeline_objs(self):
        pipelines = JPipelineUtil.get_j_pipeline_objs()
        assert pipelines

    def test_j_pipeline_fullnames(self):
        fullnames = JPipelineUtil.get_j_pipeline_fullnames()
        assert fullnames



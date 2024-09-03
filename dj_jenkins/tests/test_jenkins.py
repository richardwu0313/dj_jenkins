from dj_jenkins.utils import PipelineUtil
from dj_jenkins.utils import JobUtil


class TestJenkins:

    def test_jobs(self):
        jobs = JobUtil.get_jobs()
        assert jobs

    def test_pipelines(self):
        pipelines = PipelineUtil.get_pipeline_objs()
        assert pipelines

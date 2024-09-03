from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class JenkinsViewSet(ViewSet):

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        from dj_jenkins.utils import JobUtil
        from dj_jenkins.utils import JobBuildUtil
        from dj_jenkins.utils import PipelineUtil
        from dj_jenkins.utils import PipelineBuildUtil
        from dj_jenkins.utils import PipelineBuildStageUtil
        force = request.data.get("force", False)
        job_fullnames = request.query_params.get("job_fullnames", "")
        job_fullnames = job_fullnames.split(",")
        pipeline_fullnames = request.query_params.get("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        result = True
        added = 0
        updated = 0

        # sync job build
        job_build_result = JobBuildUtil.sync(
            update=False,
            force=force
        )
        result &= job_build_result["result"]
        added += job_build_result["detail"]["added"]
        updated += job_build_result["detail"]["updated"]
        # sync job
        job_result = JobUtil.sync(update=True)
        result &= job_result["result"]
        added += job_result["detail"]["added"]
        updated += job_result["detail"]["updated"]

        # sync pipeline build
        pipeline_build_result = PipelineBuildUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=False,
            force=force)
        result &= pipeline_build_result["result"]
        added += pipeline_build_result["detail"]["added"]
        updated += pipeline_build_result["detail"]["updated"]
        # sync pipeline build stage
        pipeline_build_stage_result = PipelineBuildStageUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=False,
            force=force)
        result &= pipeline_build_stage_result["result"]
        added += pipeline_build_stage_result["detail"]["added"]
        updated += pipeline_build_stage_result["detail"]["updated"]
        # sync pipeline
        pipeline_result = PipelineUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=True)
        result &= pipeline_result["result"]
        added += pipeline_result["detail"]["added"]
        updated += pipeline_result["detail"]["updated"]

        return Response(
            {
                "result": result,
                "detail": {
                    "added": added,
                    "updated": updated,
                }
            })

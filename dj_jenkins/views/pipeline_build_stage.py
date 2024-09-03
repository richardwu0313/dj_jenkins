import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dj_jenkins.utils import PipelineBuildStageUtil
from dj_jenkins.serializers import PipelineBuildStageSerializer
from dj_jenkins.utils import TimeUtil


class PipelineBuildStageViewSet(viewsets.ModelViewSet):
    queryset = PipelineBuildStageUtil.get_stages()
    serializer_class = PipelineBuildStageSerializer

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        pipeline_fullnames = request.data.get("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        # stage: after build stage, info can't change, so update always==False
        # force: sync since from next build number when false, sync all when true
        force = bool(request.query_params.get("force", False))
        if isinstance(force, str):
            if force.lower() == "true":
                force = True
            else:
                force = False
        result = PipelineBuildStageUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=False,
            force=force
        )
        return Response(result)

    @action(detail=False, methods=["get"], url_path="results")
    def results(self, request):
        pipeline_fullnames = request.data.get("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        year_month_day = TimeUtil.str2date(request.query_params.get("date",
                                                                    datetime.datetime.now().strftime("%Y-%m-%d")))
        year = int(str(year_month_day).split("-")[0])
        month = int(str(year_month_day).split("-")[1].strip("0"))
        day = int(str(year_month_day).split("-")[2].strip("0"))
        result = {}
        for pipeline_fullname in pipeline_fullnames.split(","):
            result[pipeline_fullname] = PipelineBuildStageUtil.get_pipeline_build_stage_results(
                pipeline_fullname,
                year,
                month,
                day)
        return Response(result)

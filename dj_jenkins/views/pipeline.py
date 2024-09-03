from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dj_jenkins.utils import PipelineUtil
from dj_jenkins.serializers import PipelineSerializer


class PipelineViewSet(viewsets.ModelViewSet):
    queryset = PipelineUtil.get_pipeline_objs()
    serializer_class = PipelineSerializer

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        pipeline_fullnames = request.data.get("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        result = PipelineUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=True)
        return Response(result)





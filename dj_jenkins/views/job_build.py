from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dj_jenkins.utils import JobBuildUtil
from dj_jenkins.serializers import JobBuildSerializer


class JobBuildViewSet(viewsets.ModelViewSet):

    queryset = JobBuildUtil.get_job_builds()
    serializer_class = JobBuildSerializer

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        job_fullnames = request.data.get("job_fullnames", "")
        job_fullnames = job_fullnames.split(",")
        force = request.data.get("force", False)
        if isinstance(force, str):
            if force.lower() == "true":
                force = True
            else:
                force = False
        result = JobBuildUtil.sync(job_fullnames=job_fullnames,
                                   update=force)
        return Response(result)

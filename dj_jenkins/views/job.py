from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dj_jenkins.utils import JobUtil
from dj_jenkins.serializers import JobSerializer
from dj_jenkins.common.http_code import HttpCode


class JobViewSet(viewsets.ModelViewSet):

    queryset = JobUtil.get_job_objs()
    serializer_class = JobSerializer

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        job_fullnames = request.data.get("job_fullnames", "")
        job_fullnames = job_fullnames.split(",")
        result = JobUtil.sync(
            job_fullnames=job_fullnames,
            update=True)
        return Response(result)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({
            "code": HttpCode.HTTP_20203_DELETED,
            "msg": "job deleted",
            "data": None
        })




from rest_framework.serializers import ModelSerializer

from dj_jenkins.models import JobModel


class JobSerializer(ModelSerializer):

    class Meta:
        model = JobModel
        fields = "__all__"




from rest_framework.serializers import ModelSerializer

from dj_jenkins.models import JobBuildModel


class JobBuildSerializer(ModelSerializer):

    class Meta:
        model = JobBuildModel
        fields = "__all__"

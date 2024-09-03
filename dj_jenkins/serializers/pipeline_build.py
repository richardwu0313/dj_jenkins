from rest_framework.serializers import ModelSerializer

from dj_jenkins.models import PipelineBuildModel


class PipelineBuildSerializer(ModelSerializer):
    class Meta:
        model = PipelineBuildModel
        fields = "__all__"

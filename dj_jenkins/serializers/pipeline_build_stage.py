
from rest_framework.serializers import ModelSerializer

from dj_jenkins.models import PipelineBuildStageModel


class PipelineBuildStageSerializer(ModelSerializer):
    class Meta:
        model = PipelineBuildStageModel
        fields = "__all__"

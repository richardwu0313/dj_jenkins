from rest_framework.serializers import ModelSerializer

from dj_jenkins.models import PipelineModel


class PipelineSerializer(ModelSerializer):

    class Meta:
        model = PipelineModel
        fields = "__all__"






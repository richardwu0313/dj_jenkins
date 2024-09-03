from django.db import models

from dj_jenkins.models.base import BaseModel


class PipelineBuildStageModel(BaseModel):
    name = models.CharField(max_length=128, unique=False)
    result = models.CharField(max_length=16, unique=False)
    duration = models.IntegerField(unique=False)
    start_time = models.DateTimeField()
    pipeline_build = models.ForeignKey(
        "PipelineBuildModel",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        db_table = "pipeline_build_stage"
        app_label = "dj_jenkins"
        verbose_name = "PipelineBuildStageModel"
        verbose_name_plural = verbose_name

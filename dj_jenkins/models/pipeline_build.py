from django.db import models

from dj_jenkins.models.base import BaseModel


class PipelineBuildModel(BaseModel):
    number = models.IntegerField()
    submitter = models.CharField(max_length=64, null=True, blank=True)
    url = models.URLField(max_length=1024, unique=False)
    description = models.CharField(max_length=1024, unique=False)
    display_name = models.CharField(max_length=128, unique=False)
    display_fullname = models.CharField(max_length=128, unique=False)
    duration = models.IntegerField(unique=False)
    duration_estimated_seconds = models.IntegerField(unique=False)
    result = models.CharField(max_length=16, unique=False)
    timestamp = models.DateTimeField()
    pipeline = models.ForeignKey(
        "PipelineModel",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        db_table = "pipeline_build"
        app_label = "dj_jenkins"
        verbose_name = "PipelineBuildModel"
        verbose_name_plural = verbose_name

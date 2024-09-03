from django.db import models

from dj_jenkins.models.base import BaseModel


class PipelineModel(BaseModel):
    name = models.CharField(max_length=128, unique=False)
    fullname = models.CharField(max_length=128, unique=False)
    url = models.URLField(max_length=1024, unique=False)
    description = models.TextField(max_length=1024, unique=False)
    display_name = models.CharField(max_length=128, unique=False)
    display_fullname = models.CharField(max_length=128, unique=False)
    color = models.CharField(max_length=32, unique=False)
    next_build_number = models.IntegerField(unique=False)
    first_build_number = models.IntegerField(unique=False)
    last_build_number = models.IntegerField(unique=False)
    last_completed_build_number = models.IntegerField(unique=False)
    last_failed_build_number = models.IntegerField(unique=False)
    last_successful_build_number = models.IntegerField(unique=False)
    last_unsuccessful_build_number = models.IntegerField(unique=False)
    last_stable_build_number = models.IntegerField(unique=False)
    last_unstable_build_number = models.IntegerField(unique=False)

    class Meta:
        db_table = "pipeline"
        app_label = "dj_jenkins"
        verbose_name = "PipelineModel"
        verbose_name_plural = verbose_name






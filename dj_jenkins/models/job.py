from django.db import models

from dj_jenkins.models.base import BaseModel


class JobModel(BaseModel):
    name = models.CharField(max_length=128, unique=False)
    fullname = models.CharField(max_length=128, unique=False)
    url = models.URLField(max_length=1024, unique=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    display_name = models.CharField(max_length=128, null=True, blank=True)
    display_fullname = models.CharField(max_length=256, null=True, blank=True)
    color = models.CharField(max_length=32, null=True, blank=True)
    next_build_number = models.IntegerField(null=True, blank=True)
    first_build_number = models.IntegerField(null=True, blank=True)
    last_build_number = models.IntegerField(null=True, blank=True)
    last_stable_build_number = models.IntegerField(null=True, blank=True)
    last_unstable_build_number = models.IntegerField(null=True, blank=True)
    last_completed_build_number = models.IntegerField(null=True, blank=True)
    last_failed_build_number = models.IntegerField(null=True, blank=True)
    last_successful_build_number = models.IntegerField(null=True, blank=True)
    last_unsuccessful_build_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = "job"
        app_label = "dj_jenkins"
        verbose_name = "JobModel"
        verbose_name_plural = verbose_name


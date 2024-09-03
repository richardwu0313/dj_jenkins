from django.db import models

from dj_jenkins.models.base import BaseModel


class JobBuildModel(BaseModel):
    number = models.IntegerField()
    submitter = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    display_name = models.CharField(max_length=128, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    duration_estimated = models.IntegerField(null=True, blank=True)
    result = models.CharField(max_length=16, null=True, blank=True)
    timestamp = models.DateTimeField()
    url = models.URLField(max_length=1024, null=True, blank=True)
    next_build_number = models.IntegerField(null=True, blank=True)
    previous_build_number = models.IntegerField(null=True, blank=True)
    job = models.ForeignKey(
        "JobModel",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True)

    def get_job_name(self):
        return self.job.fullname

    def __str__(self):
        return self.job.fullname + ":" + str(self.number)

    class Meta:
        db_table = "job_build"
        app_label = "dj_jenkins"
        verbose_name = "JobBuildModel"
        verbose_name_plural = verbose_name
        unique_together = (("job", "number"),)

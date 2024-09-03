from django.db import models


class BaseModel(models.Model):
    """
    base model for user-defined model
    """
    is_deleted = models.BooleanField(default=False, verbose_name="Deleted?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created DateTime")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated DateTime")
    deleted_at = models.DateTimeField(auto_now=True, verbose_name="Deleted DateTime")
    url = models.CharField(max_length=256)

    class Meta:
        abstract = True


from django.db import models
from django.conf import settings


STATUS_LIST = (
    ("PEN", "pending"),
    ("PROCESS", "processing"),
    ("DONE", "done"),
)


class Video(models.Model):
    task_id = models.BigIntegerField(max_length=50, null=True)
    status = models.CharField(max_length=20, choices=STATUS_LIST, default="PEN")

    @property
    def original_path(self):
        upload_path = settings.MEDIA_ROOT + "/uploads/"
        return f"{upload_path}/{self.pk}.jpg"

    @property
    def result_path(self):
        processed_path = settings.MEDIA_ROOT + "/processed/"
        return f"{processed_path}/{self.pk}.jpg"


class Detection(models.Model):
    score = models.FloatField(max_length=50, default=0)
    type = models.CharField(max_length=50)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)

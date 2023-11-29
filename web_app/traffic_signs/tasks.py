from celery import shared_task
from .utils import draw_counters
from .models import Video
import requests
import os
import json


@shared_task
def detect_problem(video_id):
    video = Video.objects.get(pk=video_id)
    video.status = "PROCESS"
    video.save()

    upload_path = video.original_path
    result_path = video.result_path

    data = {'url': video.original_path}

    api = os.getenv("API_URL")

    r = requests.post(f"http://{api}/video/", )
    data = r.json()["results"]
    draw_counters(upload_path, result_path, data, video_id)
    video.status = "DONE"
    video.save()

    return video_id


@shared_task
def test():
    print("asdasdadsasdsa")

import base64
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import VideoForm
from .utils import handle_uploaded_file
from .tasks import detect_problem, test
from .models import Video, Detection


def main_camera(request):
    form = VideoForm()

    context = {
        'form': form,
        'data': None,
    }

    if request.method == 'GET':
        return render(request, "index.html", context)

    elif request.method == 'POST':

        video = Video()
        video.save()

        task = detect_problem.delay(video.pk)

        # return JsonResponse({'Json': str(task)})
        return redirect("result", video.pk)


def result(request, video_id):
    video = Video.objects.get(pk=video_id)
    try:
        detections = Detection.objects.filter(video_id=video_id)
    except Detection.DoesNotExist:
        detections = []

    status = video.status

    preds = [{
        "class": det.type,
        "score": det.score,
    } for det in detections]

    result_path = video.result_path

    return render(request, 'results.html', context={
        "status": status,
        "result_path": result_path,
        "preds": preds,
    })
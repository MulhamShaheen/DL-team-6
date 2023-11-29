from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from .infrustructure.detector import *

app = FastAPI()
yolo_detector = YoloDetector("E:/AI Talent Hub/Deep Learning/Traffic Signs/inference_api/infrustructure/8s.pt")
UPLOAD_PATH = "uploads"


class VideoRequest(BaseModel):
    url: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/video/")
async def start_detecting(request: VideoRequest):
    res, video_path = yolo_detector.detect_contours_video(vid_url=request.url)
    preds = []
    for frame in res:
        temp = []
        for i in frame:
            temp.append(i.dict())
        preds.append(temp)

    return {"url": request.url, "results": preds, "path": video_path}

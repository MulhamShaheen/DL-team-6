from abc import ABC, abstractmethod
import os
import cv2
from typing import List
from dataclasses import dataclass, asdict
import logging
import numpy as np
from .contour import Contour
from ultralytics import YOLO
from cap_from_youtube import cap_from_youtube



@dataclass
class DetectorPrediction:
    predicted_contour: Contour
    contour_probability: float
    contour_class: int

    dict = asdict
    names = {
        0: 'blue_border',
        1: 'blue_rect',
        2: 'danger',
        3: 'main_road',
        4: 'mandatory',
        5: 'prohibitory'
    }

    colores = {
        0: (255, 0, 0),
        1: (255, 122, 0),
        2: (0, 255, 0),
        3: (0, 255, 122),
        4: (0, 0, 255),
        5: (122, 0, 255)
    }

    def dict(self):
        return {
            "contour": self.predicted_contour.xyxy,
            "probability": self.contour_probability,
            "class": self.names[int(self.contour_class)],
            "color": self.colores[int(self.contour_class)],
        }


class Detector(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def detect_contours(self, image: np.ndarray) -> List[DetectorPrediction]:
        """
        Return boxes of all detected contours from image.
        :param image: np.ndarray RGB image
        :return: List[Contour]
        """
        pass


class DummyDetector(Detector):

    def __init__(self, detection_model_path: str):
        logging.info('Loading Detector')
        self.model_path = detection_model_path

    def detect_contours(self, image: np.ndarray) -> List[DetectorPrediction]:
        dummy_contour = Contour(bounding_rect=(0, 0, 50, 50))
        prediction = DetectorPrediction(predicted_contour=dummy_contour, contour_probability=0.98)
        return [prediction]


class YoloDetector(DummyDetector):

    def __init__(self, detection_model_path: str):
        super().__init__(detection_model_path)
        self._load_model()

    def _load_model(self):
        self.model = YOLO(self.model_path)

    def detect_contours(self, img) -> [DetectorPrediction]:
        predictions = []
        results = self.model(img)
        for result in results[0].boxes.data:

            contour = Contour(bounding_rect=(result[0], result[1], result[2], result[3]))
            prediction = DetectorPrediction(contour, float(result[4]), int(result[-1]))
            predictions.append(prediction)

        return predictions

    def detect_contours_video(self, vid_url: str, save=True):
        video_id = vid_url.split("/")[-2] + "_" + vid_url.split("/")[-1]
        frames_dir = f"media/frames/{video_id}"
        video_dir = "media/videos/"
        os.makedirs(frames_dir,exist_ok=True)
        cap = cap_from_youtube(vid_url, resolution='720p')
        start_time = 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_time * cap.get(cv2.CAP_PROP_FPS))
        count = 0
        height, width = 0, 0
        res = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            height, width, layers = frame.shape
            preds = self.detect_contours(frame)
            if preds != []:
                res.append(preds)
            for pred in preds:
                data = pred.dict()
                cv2.rectangle(frame, (int(pred.predicted_contour.x_min), int(pred.predicted_contour.y_min)),
                              (int(pred.predicted_contour.x_max), int(pred.predicted_contour.y_max)), data["color"], 2)

            cv2.imwrite(f"{frames_dir}/{count}.jpg", frame)
            count += 1

        if save:
            video = cv2.VideoWriter(video_id+".avi", 0, 1, (width, height))
            images = [img for img in os.listdir(frames_dir) if img.endswith(".jpg")]
            for image in images:
                video.write(cv2.imread(os.path.join(frames_dir, image)))

            cv2.destroyAllWindows()
            video.release()

        return res, video_dir + video_id

    def save_predictions(self, img_path: str, path: str):
        predictions = self.model(img_path)
        return predictions.save(filepath=path)

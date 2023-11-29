from ultralytics import YOLO

model = YOLO("../infrustructure/Yolov8s.pt")
model.export(format="onnx", imgsz=1280)
from ultralytics import YOLO

model = YOLO("yolo11s.pt")

def detectObjects(image):
    results = model(image, verbose=False)
    return results[0].plot() # Annotated Frame

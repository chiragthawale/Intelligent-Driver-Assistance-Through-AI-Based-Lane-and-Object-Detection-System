from ultralytics import YOLO

model = YOLO(r'ckpts\best.pt')


class DetectObject:
    def __init__(self):
        pass
    
    def detect(self, frame):
        """Detects the Road Objects like Cars, Trucks, Cycles etc."""
        
        result = model(frame)

        processed_frame = result[0].plot() if hasattr(result[0], 'plot') else frame
        
        return processed_frame
    
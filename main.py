import os
import cv2
from lane_detector.detector import DetectLane
from object_detector.detector import DetectObject


class LO_Detector:
    def __init__(self, op_dir=None):
        self.op_dir = op_dir if op_dir else "results"
        self.lane_detector = DetectLane()
        self.obj_detector = DetectObject()
        
    def detect(self, video_path):
     
        file_name = os.path.basename(video_path)

        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise Exception("Can't open the video.")
        
        
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        output_video_path = os.path.join(self.op_dir, file_name)
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (original_width, original_height))

        while cap.isOpened():
            ret, frame = cap.read()
    
            if not ret:
                break
    
            frame = self.lane_detector.detect(frame)
            frame = self.obj_detector.detect(frame)
            out.write(frame)
            
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        return output_video_path
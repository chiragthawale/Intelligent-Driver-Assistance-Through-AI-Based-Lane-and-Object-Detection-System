import numpy as np
import cv2


class DetectLane:
    def __init__(self,):
        pass
        
    def detect(self, frame):
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        blurred_frame = cv2.GaussianBlur(hsv_frame, (3, 3), 0)
        
        edges = cv2.Canny(blurred_frame, 50, 150, 7)
        
        height, width = frame.shape[:2]
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height),
            (width, height),
            (width // 2, int(height * 0.6))  
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        
        masked_edges = cv2.bitwise_and(edges, mask)
        
        lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 100, np.array([]), minLineLength=100, maxLineGap=150)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)        

        return frame
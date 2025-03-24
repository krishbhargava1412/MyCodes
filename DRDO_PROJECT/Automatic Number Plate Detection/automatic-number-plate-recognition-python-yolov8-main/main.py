import os
from ultralytics import YOLO
import cv2

import util
from sort.sort import *
from util import get_car, read_license_plate, write_csv

results = {}

mot_tracker = Sort()

# load models
try:
    coco_model = YOLO('yolov8n.pt')
    
    # Use os.path.join for cross-platform compatibility
    license_plate_model_path = r'c:\Users\acer\OneDrive\Desktop\MyCodes\DRDO_PROJECT\Automatic Number Plate Detection\automatic-number-plate-recognition-python-yolov8-main\models\LicensePlateDetector.pt'
    if not os.path.exists(license_plate_model_path):
        raise FileNotFoundError(f"License plate model not found at {license_plate_model_path}")
    
    license_plate_detector = YOLO(license_plate_model_path)
    print(f"Successfully loaded license plate detector from {license_plate_model_path}")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    exit(1)

# load video
video_path = r'C:\Users\acer\OneDrive\Desktop\MyCodes\DRDO_PROJECT\Automatic Number Plate Detection\automatic-number-plate-recognition-python-yolov8-main\video\1.mp4'
if not os.path.exists(video_path):
    print(f"Video file not found at {video_path}")
    exit(1)

cap = cv2.VideoCapture(video_path)

vehicles = [2, 3, 5, 7] # vehicle

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}
        # detect vehicles
        detections = coco_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        # track vehicles
        # Track vehicles
        detections_np = np.asarray(detections_)

        # Debug: Print shape of detections before passing to tracker
        print(f"Detections shape: {detections_np.shape}")

        # Ensure there are valid detections before passing to SORT
        if detections_np.shape[0] > 0 and detections_np.shape[1] >= 5:
            track_ids = mot_tracker.update(detections_np)
        else:
            track_ids = np.empty((0, 5))  # Create an empty array if no detections found
            print("No valid detections found, skipping SORT tracking.")


        # detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:

                # crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                # read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score}}

# write results
write_csv(results, r'C:\Users\acer\OneDrive\Desktop\MyCodes\DRDO_PROJECT\Automatic Number Plate Detection\automatic-number-plate-recognition-python-yolov8-main\test.csv')
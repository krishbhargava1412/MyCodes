import os
import cv2
from ultralytics import YOLO

# Define video paths


video_path = os.path.join(r'C:\Users\acer\OneDrive\Desktop\MyCodes\DRDO_PROJECT\Train_YOLOV8_Automatic_Number_Plate_Detection\code\video\1.mp4')

if not os.path.exists(video_path):
    print(f"Error: Video file not found at {video_path}")
    exit()

video_path_out = '{}_out.mp4'.format(video_path)

# Open video file
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

if not ret:
    print("Error: Unable to read video file.")
    cap.release()
    exit()

H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

# Load YOLO model
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model = YOLO(r'DRDO_PROJECT\Train_YOLOV8_Automatic_Number_Plate_Detection\code\models\best.pt')  # Ensure correct model path

threshold = 0.5

while ret:
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            label = model.names[int(class_id)].upper()  # Use model.names instead
            cv2.putText(frame, label, (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()

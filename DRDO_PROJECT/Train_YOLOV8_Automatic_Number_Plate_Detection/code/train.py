from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
results = model.train(data="DRDO_PROJECT\Train_YOLOV8_Automatic_Number_Plate_Detection\code\loco.yaml", epochs=5)  # train the model

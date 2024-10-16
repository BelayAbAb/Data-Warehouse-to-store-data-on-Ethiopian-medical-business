import logging
import os
from PIL import Image
from ultralytics import YOLO

# Set up logging
logging.basicConfig(
    filename='object_detection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load YOLOv8 model
def load_yolo_model(model_type='yolov8n.pt'):
    logging.info(f"Loading YOLOv8 model: {model_type}...")
    try:
        model = YOLO(model_type)
        logging.info("YOLOv8 model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load YOLOv8 model: {e}")
        raise

# Function to perform object detection on an image
def detect_objects(image_path, model):
    logging.info(f"Analyzing image: {image_path}")
    
    try:
        results = model(image_path)

        detection_results = []
        for *box, conf, cls in results.xyxy[0]:  # xyxy format
            detection_results.append({
                'class_id': int(cls.item()),
                'confidence': conf.item(),
                'box': [int(x) for x in box]
            })
        
        logging.info(f"Detection results: {detection_results}")
        return detection_results
    except Exception as e:
        logging.error(f"Failed to detect objects in {image_path}: {e}")
        return []

# Process all images in the specified directory
def process_images_in_directory(directory_path):
    model = load_yolo_model()

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(directory_path, filename)

            # Ensure the file is a valid image
            try:
                with Image.open(image_path) as img:
                    img.verify()  # Verify the image is valid
            except Exception as e:
                logging.error(f"Invalid image {filename}: {e}")
                continue
            
            detection_results = detect_objects(image_path, model)

            for result in detection_results:
                logging.info(f"Detected Object in {filename} - Class ID: {result['class_id']}, "
                             f"Confidence: {result['confidence']}, "
                             f"Bounding Box: {result['box']}")

if __name__ == "__main__":
    # Specify the directory containing the images
    directory_path = r'C:\Users\User\Desktop\10Acadamy\Week 7\Data Warehouse to store data on Ethiopian medical business\photos'
    process_images_in_directory(directory_path)

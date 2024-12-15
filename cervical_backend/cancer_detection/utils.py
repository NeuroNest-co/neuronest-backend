import numpy as np
import base64
import cv2
from detectron2.utils.visualizer import Visualizer

# Helper: Convert raw bytes to OpenCV image
def bytes_to_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# Helper: Convert OpenCV image to Base64 string
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# Helper: Process predictions and generate metrics/visualization
def process_predictions(image, fastapi_response):
    predictions = fastapi_response.get('predictions', [])
    metadata = fastapi_response.get('metadata', {})

    pred_classes = [pred['class_id'] for pred in predictions]
    scores = [pred['score'] for pred in predictions]
    boxes = [pred['bbox'] for pred in predictions]
    class_names = [pred['class_name'] for pred in predictions]

    # Calculate metrics for each class
    class_metrics = {}
    for idx, class_name in enumerate(class_names):
        if class_name not in class_metrics:
            class_metrics[class_name] = {'scores': [], 'boxes': []}
        class_metrics[class_name]['scores'].append(scores[idx])
        class_metrics[class_name]['boxes'].append(boxes[idx])

    # Prepare metrics and pie chart data
    table_data = []
    pie_chart_data = []
    for class_name, metrics in class_metrics.items():
        scores = metrics['scores']
        boxes = metrics['boxes']
        mean_score = np.mean(scores)
        max_score = np.max(scores)
        min_score = np.min(scores)
        count = len(scores)
        bbox_areas = [box[2] * box[3] for box in boxes]
        large_lesions = sum(1 for area in bbox_areas if area > 5000)
        small_lesions = count - large_lesions

        table_data.append({
            'class_name': class_name,
            'mean_score': mean_score,
            'max_score': max_score,
            'min_score': min_score,
            'count': count,
            'large_lesions': large_lesions,
            'small_lesions': small_lesions
        })

        pie_chart_data.append({'class': class_name, 'count': count})

    # Visualization
    visualizer = Visualizer(image[:, :, ::-1], metadata, scale=1.2)
    output_image = visualizer.draw_instance_predictions(predictions).get_image()

    return table_data, pie_chart_data, output_image

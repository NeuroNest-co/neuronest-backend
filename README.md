# Cervical Detection Backend

This Django-based backend is designed to perform cervical cancer lesion detection using a pre-trained model. The backend handles the prediction process, including classifying lesions, visualizing predictions, and calculating various metrics. The model is served via FastAPI, and the backend returns the image with bounding boxes, a table with detailed metrics, and a pie chart showing class distribution.

## Features

- **Prediction**: Classifies cervical lesions into categories (Lesion, Light, Mucus).
- **Visualization**: Visualizes the detected lesions and overlays bounding boxes on the image.
- **Metrics**: Returns statistical metrics including scores, bounding box sizes, and lesion distribution.
- **Pie Chart**: Provides a class distribution of detected lesions.

## How to Use

### 1. **Set Up the Project**

Clone the repository and set up the project in a Python environment:

```bash
git clone https://github.com/yourusername/cervical_detection_backend.git
cd cervical_detection_backend
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py runserver
http://127.0.0.1:8000/predict/

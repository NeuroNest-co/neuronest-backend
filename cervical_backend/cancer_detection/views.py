import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
import requests
import base64
import numpy as np
import cv2
from django.views.decorators.csrf import csrf_exempt

FASTAPI_URL = "https://jumarubea-model-visualization.hf.space"  # Backend URL for FastAPI

# Function to save images to the media folder
def save_image(image_base64, filename):
    image_data = base64.b64decode(image_base64)
    image_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)
    return filename

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            # Get the uploaded image
            image_file = request.FILES.get('file')
            if not image_file:
                return JsonResponse({'success': False, 'message': 'No image file provided'}, status=400)

            # Read the file into memory
            image_bytes = image_file.read()
            if not image_bytes:
                return JsonResponse({'success': False, 'message': 'Image file is empty'}, status=400)

            # Send raw image bytes to FastAPI for prediction
            files = {'file': image_bytes}
            response = requests.post(f"{FASTAPI_URL}/predict", files=files)

            if response.status_code == 200:
                try:
                    result = response.json()

                    # Extract visualization and metrics from the response
                    img_base64 = result.get('visualization', '')
                    metrics = result.get('metrics', {})

                    # Check if predictions are included
                    predictions = result.get('predictions', [])
                    if not predictions:
                        return JsonResponse({'success': False, 'message': 'No predictions in response'}, status=500)

                    # Process detailed information for table and pie chart
                    detailed_predictions = []
                    class_counts = {}
                    scores = {}

                    for prediction in predictions:
                        class_name = prediction.get('class_name')
                        score = prediction.get('score')
                        bbox = prediction.get('bbox')

                        # Store detailed predictions
                        detailed_predictions.append({
                            'class_name': class_name,
                            'score': score,
                            'bbox': bbox
                        })

                        # Count occurrences of each class for pie chart data
                        class_counts[class_name] = class_counts.get(class_name, 0) + 1

                        # Store scores for calculating table metrics
                        if class_name not in scores:
                            scores[class_name] = []
                        scores[class_name].append(score)

                    # Prepare metrics and pie chart data
                    table_data = []
                    pie_chart_data = []
                    for class_name, score_list in scores.items():
                        # Calculate metrics for each class
                        mean_score = np.mean(score_list)
                        max_score = np.max(score_list)
                        min_score = np.min(score_list)
                        count = len(score_list)

                        # Add data to the table
                        table_data.append({
                            'class_name': class_name,
                            'mean_score': mean_score,
                            'max_score': max_score,
                            'min_score': min_score,
                            'count': count
                        })

                        # Prepare data for the pie chart
                        pie_chart_data.append({'class': class_name, 'count': count})

                    # Save the original and predicted images to the media folder
                    original_image_filename = "original_image.jpg"
                    predicted_image_filename = "predicted_image.jpg"

                    # Save original image (as base64) and predicted image
                    original_image_url = save_image(base64.b64encode(image_bytes).decode('utf-8'), original_image_filename)
                    predicted_image_url = save_image(img_base64, predicted_image_filename)

                    # Return a JSON response with URLs of the images
                    return JsonResponse({
                        'success': True,
                        'message': 'Prediction successful',
                        'data': {
                            'original_image_url': f"/media/{original_image_filename}",
                            'predicted_image_url': f"/media/{predicted_image_filename}",
                            'metrics': table_data,
                            'pie_chart_data': pie_chart_data
                        }
                    })

                except Exception as e:
                    return JsonResponse({'success': False, 'message': f"Error parsing response: {str(e)}"}, status=500)
            else:
                return JsonResponse({
                    'success': False,
                    'message': f"Error from FastAPI: {response.status_code} {response.text}"
                }, status=response.status_code)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Internal error: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

import os
import base64
import requests
import numpy as np
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PatientForm
from .models import apiResponse

FASTAPI_URL = "https://jumarubea-model-visualization.hf.space"

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
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save()

                patient_id = f'P-{datetime.datetime.now().strftime("%Y-%m-%d")}-{patient.patientId:03}' 

                # Now handle the image upload and send it for prediction
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
                    result = response.json()

                    # Extract visualization and predictions
                    img_base64 = result.get('visualization', '')
                    predictions = result.get('predictions', [])
                    if not predictions:
                        return JsonResponse({'success': False, 'message': 'No predictions in response'}, status=500)

                    # Process detailed information for table and pie chart
                    table_data = []
                    pie_chart_data = []
                    class_counts = {}
                    scores = {}

                    for prediction in predictions:
                        class_name = prediction.get('class_name')
                        score = prediction.get('score')

                        # Count occurrences of each class for pie chart
                        class_counts[class_name] = class_counts.get(class_name, 0) + 1

                        # Store scores for metrics calculation
                        if class_name not in scores:
                            scores[class_name] = []
                        scores[class_name].append(score)

                    for class_name, score_list in scores.items():
                        mean_score = np.mean(score_list)
                        max_score = np.max(score_list)
                        min_score = np.min(score_list)
                        count = len(score_list)

                        table_data.append({
                            'class_name': class_name,
                            'mean_score': mean_score,
                            'max_score': max_score,
                            'min_score': min_score,
                            'count': count
                        })

                        pie_chart_data.append({'class': class_name, 'count': count})

                    # Save images
                    original_image_filename = f"{patient_id}_original_image.jpg"
                    predicted_image_filename = f"{patient_id}_predicted_image.jpg"

                    original_image_url = save_image(base64.b64encode(image_bytes).decode('utf-8'), original_image_filename)
                    predicted_image_url = save_image(img_base64, predicted_image_filename)

                    # Prepare response
                    response_data = {
                        'success': True,
                        'message': 'Prediction successful',
                        'data': {
                            'patientId': patient_id,
                            'age': patient.age,
                            'doctor_comment': patient.doctor_comment,
                            'date': patient.date.strftime('%Y-%m-%d %H:%M:%S'),
                            'original_image_url': f"/media/{original_image_filename}",
                            'predicted_image_url': f"/media/{predicted_image_filename}",
                            'metrics': table_data,
                            'pie_chart_data': pie_chart_data
                        }
                    }

                    # Save response to the database
                    apiResponse.objects.create(
                        patient=patient,
                        response_data=result,
                        full_response=response_data
                    )

                    return JsonResponse(response_data)

                else:
                    return JsonResponse({
                        'success': False,
                        'message': f"Error from FastAPI: {response.status_code} {response.text}"
                    }, status=response.status_code)

            else:
                return JsonResponse({'success': False, 'message': 'Invalid patient details'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Internal error: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def view_all_data(request):
    if request.method == 'GET':
        all_predictions = apiResponse.objects.all()

        data = []
        for prediction in all_predictions:
            full_response = prediction.full_response or {}
            patient_id = f'P-{prediction.patient.date.strftime("%Y-%m-%d")}-{prediction.patient.patientId:03}'

            data.append({
                'patientId': patient_id,
                'age': prediction.patient.age,
                'doctor_comment': prediction.patient.doctor_comment,
                'date': prediction.patient.date.strftime('%Y-%m-%d %H:%M:%S'),
                'metrics': full_response.get('data', {}).get('metrics', []),
                'pie_chart_data': full_response.get('data', {}).get('pie_chart_data', []),
            })

        return JsonResponse({'success': True, 'data': data})

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

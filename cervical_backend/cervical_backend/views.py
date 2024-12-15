from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the cervical cancer detection model API!")

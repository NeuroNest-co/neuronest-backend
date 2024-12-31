from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('all_data/', views.view_all_data, name='all_data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
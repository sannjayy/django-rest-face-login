from django.urls import path
from .views import ImageRecognitionAWSView

urlpatterns = [
    path('auth', ImageRecognitionAWSView.as_view(), name="aws_face_login"),
]
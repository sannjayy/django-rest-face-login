from django.urls import path
from .views import ImageRecognitionView

urlpatterns = [
    path('auth', ImageRecognitionView.as_view(), name="aws_face_login"),
]
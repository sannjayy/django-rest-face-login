from django.urls import path
from .views import ImageRecognitionView

urlpatterns = [
    path('login/', ImageRecognitionView.as_view(), name="face_login"),
]
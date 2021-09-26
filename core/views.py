from rest_framework.views import APIView
from rest_framework import generics, status, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageRecognitionSerializer
from .utils import image_comparison
from .models import User, LoginAttempt
from django.shortcuts import get_object_or_404
# Create your views here.
class ImageRecognitionView(generics.GenericAPIView):
    serializer_class = ImageRecognitionSerializer

    # parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        username, image, image_url = serializer.data.values()
        user = get_object_or_404(User, username=username)
        print(user.screen_lock_img_url)
        print(username)
        print(image_url)
        img_comp = image_comparison(str(user.screen_lock_img_url), str(image_url))
        # print(image_comparison('../media/security_images/Photo-2.jpeg', '../media/security_images/Photo-2.jpeg'))
        # file_serializer.save()
        if img_comp:
            response = {
                'response':'success',
                'nam' : user.first_name + ' ' + user.last_name,
                'email' : user.email,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({'response':'user not found'}, status=status.HTTP_400_BAD_REQUEST)

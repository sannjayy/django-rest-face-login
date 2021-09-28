from rest_framework.views import APIView
from rest_framework import generics, status, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageRecognitionSerializer
from .models import User, LoginAttempt
from django.shortcuts import get_object_or_404
import boto3
import os
from django.conf import settings




# Create your views here.
'''
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

'''
class ImageRecognitionAWSView(generics.GenericAPIView):
    serializer_class = ImageRecognitionSerializer
    # parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        username, image, image_url = serializer.data.values()
        user = get_object_or_404(User, username=username)
        print('Image : ', image)
        if not image:
            return Response({'response':'Image not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        aws_access_key_id  = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key  = settings.AWS_SECRET_ACCESS_KEY
        region_name = settings.AWS_REGION_NAME

        client = boto3.client('rekognition', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        
        DB_IMG_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media/security_images/'))
        UPLOAD_IMG_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media/uploaded_temp_images/'))
        
        image_db = os.path.join(DB_IMG_FOLDER,  user.image_filename)
        image_upload = os.path.join(UPLOAD_IMG_FOLDER,  image_url)

        with open(image_db, 'rb') as image_db_source_image:
            image_db_source_bytes = image_db_source_image.read()

        with open(image_upload, 'rb') as image_upload_source_image:
            image_upload_source_bytes = image_upload_source_image.read()
            
# response = client.detect_labels(
#     Image={
#         'Bytes': image_upload,
#     },
#     MaxLabels=2
# )
        response = client.compare_faces(
            SourceImage={
                'Bytes': image_db_source_bytes,
            },
            TargetImage={
                'Bytes': image_upload_source_bytes,
            },
            # SimilarityThreshold=50,
            QualityFilter = 'AUTO'
        )
        face_match = response['FaceMatches']
        if face_match:
            similarity = face_match[0].get('Similarity')
            confidence = face_match[0].get('Face').get('Confidence')
            success_response = {                
                'user': {
                    'name' : user.first_name + ' ' + user.last_name,
                    'username' : user.username,
                    'email' : user.email,
                },
                'similarity':round(similarity, 4),
                'confidence':round(confidence, 4),
                'response':'success'
            }
            
            return Response(success_response, status=status.HTTP_202_ACCEPTED)

        return Response({'response':'authentication failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)
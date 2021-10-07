from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import boto3, os
from django.conf import settings
# Custom Imports
from .serializers import ImageRecognitionSerializer
from .models import User



# Image Recognition View
class ImageRecognitionView(generics.GenericAPIView):
    """[Image Recognition Function]

    Args:
        username (Char): [Username of Account]
        image (ImageField): [Captured Image (Base64 or Image Path) of the User]

    Returns:
        [user]: [user object]
        [similarity]: [Image similarity]
        [confidence]: [Image matching confidence]
        [response]: [success / failed]
    """
    serializer_class = ImageRecognitionSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_attempt_data = serializer.save()
        username, image, image_url = serializer.data.values()

        # Try to find the user.
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            login_attempt_data.delete() # If unauthenticated user data will be deleted.
            return Response({'response':'User credentials not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not image:
            return Response({'response':'Image not found'}, status=status.HTTP_400_BAD_REQUEST)

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

        # Try to compare the user image.
        try:
            response = client.compare_faces(
                SourceImage={
                    'Bytes': image_db_source_bytes,
                },
                TargetImage={
                    'Bytes': image_upload_source_bytes,
                },
                SimilarityThreshold=80,
                QualityFilter = 'HIGH'
            )                
            face_match = response['FaceMatches']  

        except:
            login_attempt_data.delete() # Also If unauthenticated user data will be deleted.
            return Response({'response':'User image mismatch'}, status=status.HTTP_406_NOT_ACCEPTABLE)  

        if face_match:
            """[Your Login (Authentication) Logic Place in Here]
            Example : user = authenticate(username='john', password='secret') 
            """

            similarity = face_match[0].get('Similarity')
            confidence = face_match[0].get('Face').get('Confidence')
            success_response = {                
                'user': {
                    'name' : user.first_name + ' ' + user.last_name,
                    'username' : user.username,
                    'email' : user.email,
                },
                'similarity': round(similarity, 4),
                'confidence': round(confidence, 4),
                'response':'success'
            }

        return Response(success_response, status=status.HTTP_202_ACCEPTED)




# ==============================================================
# With CV2 Method.
'''
class ImageRecognitionView(generics.GenericAPIView):
    """[Alternative Method]
    If you want to use opencv then you can use this code.
    """
    serializer_class = ImageRecognitionSerializer

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
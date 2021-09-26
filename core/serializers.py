from rest_framework import serializers
from .models import User, LoginAttempt

class ImageRecognitionSerializer(serializers.HyperlinkedModelSerializer):
    # user_image = serializers.ImageField()
    # photo_url = serializers.SerializerMethodField()
    # photo_url = serializers.SerializerMethodField()
    class Meta:
        model = LoginAttempt
        fields= ('username', 'image', 'image_url')
    

    # def get_photo_url(self, obj):
    #         request = self.context.get('request')
          
    #         photo_url = obj.image.url
    #         return request.build_absolute_uri(photo_url)
           
    # def validate(self, attrs):
    #     image = attrs.get('image', '')
    #     print(image)
    # def get_photo_url(self, obj):
    #     request = self.context.get('request')
    #     print(obj['image'].url)
    #     # photo_url = obj.image.url
    #     # return request.build_absolute_uri(photo_url)
    #     pass

    # def create(self, validated_data):
    #     image = validated_data['image']
    #     print(image)
    #     return True
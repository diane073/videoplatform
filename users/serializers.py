from django.core.mail import EmailMessage
from project import settings
from django.template.loader import render_to_string
from rest_framework import serializers
from users.models import User, Tag
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from users.tokens import account_activation_token

from drf_extra_fields.fields import Base64ImageField

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']
    
    def __str__(self):
        return self.name


# 회원가입
class UserSerializer(serializers.ModelSerializer):
    # profile_image = Base64ImageField(required=False)
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'profile_image', 'bio', 'joined_at', 'tags', 'followings']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = False
        password = user.password
        user.set_password(password)
        user.save()

        message = render_to_string('email_signup_message.html', {
            'user':user,
            'domain':'localhost:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        subject = '회원가입 인증 메일입니다.'
        to = [user.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

class UserViewSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    followers = UserSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'profile_image', 'bio', 'joined_at', 'tags', 'followers']

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
    



from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    ROLES_CHOICES=[
        ('reception','RECEPTION'),
        ('waiter','WAITER')

    ]
    roles= serializers.ChoiceField(choices=ROLES_CHOICES)
    email = serializers.EmailField(max_length=100)
    password= serializers.CharField(max_length=100,write_only=True)
    confirm_password = serializers.CharField(max_length=100, write_only=True)

    def validate_email(self,value):
        if User.objects.filter(email= value).exists():
            raise serializers.ValidationError("email already exist....!!!!!")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password':'password doesnot matched..!!'
            })
        return super().validate(attrs)
    
    def create(self, validated_data,*args, **kwargs):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            roles=validated_data['roles']

        )
        return user
        
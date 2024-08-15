from django.shortcuts import render
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterUserSerializer, UserLoginSerializer
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models    import Token
from rest_framework.permissions import IsAdminUser
# Create your views here.

User = get_user_model()


class UserViewsets(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


    # i am overriding the default create method so that i can check only the super_user has the ability to add waiter or reception
    def create(self,request,*args,**kwargs):
        #check if the requesting user  is a superuser
        if not request.user.is_superuser:
            return Response(
                {
                    "detail":"you do not have permissions to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request,*args,**kwargs)



    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(f"email or usernmae is : {serializer.validated_data['email']}")
        # print(f"password is : {serializer.validated_data['password']}")


        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        # print(f"user   :{user}")

        if user is not None:
            token,_= Token.objects.get_or_create(user=user)

            return Response({
                'token':token.key,
                'user': serializer.data,
                "message": "user logged in successfully....!!!!!"
            },
                status=status.HTTP_200_OK

            )

        else:
             return Response({
                'errors': 'email or password doesnot matched....!!!!!!'
            },
                status=status.HTTP_401_UNAUTHORIZED
            )

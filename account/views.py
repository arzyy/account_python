from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializers import LoginSerializer, RegisterSerializer, UserDetailSerializer, UserListSerializer
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.

class UserRegistration(APIView):#
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=200)
        
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer#{ "token": "88c346eaf668b6aceddc90075d9e8c214c9319ed"}

    def post(self, request):
        serializer = self.serializer_class(data = request.data, 
                                           context = {'request':request })
        serializer.is_valid(raise_exception=True)                                       
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user = user)
        # token,_ = Token.objects.get_or_create(user = user)

        response_data = {
            'token': token.key, 
            'username': user.username, 
            'id': user.id
        }
        print(response_data, '!!!!!')
        return Response(response_data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы  ввышли')
    

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    permission_classes =[IsAdminUser]

#wed 12.2023
class CustomViewSet(mixins.RetrieveModelMixin, 
                    mixins.ListModelMixin,
                    GenericViewSet):
    pass

class UserViewSet(CustomViewSet):
    queryset = User.objects.all()


    def get_serializer_class(self):
        if self.action == 'retrieve':#если action равнятеся то он будет наследуется от Retrieve
            return UserDetailSerializer
        return UserListSerializer
    

    def get_permissions(self):
        if self.request.method == 'retrieve':
            return IsAdminUser(), #or [IsAdminUser()]
        return [IsAuthenticated()]

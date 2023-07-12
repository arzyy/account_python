from imaplib import _Authenticator
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    password = serializers.CharField(min_length=8, write_only=True, required = True)
    password_confirmation  = serializers.CharField(min_length=8, write_only = True, required = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')

    def validate(self, attrs):# сюда прихoдит то что fields
        print(attrs, "!!!!")
        password_confirmation= attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError('Пароли не совпадают')
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError('Имя должно начинаться с большой буквы')
        return attrs


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        print(data, "££££££")
        request = self.context.get('request')
        username = data.get('username') 
        password = data.get('password') 
        if username and password:
            user = authenticate(username=username, 
                                password = password, 
                                request = request)
            if not user:
                raise serializers.ValidationError(
                    'Неверный юзернейм или пароль'
                )
        else:
            raise serializers.ValidationError(
                'Username и password обязательны к заполнению'
            )   
        data['user']= user
        return data#мы используем в вью validation
    
    def validate_username(self, username):
        print(username)
        if not User.objects.filter(username = username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username нe найден'
            )
        return username
    



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


    
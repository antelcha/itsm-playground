from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['department', 'role', 'employee_id']

class UserSerializer(serializers.ModelSerializer):
    usermodel = UserModelSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
'usermodel']
        read_only_fields = ['id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    usermodel = UserModelSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
'password', 'usermodel']

    def create(self, validated_data):
        usermodel_data = validated_data.pop('usermodel')
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        UserModel.objects.create(user=user, **usermodel_data)
        return user

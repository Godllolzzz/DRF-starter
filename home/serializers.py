from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({
                'error': 'age must be >= 18'
            })
        
        for character in data['name']:
            # print(character)
            if character.isdigit():
                raise serializers.ValidationError({
                    'error': 'character must not contain any number'
                })
        
        return data
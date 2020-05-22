from rest_framework import serializers

from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'auth_token',
        )

        extra_kwargs = {
            'password':{
                'write_only':True
            },
            'is_active':{
                'read_only':True
            },
            'auth_token':{
                'read_only':True
            }
        }

    def create(self, validated_data):
        """
        Creates New User. 
        Note: is_active property is always set per default.
        Remove is_active from extra_kwargs by setting it at this method.
        """
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_active',
        )

        extra_kwargs = {
            'is_active':{
                'read_only':True
            },
            'first_name':{
                'required':False
            },
            'last_name':{
                'required':False
            },
            'email':{
                'required':False
            },
        }
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.email = validated_data.get(
            'email',
            instance.email
        )
        instance.save()
        return instance


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password',
            'email'
        )
        extra_kwargs = {
            'password':{
                'write_only':True,
                'required':False
            },
            'email':{
                'required':False,
            },
            'first_name':{
                'read_only':True,
            },
            'last_name':{
                'read_only':True,
            },
        }

    def update(self, instance, validated_data):
        """
        Handles just PW Reset
        """
        instance.email = validated_data.get(
            'email',
            instance.email
        )

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

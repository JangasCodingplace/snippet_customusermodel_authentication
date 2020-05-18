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
        return User.objects.create(**validated_data)
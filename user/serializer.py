from rest_framework import serializers
from user.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'

        def create(self, validated_data):
            user = CustomUser(self, **validated_data)
            user.is_active = True
            if senha := validated_data.pop('senha', None):
                user.set_password(senha)
            user.save()
            return user
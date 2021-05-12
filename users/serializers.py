from rest_framework.serializers import ModelSerializer, CharField, ValidationError, SerializerMethodField
from .models import CustomUser, ConnectedUsers


class CustomUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'sex', 'birth_date', 'password')

    def validate_password(self, value):
        if self.instance and value != self.instance.password:
            raise ValidationError("'password' should be changed using endpoint - '/api/auth/users/set_password/'.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ConnectedUserSerializer(ModelSerializer):
    username = SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    class Meta:
        model = ConnectedUsers
        fields = ['username', 'last_joined']

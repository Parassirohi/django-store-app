from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

# from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # model = User
        # to inherit everything in a Meta class in this class,
        # we can use BaseUserCreateSerializer.Meta
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        # now register it to our settings module


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

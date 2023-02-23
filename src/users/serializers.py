from rest_framework import serializers

from src.users.models import User,AdminManager,AdminManagerEmployer
from src.common.serializers import ThumbnailerJSONSerializer


class UserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_picture',
        )
        read_only_fields = ('username',)


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')
    tokens = serializers.SerializerMethodField()
    manager_id = serializers.IntegerField(allow_null=True,required=False)


    def get_tokens(self, user):
        return user.get_tokens()

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        manager_id = validated_data['manager_id']

        del validated_data['manager_id']
        validated_data['is_company']=False
        user = User.objects.create_user(**validated_data)
        print(user)

        if validated_data['is_manager']:
            AdminManager.objects.create(
                admin=self.context['request'].user, 
                manager=user
            )

        if validated_data['is_employer'] :
            AdminManagerEmployer.objects.create(
                admin=self.context['request'].user,
                manager_id=manager_id,
                employer=user
            )

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'manager_id',
            'is_manager',
            'is_employer',
            'email',
            'tokens',
            'profile_picture',
        )
        read_only_fields = ('tokens',)
        extra_kwargs = {'password': {'write_only': True}}

from rest_framework import serializers

from felicinema.apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'password', 'phone',
            'address', 'gender', '_birth_year',
            'first_name', 'last_name',
            'email',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

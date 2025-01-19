from rest_framework import serializers
from user.models import User


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "lat",
            "long",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email_query = User.objects.filter(email=validated_data["email"])
        if self.instance:
            email_query = email_query.exclude(id=self.instance.id)
        if email_query.exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )

        return validated_data

    def create(self, validated_data):
        validated_data["user_type"] = User.UserTypes.DRIVER
        validated_data["username"] = validated_data["email"]
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(validated_data["password"])
        return super().update(instance, validated_data)

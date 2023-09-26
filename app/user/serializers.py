from django.contrib.auth import authenticate
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        emails = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=emails,
            password=password,
        )
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user

        return attrs

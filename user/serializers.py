from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password"),
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return USER.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a user, setting the password correctly."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

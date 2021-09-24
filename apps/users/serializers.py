import re
from rest_framework import serializers

from libs.utils.helpers import check_unique_value
from .models import User
from .error_messages import errors


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    first_name = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["first_name"]["required"],
            "blank": errors["first_name"]["blank"],
        },
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["last_name"]["required"],
            "blank": errors["last_name"]["blank"],
        },
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": errors["email"]["required"],
            "blank": errors["email"]["blank"],
            "invalid": errors["email"]["invalid"],
        },
    )
    phone_number = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["phone_number"]["required"],
            "blank": errors["phone_number"]["blank"],
        },
    )
    id_number = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["id_number"]["required"],
            "blank": errors["id_number"]["blank"],
        },
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "id_number",
            "profile_picture",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, email):
        norm_email = email.lower()
        check_unique_value(User, "email", email, errors)

        return norm_email

    def validate_phone_number(self, phone_number):
        phone_number_regex = r"^\+(?:[0-9] ?){6,14}[0-9]$"

        if not re.match(phone_number_regex, phone_number):
            raise serializers.ValidationError(errors["phone_number"]["invalid"])

        check_unique_value(User, "phone_number", phone_number, errors)

        return phone_number

    def validate_id_number(self, id_number):
        check_unique_value(User, "id_number", id_number, errors)

        return id_number

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

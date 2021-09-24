import pytest

from apps.users.models import User
from apps.users.error_messages import errors


@pytest.mark.django_db
class TestUserModel:
    """Test user model"""

    new_user = {
        "first_name": "Test",
        "last_name": "USer",
        "email": "test.user@app.com",
        "phone_number": "+250780000000",
        "id_number": "1111111111",
    }

    admin_user = {
        "first_name": "Admin",
        "last_name": "USer",
        "email": "admin.user@app.com",
        "password": "TestPassword",
        "phone_number": "+250780000000",
        "id_number": "1111111111",
    }

    def test_user_str(self, new_user):
        email = new_user.__str__()

        assert email == f"{new_user.email}"

    def test_user_email_is_normalized(self, new_user):
        email = "user@APP.COM"

        assert new_user.email == email.lower()

    def test_create_user_succeeds(self):
        user = User.objects.create_user(**self.new_user)

        assert user.email == self.new_user["email"]
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_admin == False
        assert user.is_superuser == False

    def test_create_user_without_email_fails(self):
        with pytest.raises(ValueError) as error:
            self.new_user["email"] = ""
            User.objects.create_user(**self.new_user)

            assert str(error.value) == errors["email"]["required"]

    def test_create_user_with_invalid_email_fails(self):
        with pytest.raises(ValueError) as error:
            self.new_user["email"] = "user"
            User.objects.create_user(**self.new_user)

            assert str(error.value) == errors["email"]["invalid"]

    def test_create_super_user_succeeds(self):
        user = User.objects.create_superuser(**self.admin_user)

        assert user.email == self.admin_user["email"]
        assert user.is_active == True
        assert user.is_staff == True
        assert user.is_admin == True
        assert user.is_superuser == True

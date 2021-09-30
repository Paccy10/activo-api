import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group

from apps.users.models import User


@pytest.mark.django_db
@pytest.fixture
def new_user():
    """New user fixture"""

    return User.objects.create_user(
        first_name="user",
        last_name="new",
        email="user@app.com",
        phone_number="+250780000000",
        id_number="111111111111",
        password="password",
    )


@pytest.mark.django_db
@pytest.fixture
def new_group():
    """New user fixture"""

    return Group.objects.create(name="admins")


@pytest.fixture
def auth(new_user):
    token = RefreshToken.for_user(new_user)

    return {"token": str(token.access_token), "user": new_user}

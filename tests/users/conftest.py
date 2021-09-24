import pytest

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
    )

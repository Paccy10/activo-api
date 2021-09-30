import pytest
import json
from django.contrib.auth.models import Permission

from tests.constants import JSON_CONTENT_TYPE
from apps.users.error_messages import errors
from apps.users.models import User


@pytest.mark.django_db
class TestUpdateUserEndpoint:
    """Test update user endpoint"""

    url = "/users/"
    data = {
        "first_name": "Test",
        "last_name": "Edit",
        "email": "test.edit@app.com",
        "phone_number": "+250780000001",
        "id_number": "1111111111",
    }

    def test_update_user_with_unauthorized_user_fails(self, api_client, new_user):
        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_update_user_without_add_permission_fails(self, api_client, auth, new_user):
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_update_user_succeeds(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 200
        assert response.json()["email"] == self.data["email"]
        assert response.json()["email"] != new_user.email

    def test_update_user_with_unexisted_id_succeeds(self, api_client, auth):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}10/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Not found."

    def test_update_user_with_blank_first_name_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["first_name"] = ""
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["blank"]]

    def test_update_user_with_blank_last_name_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["last_name"] = ""
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["blank"]]

    def test_update_user_with_blank_email_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["email"] = ""
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["blank"]]

    def test_update_user_with_taken_email_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        user = User.objects.create_user(email="another.user@app.com")
        data = self.data.copy()
        data["email"] = user.email
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["unique"]]

    def test_update_user_with_blank_id_number_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["id_number"] = ""
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["blank"]]

    def test_update_user_with_taken_id_number_fails(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        user = User.objects.create_user(
            email="another.user@app.com", id_number="0101010101"
        )
        data = self.data.copy()
        data["id_number"] = user.id_number
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["unique"]]

    def test_update_user_with_blank_phone_number_fails(
        self, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["phone_number"] = ""
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["blank"]]

    def test_update_user_with_taken_phone_number_fails(
        self, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="change_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        user = User.objects.create_user(
            email="another.user@app.com", phone_number="+250788888888"
        )
        data = self.data.copy()
        data["phone_number"] = user.phone_number
        data = json.dumps(data)
        response = api_client.patch(
            f"{self.url}{new_user.id}/", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["unique"]]


@pytest.mark.django_db
class TestDeleteUserEndpoint:
    """Test delete user endpoint"""

    url = "/users/"

    def test_delete_user_with_unauthorized_user_fails(self, api_client, new_user):
        response = api_client.delete(f"{self.url}{new_user.id}/")

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_delete_user_without_add_permission_fails(self, api_client, auth, new_user):
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.delete(f"{self.url}{new_user.id}/")

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_delete_user_succeeds(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="delete_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.delete(f"{self.url}{new_user.id}/")

        assert response.status_code == 204

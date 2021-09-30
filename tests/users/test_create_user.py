import pytest
import json
import django_rq
from unittest.mock import MagicMock
from django.contrib.auth.models import Permission

from apps.users.error_messages import errors
from tests.constants import JSON_CONTENT_TYPE


@pytest.mark.django_db
class TestCreateUserEndpoint:
    """Test create user endpoint"""

    url = "/users/"
    data = {
        "first_name": "Test",
        "last_name": "USer",
        "email": "test.user@app.com",
        "phone_number": "+250780000001",
        "id_number": "1111111111",
    }

    def test_create_user_with_unauthorized_user_fails(self, api_client):
        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_create_user_without_add_permission_fails(self, api_client, auth):
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_create_user_succeeds(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        django_rq.enqueue = MagicMock(return_value=None)

        data = self.data.copy()
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 201
        assert response.json()["email"] == self.data["email"]
        assert response.json()["should_set_password"] is True
        assert "initial_password" in response.json()

    def test_create_user_without_email_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data.pop("email")
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["required"]]

    def test_create_user_with_blank_email_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["email"] = ""
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["blank"]]

    def test_create_user_with_invalid_email_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["email"] = "email"
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["invalid"]]

    def test_create_user_with_taken_email_fails(
        self, new_group, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["email"] = new_user.email
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["unique"]]

    def test_create_user_without_first_name_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data.pop("first_name")
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["required"]]

    def test_create_user_with_blank_first_name_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["first_name"] = ""
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["blank"]]

    def test_create_user_without_last_name_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data.pop("last_name")
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["required"]]

    def test_create_user_with_blank_last_name_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["last_name"] = ""
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["blank"]]

    def test_create_user_without_phone_number_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data.pop("phone_number")
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["required"]]

    def test_create_user_with_blank_phone_number_fails(
        self, new_group, api_client, auth
    ):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["phone_number"] = ""
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["blank"]]

    def test_create_user_with_invalid_phone_number_fails(
        self, new_group, api_client, auth
    ):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["phone_number"] = "hello"
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["invalid"]]

    def test_create_user_with_taken_phone_number_fails(
        self, new_group, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["phone_number"] = new_user.phone_number
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["unique"]]

    def test_create_user_without_id_number_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data.pop("id_number")
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["required"]]

    def test_create_user_with_blank_id_number_fails(self, new_group, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["id_number"] = ""
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["blank"]]

    def test_create_user_with_taken_id_number_fails(
        self, new_group, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["id_number"] = new_user.id_number
        data["groups"] = [new_group.id]
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["unique"]]

    def test_create_user_without_groups_fails(self, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["groups"] == ["This field is required."]

    def test_create_user_with_invalid_groups_fails(self, api_client, auth):
        permission = Permission.objects.get(codename="add_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        data = self.data.copy()
        data["groups"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["groups"] == [
            'Expected a list of items but got type "str".'
        ]

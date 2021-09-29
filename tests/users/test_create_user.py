import pytest
import django_rq
from unittest.mock import MagicMock

from apps.users.error_messages import errors


@pytest.mark.django_db
class TestCreateUserEndpoint:
    """Test create user endpoint"""

    url = "/users/"
    data = {
        "first_name": "Test",
        "last_name": "USer",
        "email": "test.user@app.com",
        "phone_number": "+250780000000",
        "id_number": "1111111111",
    }

    def test_create_user_succeeds(self, api_client):
        
        django_rq.enqueue = MagicMock(return_value=None)
        response = api_client.post(self.url, self.data)

        assert response.status_code == 201
        assert response.json()["email"] == self.data["email"]
        assert "initial_password" in response.json()

    def test_create_user_without_email_fails(self, api_client):

        self.data.pop("email")
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["required"]]

    def test_create_user_with_blank_email_fails(self, api_client):

        self.data["email"] = ""
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["blank"]]

    def test_create_user_with_invalid_email_fails(self, api_client):

        self.data["email"] = "email"
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["invalid"]]

    def test_create_user_with_taken_email_fails(self, api_client, new_user):

        self.data["email"] = new_user.email
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["unique"]]

    def test_create_user_without_first_name_fails(self, api_client):

        self.data.pop("first_name")
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["required"]]

    def test_create_user_with_blank_first_name_fails(self, api_client):

        self.data["first_name"] = ""
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["blank"]]

    def test_create_user_without_last_name_fails(self, api_client):

        self.data.pop("last_name")
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["required"]]

    def test_create_user_with_blank_last_name_fails(self, api_client):

        self.data["last_name"] = ""
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["blank"]]

    def test_create_user_without_phone_number_fails(self, api_client):

        self.data.pop("phone_number")
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["required"]]

    def test_create_user_with_blank_phone_number_fails(self, api_client):

        self.data["phone_number"] = ""
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["blank"]]

    def test_create_user_with_invalid_phone_number_fails(self, api_client):

        self.data["phone_number"] = "hello"
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["invalid"]]

    def test_create_user_with_taken_phone_number_fails(self, api_client, new_user):

        self.data["phone_number"] = new_user.phone_number
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["phone_number"] == [errors["phone_number"]["unique"]]

    def test_create_user_without_id_number_fails(self, api_client):

        self.data.pop("id_number")
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["required"]]

    def test_create_user_with_blank_id_number_fails(self, api_client):

        self.data["id_number"] = ""
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["blank"]]

    def test_create_user_with_taken_id_number_fails(self, api_client, new_user):

        self.data["id_number"] = new_user.id_number
        response = api_client.post(self.url, self.data)

        assert response.status_code == 400
        assert response.json()["id_number"] == [errors["id_number"]["unique"]]

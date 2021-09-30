import pytest
import json

from tests.constants import JSON_CONTENT_TYPE


@pytest.mark.django_db
class TestLoginEndpoint:

    url = "/users/login/"

    def test_login_succeeds(self, api_client, new_user):
        data = json.dumps({"email": new_user.email, "password": "password"})
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json()["user"]["email"] == new_user.email

    def test_login_without_email_fails(self, api_client):
        data = json.dumps({"password": "password"})
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == ["This field is required."]

    def test_login_without_password_fails(self, api_client, new_user):
        data = json.dumps({"email": new_user.email})
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["password"] == ["This field is required."]

    def test_login_with_invalid_credentials_fails(self, api_client, new_user):
        data = json.dumps({"email": new_user.email, "password": "wrong_password"})
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "No active account found with the given credentials"
        )

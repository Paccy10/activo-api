import pytest
from django.contrib.auth.models import Permission


@pytest.mark.django_db
class TestGetUsersEndpoint:
    """Test Get users endpoint"""

    url = "/users/"

    def test_get_users_with_unauthorized_user_fails(self, api_client):
        response = api_client.get(self.url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_users_without_add_permission_fails(self, api_client, auth):
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.get(self.url)

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_get_users_succeeds(self, api_client, auth):
        permission = Permission.objects.get(codename="view_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.get(self.url)

        assert response.status_code == 200
        assert len(response.json()) == 1


@pytest.mark.django_db
class TestGetUserEndpoint:
    """Test Get user endpoint"""

    url = "/users/"

    def test_get_single_user_with_unauthorized_user_fails(self, api_client, new_user):
        response = api_client.get(f"{self.url}{new_user.id}/")

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_single_user_without_add_permission_fails(
        self, api_client, auth, new_user
    ):
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.get(f"{self.url}{new_user.id}/")

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_get_single_user_succeeds(self, api_client, auth, new_user):
        permission = Permission.objects.get(codename="view_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.get(f"{self.url}{new_user.id}/")

        assert response.status_code == 200
        assert response.json()["email"] == new_user.email

    def test_get_single_user_with_unexisted_id_succeeds(
        self, api_client, auth, new_user
    ):
        permission = Permission.objects.get(codename="view_user")
        auth["user"].user_permissions.add(permission)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth['token']}")

        response = api_client.get(f"{self.url}10/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not found."

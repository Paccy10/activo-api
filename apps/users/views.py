from rest_framework import mixins, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django_rq import enqueue
from django.template.loader import get_template

from .models import User, generate_password
from .serializers import (
    UserSerializer,
    UserDisplaySerializer,
    CustomTokenObtainPairSerializer,
)
from .permissions import ModelPermissions
from libs.utils.helpers import send_email


class UsersView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    """User viewsets

    post:
        Create a new user

    get:
        Get users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ModelPermissions]
    search_fields = [
        "first_name",
        "lastname",
        "email",
        "phone_number",
        "id_number",
        "groups__name",
    ]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        # Generate password
        user_id = response.data["id"]
        user = User.objects.get(id=user_id)
        initial_password = generate_password()
        user.set_password(initial_password)
        user.should_set_password = True
        user.save()

        # Send email
        subject = "New Account"
        message = get_template("new_account.html").render(
            {"user": user, "initial_password": initial_password}
        )
        enqueue(send_email, subject, message, [user.email])

        response.data["initial_password"] = initial_password
        response.data["should_set_password"] = user.should_set_password
        return response

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserDisplaySerializer

        return self.list(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom TokenObtainPairView"""

    serializer_class = CustomTokenObtainPairSerializer


class UserDetailsView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    get:
        Get user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ModelPermissions]

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserDisplaySerializer
        return self.retrieve(request, *args, **kwargs)

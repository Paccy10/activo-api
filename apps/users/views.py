from rest_framework import mixins, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django_rq import enqueue
from django.template.loader import get_template

from .models import User, generate_password
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from libs.utils.helpers import send_email


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """User viewsets

    post:
        Create a new user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["first_name", "lastname", "email"]

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


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom TokenObtainPairView"""

    serializer_class = CustomTokenObtainPairSerializer

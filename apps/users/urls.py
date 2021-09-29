from django.urls import path

from .views import UserView, CustomTokenObtainPairView

urlpatterns = [
    path("", UserView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
]

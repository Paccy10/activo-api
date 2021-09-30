from django.urls import path

from .views import UsersView, CustomTokenObtainPairView, UserDetailsView

urlpatterns = [
    path("", UsersView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("<int:pk>/", UserDetailsView.as_view()),
]

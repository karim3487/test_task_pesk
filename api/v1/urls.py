from django.urls import path

from authentication import views as auth_views
from api import views as api_views

urlpatterns = [
    path("login/", auth_views.LoginAPIView.as_view(), name="login"),
    path("register/", auth_views.RegisterAPIView.as_view(), name="register"),
    path("logout/", auth_views.LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", auth_views.RefreshAPIView.as_view(), name="token_refresh"),
    # Admin
    path("admin_view", api_views.AdminView.as_view(), name="admin_view"),
    # User
    path("user_view", api_views.UserView.as_view(), name="user_view"),
]

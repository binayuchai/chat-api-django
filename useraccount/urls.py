from django.urls import path
from .views import UserRegisterView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView,TokenVerifyView

app_name = "user_auth"

urlpatterns = [
    path('api/register/',UserRegisterView.as_view(),name="register"),
    path('api/login/',UserLoginView.as_view(),name="login"),
    path('api/profile/',UserProfileView.as_view(),name="profile"),
    path('api/change-password/',UserChangePasswordView.as_view(),name="change_password"),
    path('api/send-reset-password/',SendPasswordResetEmailView.as_view(),name="send_password_reset"),
    path('api/reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="password_reset"),
    path('api/logout/',LogoutView.as_view(),name="logout"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),


]
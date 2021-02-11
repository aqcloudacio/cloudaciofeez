from django.urls import path, include
from users.api.views import (UserViewSet, AFSLViewSet, PracticeViewSet,
                             NotificationViewSet,RegoViewSet, VerifyViewSet,
                             ResetPasswordViewSet, ChangePasswordViewSet,
                             RegoDetailsViewSet)
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

app_name = "users"

userrouter = SimpleRouter()

userrouter.register(r"user",
                    UserViewSet,
                    "user")

userrouter.register(r"afsls",
                    AFSLViewSet,
                    "afsls")

userrouter.register(r"practices",
                    PracticeViewSet,
                    "practices")

userrouter.register(r"notifications",
                    NotificationViewSet,
                    "notifications")

userrouter.register(r"rego",
                    RegoViewSet,
                    "rego")

userrouter.register(r"regodetails",
                    RegoDetailsViewSet,
                    "regodetails")

userrouter.register(r"resetpassword",
                    ResetPasswordViewSet,
                    "resetpassword")

userrouter.register(r"verify",
                    VerifyViewSet,
                    "verify")

userrouter.register(r"changepassword",
                    ChangePasswordViewSet,
                    "changepassword")


urlpatterns = [
    path("", include(userrouter.urls)),
    # Obtain a new access token and refresh JWT token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Submit a refresh token to obtain a new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

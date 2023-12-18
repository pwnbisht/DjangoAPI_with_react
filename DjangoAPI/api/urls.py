from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import RegistrationView, LoginView, UserFilesView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name="user_registration"),
    path('login/', LoginView.as_view(), name="user_login"),
    path('files/uploads/', UserFilesView.as_view(), name="uploads_files"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

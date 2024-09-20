from django.urls import path
from .views import RegisterView, MeuPerfilView, ChangePasswordView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenBlacklistView)


urlpatterns = [
    path('singup', RegisterView.as_view()),
    path('meuperfil/', MeuPerfilView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('alterar-senha/', ChangePasswordView.as_view(), name='alterar-senha'),
]
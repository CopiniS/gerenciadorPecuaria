from django.urls import path
from .views import RegisterView, MeuPerfilView, ChangePasswordView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenBlacklistView)
from .views import RecuperarSenhaView, RedefinirSenhaView, VerificarEmailView


urlpatterns = [
    path('singup', RegisterView.as_view()),
    path('meuperfil/', MeuPerfilView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('alterar-senha/', ChangePasswordView.as_view(), name='alterar-senha'),

    path('recuperar-senha/', RecuperarSenhaView.as_view(), name='recuperar_senha'),
    path('redefinir-senha/', RedefinirSenhaView.as_view(), name='redefinir_senha'),
    path('verificar-email/', VerificarEmailView.as_view(), name='verificar-email'),
]
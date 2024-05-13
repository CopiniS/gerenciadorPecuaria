from django.urls import path
from .views import RegisterView, LogoutView, GeraTokens, RenovaToken


urlpatterns = [
    path('singup', RegisterView.as_view()),
    path('logout', LogoutView.as_view()),
    path('token/', GeraTokens.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RenovaToken.as_view(), name='token_refresh'),
]
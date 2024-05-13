from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ProdutorSerializer
from .models import Produtor
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = ProdutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GeraTokens(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        token_access = AccessToken(response.data['access'])
        token_refresh = RefreshToken(response.data['refresh'])

        tempo_expiracao_access = token_access['exp']
        tempo_expiracao_refresh = token_refresh['exp']

        response.data['access_exp'] = tempo_expiracao_access
        response.data['refresh_exp'] = tempo_expiracao_refresh
        return response

class RenovaToken(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        token_access = AccessToken(response.data['access'])
        tempo_expiracao_access = token_access['exp']

        response.data['access_exp'] = tempo_expiracao_access
        return response


class LogoutView(APIView):
    pass
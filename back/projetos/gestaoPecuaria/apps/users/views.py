from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ProdutorSerializer
from .models import Produtor
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = ProdutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        produtor = Produtor.objects.filter(email=email).first()

        if produtor is None:
            raise AuthenticationFailed('Email não encontrado!')

        if not produtor.check_password(password):
            raise AuthenticationFailed('Senha incorreta!')
        
        access_token = AccessToken.for_user(produtor) 

        return Response({
            'access_token': str(access_token),  
            'message': 'Login bem-sucedido.'
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout bem-sucedido."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
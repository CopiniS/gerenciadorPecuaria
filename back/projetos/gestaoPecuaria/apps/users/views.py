from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import ProdutorSerializer
from .serializers import UpdateProdutorSerializer, GetProdutorSerializer, ChangePasswordSerializer
from .models import Produtor

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
import time
from .models import Produtor
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class VerificarEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                'existe': False,
                'mensagem': 'Email não fornecido'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar formato do email
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'existe': False,
                'mensagem': 'Formato de email inválido'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Pequeno delay para evitar força bruta
            time.sleep(0.5)

            # Verificar se o email existe no banco de dados
            produtor = Produtor.objects.filter(email=email).exists()

            return Response({
                'existe': produtor,
                'mensagem': 'Email encontrado' if produtor else 'Email não encontrado'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'existe': False,
                'mensagem': 'Erro ao verificar email'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RedefinirSenhaView(APIView):
    def post(self, request):
        try:
            uid = force_str(urlsafe_base64_decode(request.data.get('uid')))
            user = Produtor.objects.get(pk=uid)
            token = request.data.get('token')

            if default_token_generator.check_token(user, token):
                user.set_password(request.data.get('new_password'))
                user.save()
                return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, Produtor.DoesNotExist):
            return Response({"error": "Link inválido."}, status=status.HTTP_400_BAD_REQUEST)

class RecuperarSenhaView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Produtor.objects.get(email=email)
        except Produtor.DoesNotExist:
            return Response({"detail": "Se este e-mail estiver registrado, você receberá um link de recuperação."}, 
                          status=status.HTTP_200_OK)

        # Gerar token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construir link de recuperação com a URL do frontend
        reset_url = f"http://localhost:8081/redefinir-senha/{uid}/{token}"  # Ajuste a porta conforme seu frontend

        # Enviar e-mail
        send_mail(
            'Recuperação de Senha',
            f'Use este link para redefinir sua senha: {reset_url}',
            'noreply@seudominio.com',
            [email],
            fail_silently=False,
        )

        return Response({"detail": "Se este e-mail estiver registrado, você receberá um link de recuperação."}, 
                      status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        serializer = ProdutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class MeuPerfilView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            user = Produtor.objects.get(pk=request.user.id)
        except Produtor.DoesNotExist:
            raise NotFound('Usuário não encontrado.')

        serializer = UpdateProdutorSerializer(user, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        try:
            user = Produtor.objects.get(pk=request.user.id)
        except Produtor.DoesNotExist:
            raise NotFound('Usuário não encontrado.')
        
        serializer = GetProdutorSerializer(user)
        return Response(serializer.data)
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print (request.data)
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import ProdutorSerializer
from .serializers import UpdateProdutorSerializer, GetProdutorSerializer, ChangePasswordSerializer
from .models import Produtor

# Create your views here.
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
    
# class VerifyPasswordView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = VerifyPasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             user = request.user

#             # Verifica se a senha está correta
#             if not user.check_password(serializer.validated_data['password']):
#                 return Response({"detail": "Senha incorreta."}, status=status.HTTP_400_BAD_REQUEST)

#             # Se a senha estiver correta, retorna um status 200
#             return Response({"detail": "Senha verificada com sucesso."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
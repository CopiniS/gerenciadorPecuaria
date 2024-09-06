from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import ProdutorSerializer
from .serializers import UpdateProdutorSerializer
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
        
        serializer = UpdateProdutorSerializer(user)
        return Response(serializer.data)
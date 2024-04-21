from rest_framework import viewsets
from core.models import Produtor, Cidade, Propriedade, Raca, Animal, Estado
from core.serializers import ProdutorSerializer, CidadeSerializer, PropriedadeSerializer, RacaSerializer, AnimalSerializer, EstadoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class ProdutorLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')

        if email is None or senha is None:
            return Response({'error': 'Por favor, forneça tanto o email quanto a senha.'}, status=status.HTTP_400_BAD_REQUEST)

        produtor = Produtor.objects.filter(email=email).first()

        if produtor is None or not produtor.senha == senha:
            return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(produtor)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)

class ProdutorViewSet(viewsets.ModelViewSet):
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer

class CidadeViewSet(viewsets.ModelViewSet):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class PropriedadeViewSet(viewsets.ModelViewSet):
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer


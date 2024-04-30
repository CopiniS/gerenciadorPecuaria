from rest_framework import viewsets
from core.models import Produtor, Propriedade, Raca, Animal, Lote
from core.serializers import ProdutorSerializer, PropriedadeSerializer, RacaSerializer, AnimalSerializer, LoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

current_produtor_id = []

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

        global current_produtor_id
        current_produtor_id = []
        current_produtor_id.append(produtor.id)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)

class ProdutorViewSet(viewsets.ModelViewSet):
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer
  
class PropriedadeViewSet(viewsets.ModelViewSet):
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.filter(produtor__in=current_produtor_id)
    #Atualiza o produtor para o current_produtor
    def create(self, request, *args, **kwargs):
        data = request.data
        data['produtor'] = current_produtor_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer

    def get_queryset(self):
        return Raca.objects.filter(idProdutor__in=current_produtor_id)
    #Atualiza o idProdutor para o current_produtor
    def create(self, request, *args, **kwargs):
        data = request.data
        data['idProdutor'] = current_produtor_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.filter(lote__propriedade__produtor__in=current_produtor_id)

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

    def get_queryset(self):
        return Lote.objects.filter(propriedade__produtor__in=current_produtor_id)
    
    @action(detail=True, methods=['get'])
    def lotes_por_propriedade(self, request, pk=None):
        propriedade_id = self.kwargs['pk']
        lotes = Lote.objects.filter(propriedade__id=propriedade_id)
        serializer = self.get_serializer(lotes, many=True)
        return Response(serializer.data)

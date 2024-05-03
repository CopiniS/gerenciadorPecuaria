from rest_framework import viewsets
from core.models import Propriedade, Raca, Animal, Lote
from core.serializers import PropriedadeSerializer, RacaSerializer, AnimalSerializer, LoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

current_produtor_id = []

class PropriedadeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.filter(produtor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(produtor=self.request.user)

class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer

    def get_queryset(self):
        return Raca.objects.filter(produtor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(produtor=self.request.user)


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.filter(lote__propriedade__produtor = self.request.user)

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

    def get_queryset(self):
        return Lote.objects.filter(propriedade__produtor = self.request.user)
    
    @action(detail=True, methods=['get'])
    def lotes_por_propriedade(self, request, pk=None):
        propriedade_id = self.kwargs['pk']
        lotes = Lote.objects.filter(propriedade__id=propriedade_id)
        serializer = self.get_serializer(lotes, many=True)
        return Response(serializer.data)

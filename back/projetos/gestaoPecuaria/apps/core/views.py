from rest_framework import viewsets
from core.models import Propriedade, Raca, Animal, Lote
from core.serializers import PropriedadeSerializer, RacaSerializer, AnimalSerializer, LoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class PropriedadeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

    def get_queryset(self):
        return Propriedade.objects.filter(produtor=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['produtor'] = [self.request.user.id]
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        return super().destroy(request, pk, *args, **kwargs)

class RacaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer

    def get_queryset(self):
        return Raca.objects.filter(produtor=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['produtor'] = self.request.user.id
        return super().create(request, *args, **kwargs)

class AnimalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = Animal.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(lote__propriedade=propriedade_selecionada)
        serializer = AnimalSerializer(queryset, many=True)
        return Response(serializer.data)

class LoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = Lote.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        serializer = LoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    

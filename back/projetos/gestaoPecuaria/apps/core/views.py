from rest_framework import viewsets
from core import models
from core import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

class PropriedadeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Propriedade.objects.all()
    serializer_class = serializers.PropriedadeSerializer

    def get_queryset(self):
        return models.Propriedade.objects.filter(produtor=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['produtor'] = [self.request.user.id]
        return super().create(request, *args, **kwargs)
    

class RacaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Raca.objects.all()
    serializer_class = serializers.RacaSerializer

    def get_queryset(self):
        return models.Raca.objects.filter(produtor=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['produtor'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class AnimalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Animal.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(piquete__propriedade=propriedade_selecionada)
        serializer = serializers.AnimalSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='machos')
    def list_machos(self, request, *args, **kwargs):
        machos = models.Animal.objects.filter(sexo='macho')
        serializer = self.get_serializer(machos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='femeas')
    def list_femeas(self, request, *args, **kwargs):
        femeas = models.Animal.objects.filter(sexo='femea')
        serializer = self.get_serializer(femeas, many=True)
        return Response(serializer.data)
    
    
class PiqueteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Piquete.objects.all()
    serializer_class = serializers.PiqueteSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Piquete.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        serializer = serializers.PiqueteSerializer(queryset, many=True)
        return Response(serializer.data)


class VeterinarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Veterinario.objects.all()
    serializer_class = serializers.VeterinarioSerializer

    def get_queryset(self):
        return models.Veterinario.objects.filter(produtor=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['produtor'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Produto.objects.all()
    serializer_class = serializers.ProdutoSerializer

    def get_queryset(self):
        return models.Produto.objects.filter(produtor=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['produtor'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class PesagemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Pesagem.objects.all()
    serializer_class = serializers.PesagemSerializer 

    def list(self, request, *args, **kwargs):
        dataSelecionada = request.query_params.get('dataPesagem', None)
        queryset = models.Pesagem.objects.all()
        if dataSelecionada is not None:
            queryset = queryset.filter(dataPesagem=dataSelecionada)
        serializer = serializers.PesagemComAnimaisSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='datas')
    def list_datas(self, request, *args, **kwargs):
        datas = models.Pesagem.objects.values_list('dataPesagem', flat=True).distinct()
        return Response(datas)
    

class CompraProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.CompraProduto.objects.all()
    serializer_class = serializers.CompraProdutoSerializer

    def get_queryset(self):
        return models.CompraProduto.objects.filter(produto__produtor=self.request.user)


class SuplementacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Suplementacao.objects.all()
    serializer_class = serializers.SuplementacaoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Suplementacao.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.SuplementacaoSerializer(queryset, many=True)
        return Response(serializer.data)


class OcorrenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Ocorrencia.objects.all()
    serializer_class = serializers.OcorrenciaSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Ocorrencia.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.OcorrenciaSerializer(queryset, many=True)
        return Response(serializer.data)


class InseminacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Inseminacao.objects.all()
    serializer_class = serializers.InseminacaoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Inseminacao.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.InseminacaoSerializer(queryset, many=True)
        return Response(serializer.data)
    

class OutraDespesaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.OutraDespesa.objects.all()
    serializer_class = serializers.OutraDespesaSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.OutraDespesa.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        serializer = serializers.OutraDespesaSerializer(queryset, many=True)
        return Response(serializer.data)


class VendaAnimalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.VendaAnimal.objects.all()
    serializer_class = serializers.VendaAnimalSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.VendaAnimal.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.VendaAnimalSerializer(queryset, many=True)
        return Response(serializer.data)

   
class AplicacaoProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.AplicacaoProduto.objects.all()
    serializer_class = serializers.AplicacaoProdutoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.AplicacaoProduto.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.AplicacaoProdutoSerializer(queryset, many=True)
        return Response(serializer.data)
    

class FotoViewSet(viewsets.ModelViewSet):
    queryset = models.Foto.objects.all()
    serializer_class = serializers.FotoSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Foto.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.FotoSerializer(queryset, many=True)
        return Response(serializer.data)
    


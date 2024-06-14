from rest_framework import viewsets
from core import models
from core import serializers
from rest_framework import status
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
        serializer = serializers.AnimalComPiqueteAndRacaSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='machos')
    def list_machos(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        machos = models.Animal.objects.filter(sexo='macho')
        machosProp = machos.filter(piquete__propriedade=propriedade_selecionada)
        serializer = self.get_serializer(machosProp, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='femeas')
    def list_femeas(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        femeas = models.Animal.objects.filter(sexo='femea')
        femeasProp = femeas.filter(piquete__propriedade=propriedade_selecionada)
        serializer = self.get_serializer(femeasProp, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='vivos')
    def list_vivos(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        vivos = models.Animal.objects.filter(status = 'Vivo')
        vivosProp = vivos.filter(piquete__propriedade=propriedade_selecionada)
        serializer = self.get_serializer(vivosProp, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='femeas/vivas')
    def list_femeasVivas(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        femeas = models.Animal.objects.filter(sexo='femea')
        femeasVivas = femeas.filter(status='Vivo')
        femeasVivasProp = femeasVivas.filter(piquete__propriedade=propriedade_selecionada)
        serializer = self.get_serializer(femeasVivasProp, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path=r'animal/(?P<id>\d+)')
    def retornaAnimalSelecionado(self, request, *args, **kwargs):
        id_animal = kwargs.get('id')
        animal = self.get_queryset().filter(id=id_animal)
        serializer = serializers.AnimalComPiqueteAndRacaSerializer(animal, many=True)
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
    
    @action(detail=False, methods=['get'], url_path='sanitarios')
    def list_sanitarios(self, request, *args, **kwargs):
        sanitarios = models.Produto.objects.filter(tipo='sanitario')
        serializer = self.get_serializer(sanitarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='alimenticios')
    def list_alimenticios(self, request, *args, **kwargs):
        alimenticios = models.Produto.objects.filter(tipo='alimenticio')
        serializer = self.get_serializer(alimenticios, many=True)
        return Response(serializer.data)

class EstoqueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Estoque.objects.all()
    serializer_class = serializers.EstoqueSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Estoque.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        serializer = serializers.EstoqueSerializer(queryset, many=True)
        return Response(serializer.data)


class PesagemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Pesagem.objects.all()
    serializer_class = serializers.PesagemSerializer 

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Pesagem.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.PesagemComAnimaisSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='datas/(?P<data>[^/.]+)')
    def delete_por_data(self, request, *args, **kwargs):
        data = kwargs.get('data')
        try:
            objetos = self.get_queryset().filter(dataPesagem=data)
            objetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompraProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.CompraProduto.objects.all()
    serializer_class = serializers.CompraProdutoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.CompraProduto.objects.all()
        print('prop: ', propriedade_selecionada)
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        serializer = serializers.CompraProdutosComProdutosSerializer(queryset, many=True)
        return Response(serializer.data)


class SuplementacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Suplementacao.objects.all()
    serializer_class = serializers.SuplementacaoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Suplementacao.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.SuplementacaoComProdutoAndPiqueteSerializer(queryset, many=True)
        return Response(serializer.data)


class OcorrenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Ocorrencia.objects.all()
    serializer_class = serializers.OcorrenciaSerializer

    def list(self, request, *args, **kwargs):
        animal_selecionado = request.query_params.get('animalSelecionado', None)
        queryset = models.Ocorrencia.objects.all()
        if animal_selecionado is not None:
            queryset = queryset.filter(animal=animal_selecionado)
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
        serializer = serializers.InseminacaoComAnimalAndVeterinarioSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='datas/(?P<data>[^/.]+)')
    def delete_por_data(self, request, *args, **kwargs):
        data = kwargs.get('data')
        try:
            objetos = self.get_queryset().filter(dataInseminacao=data)
            objetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        serializer = serializers.VendaAnimalComAnimalSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='datas/(?P<data>[^/.]+)')
    def delete_por_data(self, request, *args, **kwargs):
        data = kwargs.get('data')
        try:
            objetos = self.get_queryset().filter(dataVenda=data)
            objetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
class AplicacaoProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.AplicacaoProduto.objects.all()
    serializer_class = serializers.AplicacaoProdutoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.AplicacaoProduto.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
        serializer = serializers.AplicacaoProdutoComAnimalAndProdutoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        animais = request.data['animal']
        respostas = []
        deuErro = False
        for animal in animais:
            request.data['animal'] = animal
            response = super().create(request, *args, **kwargs)
            respostas.append(response)
        for resposta in respostas:
            if resposta.status_code != status.HTTP_201_CREATED:
                deuErro = True
        if not deuErro:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='datas/(?P<data>[^/.]+)')
    def delete_por_data(self, request, *args, **kwargs):
        data = kwargs.get('data')
        try:
            objetos = self.get_queryset().filter(dataAplicacao=data)
            objetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FotoViewSet(viewsets.ModelViewSet):
    queryset = models.Foto.objects.all()
    serializer_class = serializers.FotoSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        animalSelecionado = request.query_params.get('animalSelecionado', None)
        queryset = models.Foto.objects.all()
        if animalSelecionado is not None:
            queryset = queryset.filter(animal=animalSelecionado)
        serializer = serializers.FotoSerializer(queryset, many=True)
        return Response(serializer.data)
    
class MovimentacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Movimentacao.objects.all()
    serializer_class = serializers.MovimentacaoSerializer

    


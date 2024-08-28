from rest_framework import viewsets
from core import models
from core import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q


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
    
    @action(detail=False, methods=['get'], url_path='produtor')
    def list_animais_do_produtor(self, request, *args, **kwargs):
        queryset = models.Animal.objects.all()
        queryset = queryset.filter(piquete__propriedade__produtor=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
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
    
    @action(detail=False, methods=['get'], url_path='vivos-piquetes')
    def list_vivos_piquetes(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        vivos = models.Animal.objects.filter(status = 'Vivo')
        vivosProp = vivos.filter(piquete__propriedade=propriedade_selecionada) 
        serializer = serializers.AnimalComPiqueteAndRacaSerializer(vivosProp, many=True)
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
        print('queryset antes: ', queryset)
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
            print('queryset: ', queryset)
        serializer = serializers.PiqueteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='piquetes-propriedades')
    def list_piquetes_propriedade(self, request, *args, **kwargs):
        piquetes = models.Piquete.objects.all()
        piquetes = piquetes.filter(propriedade__produtor=self.request.user)
        serializer = serializers.PiqueteComPropriedadeSerializer(piquetes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='com-animais')
    def list_piquetes_com_animais(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        vivos = models.Animal.objects.filter(status = 'Vivo')
        vivosProp = vivos.filter(piquete__propriedade=propriedade_selecionada)
        piquetesComAnimais = []
        for animal in vivosProp:
            if animal.piquete not in piquetesComAnimais:
                piquetesComAnimais.append(animal.piquete)
        serializer = serializer = serializers.PiqueteSerializer(piquetesComAnimais, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='com-animais-propriedade')
    def list_piquetes_com_animais_propriedade(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        vivos = models.Animal.objects.filter(status = 'Vivo')
        vivosProp = vivos.filter(piquete__propriedade=propriedade_selecionada)
        piquetesComAnimais = []
        for animal in vivosProp:
            if animal.piquete not in piquetesComAnimais:
                piquetesComAnimais.append(animal.piquete)
        serializer = serializers.PiqueteComPropriedadeSerializer(piquetesComAnimais, many=True)
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
    
    @action(detail=False, methods=['get'], url_path=r'pesagem/(?P<id>\d+)')
    def retornaPesagemSecionada(self, request, *args, **kwargs):
        id_pesagem = kwargs.get('id')
        pesagem = self.get_queryset().filter(id=id_pesagem)
        serializer = serializers.PesagemComAnimaisSerializer(pesagem, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='por-data')
    def list_por_datas(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        data_selecionada = request.query_params.get('dataSelecionada', None)
        queryset = models.Pesagem.objects.all()
        if propriedade_selecionada is not None and data_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
            queryset = queryset.filter(dataPesagem=data_selecionada)
            
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

    @action(detail=False, methods=['get'], url_path=r'compra/(?P<id>\d+)')
    def retornaCompraSecionada(self, request, *args, **kwargs):
        id_compra = kwargs.get('id')
        compra = self.get_queryset().filter(id=id_compra)
        serializer = serializers.CompraProdutosComProdutosSerializer(compra, many=True)
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
    
    @action(detail=False, methods=['get'], url_path=r'suplementacao/(?P<id>\d+)')
    def retornaSuplementacaoSecionada(self, request, *args, **kwargs):
        id_suplementacao = kwargs.get('id')
        suplementacao = self.get_queryset().filter(id=id_suplementacao)
        serializer = serializers.SuplementacaoComProdutoAndPiqueteSerializer(suplementacao, many=True)
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
    
    @action(detail=False, methods=['get'], url_path=r'ocorrencia/(?P<id>\d+)')
    def retornaOcorrenciaSelecionada(self, request, *args, **kwargs):
        id_ocorrencia = kwargs.get('id')
        ocorrencia = self.get_queryset().filter(id=id_ocorrencia)
        serializer = serializers.OcorrenciaComAnimalSerializer(ocorrencia, many=True)
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
    
    @action(detail=False, methods=['get'], url_path=r'inseminacao/(?P<id>\d+)')
    def retornaInseminacaoSecionada(self, request, *args, **kwargs):
        id_inseminacao = kwargs.get('id')
        inseminacao = self.get_queryset().filter(id=id_inseminacao)
        serializer = serializers.InseminacaoComAnimalAndVeterinarioSerializer(inseminacao, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='por-data')
    def list_por_datas(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        data_selecionada = request.query_params.get('dataSelecionada', None)
        queryset = models.Inseminacao.objects.all()
        if propriedade_selecionada is not None and data_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
            queryset = queryset.filter(dataInseminacao=data_selecionada)
            
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


class GastoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Gasto.objects.all()
    serializer_class = serializers.GastoSerializer

    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Gasto.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(propriedade=propriedade_selecionada)
        print('queryset: ' , queryset)
        serializer = serializers.GastoSerializer(queryset, many=True)
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
    
    @action(detail=False, methods=['get'], url_path='por-data')
    def list_por_datas(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        data_selecionada = request.query_params.get('dataSelecionada', None)
        queryset = models.VendaAnimal.objects.all()
        if propriedade_selecionada is not None and data_selecionada is not None:
            queryset = queryset.filter(animal__piquete__propriedade=propriedade_selecionada)
            queryset = queryset.filter(dataVenda=data_selecionada)
            
        serializer = serializers.VendaAnimalComAnimalSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'venda/(?P<id>\d+)')
    def retornaVendaSelecionada(self, request, *args, **kwargs):
        id_venda = kwargs.get('id')
        venda = self.get_queryset().filter(id=id_venda)
        serializer = serializers.VendaAnimalComAnimalSerializer(venda, many=True)
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
    
    @action(detail=False, methods=['get'], url_path=r'aplicacao/(?P<id>\d+)')
    def retornaAplicacaoSecionada(self, request, *args, **kwargs):
        id_aplicacao = kwargs.get('id')
        aplicacao = self.get_queryset().filter(id=id_aplicacao)
        serializer = serializers.AplicacaoProdutoComAnimalAndProdutoSerializer(aplicacao, many=True)
        return Response(serializer.data)

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
    
    def list(self, request, *args, **kwargs):
        propriedade_selecionada = request.query_params.get('propriedadeSelecionada', None)
        queryset = models.Movimentacao.objects.all()
        if propriedade_selecionada is not None:
            queryset = queryset.filter(
            Q(piqueteOrigem__propriedade=propriedade_selecionada) | 
            Q(piqueteDestino__propriedade=propriedade_selecionada)
        )
        serializer = serializers.MovimentacaoComPiquetesAndAnimalSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='por-detalhe')
    def list_por_detalhe(self, request, *args, **kwargs):
        dataSelecionada = request.query_params.get('dataSelecionada', None)
        piqueteOrigem = request.query_params.get('piqueteOrigem', None)
        piqueteDestino = request.query_params.get('piqueteDestino', None)
        queryset = models.Movimentacao.objects.all()
        if dataSelecionada is not None and piqueteOrigem is not None and piqueteDestino is not None:
            queryset = queryset.filter(
            Q(dataMovimentacao=dataSelecionada) &
            Q(piqueteOrigem=piqueteOrigem) & 
            Q(piqueteDestino=piqueteDestino) 
        )
        serializer = serializers.MovimentacaoComPiquetesAndAnimalSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'movimentacao/(?P<id>\d+)')
    def retornaMovimentacaoSecionada(self, request, *args, **kwargs):
        id_movimentacao = kwargs.get('id')
        movimentacao = self.get_queryset().filter(id=id_movimentacao)
        serializer = serializers.MovimentacaoComPiquetesAndAnimalSerializer(movimentacao, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='datas/(?P<data>[^/.]+)')
    def delete_por_data(self, request, *args, **kwargs):
        data = kwargs.get('data')
        try:
            objetos = self.get_queryset().filter(dataMovimentacao=data)
            objetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

    


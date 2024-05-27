from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model


class PropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Propriedade
        fields ="__all__"

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Raca
        fields ="__all__"

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields ="__all__"

class PiqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Piquete
        fields = "__all__"

class VeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Veterinario
        fields = "__all__"

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produto
        fields = "__all__"

class PesagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pesagem
        fields = "__all__"

class PesagemComAnimaisSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer(read_only=True)

    class Meta:
        model = models.Pesagem
        fields = "__all__"

class CompraProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompraProduto
        fields = "__all__"

class CompraProdutosComProdutosSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    
    class Meta:
        model = models.CompraProduto
        fields = "__all__"

class SuplementacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Suplementacao
        fields = "__all__"

class OcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ocorrencia
        fields = "__all__"

class InseminacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inseminacao
        fields = "__all__"

class OutraDespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutraDespesa
        fields = "__all__"

class VendaAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VendaAnimal
        fields = "__all__"

class AplicacaoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AplicacaoProduto
        fields = "__all__"

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Foto
        fields = "__all__"
from rest_framework import serializers
from core.models import Produtor, Cidade, Propriedade, Raca, Animal, Estado

class ProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtor
        fields = ['id', 'nome', 'cpf', 'email', 'senha']

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields ="__all__"

class PropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propriedade
        fields ="__all__"

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields ="__all__"

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields ="__all__"

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields ="__all__"
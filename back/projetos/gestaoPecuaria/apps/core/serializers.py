from rest_framework import serializers
from core.models import Produtor, Propriedade, Raca, Animal, Lote

class ProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtor
        fields = "__all__"

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

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = "__all__"
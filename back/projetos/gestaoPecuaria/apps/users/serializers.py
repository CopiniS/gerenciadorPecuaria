from rest_framework import serializers
from .models import Produtor


class ProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtor
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class UpdateProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtor
        fields = ['nome', 'cpf', 'telefone1', 'telefone2']

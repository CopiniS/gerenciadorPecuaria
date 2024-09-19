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
        fields = ['nome', 'cpf', 'telefone1', 'telefone2', 'email']

class GetProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtor
        fields = ['nome', 'cpf', 'telefone1', 'telefone2', 'email']


class VerifyPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
from django.db import models

class Produtor(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cpf = models.CharField('CPF', max_length=11)
    email = models.CharField('Email', max_length=50)
    senha = models.CharField('Senha', max_length=20)

class Estado(models.Model):
    nome = models.CharField('Nome', max_length=50)

class Cidade(models.Model):
    nome = models.CharField('Nome', max_length=35)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Propriedade(models.Model):
    nome = models.CharField('Nome', max_length=50)
    endereco = models.CharField('Endereco', max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=2)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=2)
    produtor = models.ManyToManyField(Produtor)

class Lote(models.Model):
    nome = models.CharField('Nome', max_length=50)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    tipoCultivo = models.CharField('Tipo do cultivo', max_length=50)

class Raca(models.Model):
    nome = models.CharField('Nome', max_length=20)

class Animal(models.Model):
    brinco = models.CharField('Brinco', max_length=6)
    dataNascimento = models.DateField('Data de nascimento')
    sexo = models.CharField('Sexo', max_length=5)
    racaPredominante = models.ForeignKey(Raca, on_delete=models.CASCADE)
    racaObservacao = models.CharField('Raça de observação', max_length=50)
    lote = models.ForeignKey('Lote', on_delete=models.CASCADE, default=0) 

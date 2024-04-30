from django.db import models

class Produtor(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cpf = models.CharField('CPF', max_length=15)
    email = models.CharField('Email', max_length=50)
    senha = models.CharField('Senha', max_length=20)
    telefone1 = models.CharField('Telefone', max_length=15, default='')
    telefone2 = models.CharField('Telefone 2', max_length=15, null=True)

class Propriedade(models.Model):
    nome = models.CharField('Nome', max_length=50)
    endereco = models.CharField('Endereco', max_length=50)
    estado = models.CharField('Estado', max_length=50)
    cidade = models.CharField('Cidade', max_length=50)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=2)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=2)
    produtor = models.ManyToManyField(Produtor)

class Lote(models.Model):
    nome = models.CharField('Nome', max_length=50)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    tipoCultivo = models.CharField('Tipo do cultivo', max_length=50)

class Raca(models.Model):
    nome = models.CharField('Nome', max_length=20)
    idProdutor = models.ForeignKey(Produtor,on_delete=models.CASCADE )

class Animal(models.Model):
    brinco = models.CharField('Brinco', max_length=6)
    dataNascimento = models.DateField('Data de nascimento')
    sexo = models.CharField('Sexo', max_length=5)
    racaPredominante = models.ForeignKey(Raca, on_delete=models.CASCADE)
    racaObservacao = models.CharField('Raça de observação', max_length=50)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, default=0) 

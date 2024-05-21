from django.db import models
from users.models import Produtor

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
    produtor = models.ForeignKey(Produtor,on_delete=models.CASCADE )

class Animal(models.Model):
    brinco = models.CharField('Brinco', max_length=6)
    dataNascimento = models.DateField('Data de nascimento')
    sexo = models.CharField('Sexo', max_length=5)
    racaPredominante = models.ForeignKey(Raca, on_delete=models.CASCADE)
    racaObservacao = models.CharField('Raça de observação', max_length=50)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, default=0) 
    brincoPai = models.CharField('Brinco do pai', max_length=6, null=True)
    brincoMae = models.CharField('Brinco da mae', max_length=6, null=True)

class Veterinario(models.Model):
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.CharField('Email', max_length=255)
    crmv = models.CharField('CRMV', max_length=15)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)

class ProdutoSanitario(models.Model):
    nome = models.CharField('Nome', max_length=50)
    tipo = models.CharField('Tipo', max_length=50)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)

class ProdutoAlimenticio(models.Model):
    nome = models.CharField('Nome', max_length=50)
    tipo = models.CharField('Tipo', max_length=50)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)    

class Pesagem(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    dataPesagem = models.DateField('Data de pesagem')
    peso = models.DecimalField('Peso', max_digits=10, decimal_places=2)
    Observacao = models.CharField('Observacao', max_length=255)

class CompraProdutoAlimenticio(models.Model):
    produtoAlimenticio = models.ForeignKey(ProdutoAlimenticio, on_delete=models.CASCADE)
    valorUnitario = models.DecimalField('Valor unitário', max_digits=10,  decimal_places=2)
    quantidadeComprada = models.DecimalField('Quantidade comprada', max_digits=10,  decimal_places=3)
    dataCompra = models.DateField('Data de compra')
    validade = models.DateField('Data de vencimento')
    lote = models.CharField('Lote', max_length=50)

class CompraProdutoSanitario(models.Model):
    produtoSanitario = models.ForeignKey(ProdutoSanitario, on_delete=models.CASCADE)
    valorUnitario = models.DecimalField('Valor unitário', max_digits=10,  decimal_places=2)
    quantidadeComprada = models.DecimalField('Quantidade comprada', max_digits=10,  decimal_places=3)
    dataCompra = models.DateField('Data de compra')
    validade = models.DateField('Data de vencimento')
    lote = models.CharField('Lote', max_length=50)

class Suplementacao(models.Model):
    produtoAlimenticio = models.ForeignKey(ProdutoAlimenticio, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    dataInicial = models.DateField('Data inicial')
    dataFinal = models.DateField('Data final')
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)




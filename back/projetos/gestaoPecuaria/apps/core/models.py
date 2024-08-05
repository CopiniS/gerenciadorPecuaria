from django.db import models
from users.models import Produtor


class Propriedade(models.Model):
    nome = models.CharField('Nome', max_length=50)
    endereco = models.CharField('Endereco', max_length=50)
    estado = models.CharField('Estado', max_length=50)
    cidade = models.CharField('Cidade', max_length=50)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=2)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=2)
    area = models.DecimalField('Área', max_digits=10, decimal_places=2)
    produtor = models.ManyToManyField(Produtor)

class Piquete(models.Model):
    nome = models.CharField('Nome', max_length=50)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    tipoCultivo = models.CharField('Tipo do cultivo', max_length=50)
    area = models.DecimalField('Área', max_digits=10, decimal_places=2)

class Raca(models.Model):
    nome = models.CharField('Nome', max_length=20)
    produtor = models.ForeignKey(Produtor,on_delete=models.CASCADE )

class Animal(models.Model):
    brinco = models.CharField('Brinco', max_length=6)
    dataNascimento = models.DateField('Data de nascimento')
    sexo = models.CharField('Sexo', max_length=5)
    racaPredominante = models.ForeignKey(Raca, on_delete=models.CASCADE, null=True)
    racaObservacao = models.CharField('Raça de observação', max_length=50, null=True)
    piquete = models.ForeignKey(Piquete, on_delete=models.CASCADE, default=0) 
    brincoPai = models.CharField('Brinco do pai', max_length=6, null=True)
    brincoMae = models.CharField('Brinco da mae', max_length=6, null=True)
    rfid = models.CharField('RFID', max_length=50, null=True)
    observacoes = models.CharField('Observações', max_length=255, null=True)
    dataBaixa = models.DateField('Data da baixa', null=True)
    status = models.CharField('Status', max_length=50)
    dataCompra = models.DateField('Data de compra', null=True)
    valorCompra = models.DecimalField('Valor da compra', max_digits=10, decimal_places=2, null=True)

class Veterinario(models.Model):
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.CharField('Email', max_length=255)
    crmv = models.CharField('CRMV', max_length=15)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=50)
    tipo = models.CharField('Tipo', max_length=50)
    categoria = models.CharField('Categoria', max_length=50, null=True)
    descricao = models.CharField('Descricao', max_length=255, null=True)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)
    
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    quantidade = models.BigIntegerField('Quantidade')

class Pesagem(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    dataPesagem = models.DateField('Data de pesagem')
    peso = models.DecimalField('Peso', max_digits=10, decimal_places=2)
    observacao = models.CharField('Observacao', max_length=255, null=True)

class CompraProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valorUnitario = models.DecimalField('Valor unitário', max_digits=10,  decimal_places=2)
    quantidadeComprada = models.BigIntegerField('Quantidade comprada')
    dataCompra = models.DateField('Data de compra')
    validade = models.DateField('Data de vencimento')
    lote = models.CharField('Lote', max_length=50, null=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)

class Suplementacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    dataInicial = models.DateField('Data inicial')
    dataFinal = models.DateField('Data final', null=True)
    piquete = models.ForeignKey(Piquete, on_delete=models.CASCADE)

class Ocorrencia(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    dataOcorrencia = models.DateField('Data da ocorrência')
    tipo = models.CharField('Tipo', max_length=50)
    descricao = models.CharField('Descrição', max_length=255, null=True)

class Inseminacao(models.Model):
    dataInseminacao = models.DateField('Data')
    identificadorTouro = models.CharField('Identificador do touro', max_length=50)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
    observacao = models.CharField('Observação', max_length=255, null=True)

class OutraDespesa(models.Model):
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    dataDespesa = models.DateField('Data da despesa')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    descricao = models.CharField('Descrição', max_length=255)
    categoria = models.CharField('Categoria', max_length=50)

class VendaAnimal(models.Model):
    dataVenda = models.DateField('Data da venda')
    peso = models.DecimalField('Peso', max_digits=10, decimal_places=3, null=True)
    precoKg = models.DecimalField('Preço po Kg', max_digits=10, decimal_places=2, null=True)
    valorTotal = models.DecimalField('Valor total', max_digits=10, decimal_places=2)
    finalidade = models.CharField('Finalidade', max_length=50)
    observacao = models.CharField('Observação', max_length=255, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
class AplicacaoProduto(models.Model):
    dataAplicacao = models.DateField('Data da aplicação')
    dosagem = models.DecimalField('Dosagem', max_digits=10, decimal_places=2)
    observacao = models.CharField('Observação', max_length=255, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

class Foto(models.Model):
    foto = models.ImageField('Foto', upload_to='fotos-animais/')
    dataFoto = models.DateField('Data da foto')
    observacao = models.CharField('Observação', max_length=255, null =True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

class Movimentacao(models.Model):
    dataMovimentacao = models.DateField('Data da Movimentação')
    piqueteOrigem = models.ForeignKey(Piquete, on_delete=models.CASCADE, related_name='movimentacoes_origem')
    piqueteDestino = models.ForeignKey(Piquete, on_delete=models.CASCADE, related_name='movimentacoes_destino')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    motivo = models.CharField('Motivo', max_length=255, null=True)

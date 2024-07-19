<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'aplicacoes' }" id="nav-vet-tab" @click="selectTab('aplicacoes')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Aplicação</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab" @click="selectTab('edicao')" 
        type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição de Aplicação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacoes' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel" aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Aplicação</h1>
            <form @submit.prevent="submitForm">
            <div class="mb-3 input-group" :class="{ 'is-invalid': !isDataValida }">
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :placeholder="dataPlaceholder" class="form-control" id="dataAplicacaoEdicao"
                v-model="formData.dataAplicacao">
            </div>
            <div class="mb-3 input-group" :class="{ 'is-invalid': !isBrincoValido }">
              <input v-model="brinco" @input="inputBrinco" type="text" class="form-control" id="brincoField"
                :placeholder="brincoPlaceholder">
            </div>
            <div class="list-group" v-if="brinco && animaisFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados"
                :key="animal.id" @click="selectAnimal(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group" :class="{ 'is-invalid': !isProdutoValido }">
              <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control"
                :placeholder="produtoPlaceholder">
            </div>
            <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                {{ produto.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.dosagem" type="text" @input="aplicarDosagemMask" class="form-control" id="dosagem" :placeholder="dosagemPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.observacao" type="text" @input="aplicarObservacaoMask" class="form-control" id="observacao" :placeholder="observacaoPlaceholder">
              <div>({{ contadorObservacoes }} / 255)</div>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('aplicacoes')">Cancelar</button>
              <button type="submit" class="btn btn-success">Enviar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';
import { masksMixin } from '../mixins/maks';

export default {
  mixins: [masksMixin],

  data() {
    return {
      activeTab: 'edicao', // Começa na aba de edição
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      produtos: [],
      produtosFiltrados: [],
      nomeProduto: '',
      radioEscolha: 'brinco',
      formData: {
        id: null,
        produto: '',
        animal: [],
        dosagem: '',
        dataAplicacao: '',
        observacao: null,
      },
      isBrincoValido: true,
      isDataValida: true,
      isPiqueteValido: true,
      isDosagemValida: true,
      isObservacaoValida: true,
      isProdutoValido: true,
      brincoPlaceholder: 'Brinco do animal*',
      dataPlaceholder: 'Data da aplicacao*',
      piquetePlaceholder: 'Piquete*',
      dosagemPlaceholder: 'Dosagem do produto*',
      observacaoPlaceholder: 'Observação',
      produtoPlaceholder: 'Produto*'
    };
  },

  mounted() {
    const aplicacaoId = this.$route.params.aplicacaoId;
    if (aplicacaoId) {
      this.fetchAplicacao(aplicacaoId);
    }
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();

  },
  methods: {
    async fetchAplicacao(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/aplicacoes-produtos/aplicacao/${id}`);
        const aplicacao = response.data;
        this.formData.id = aplicacao[0].id;
        this.formData.animal = aplicacao[0].animal.id;
        this.formData.dataAplicacao = aplicacao[0].dataAplicacao;
        this.formData.produto = aplicacao[0].produto.id;
        this.formData.dosagem = aplicacao[0].dosagem;
        this.formData.observacao = aplicacao[0].observacao;

        this.brinco = aplicacao[0].animal.brinco;
        this.nomeProduto = aplicacao[0].produto.nome;
      } catch (error) {
        console.error('Erro ao carregar dados da aplicacao:', error);
      }
    },

    aplicarDosagemMask(event) {
      const value = event.target.value;
      this.formData.dosagem =  this.valorMask(value);
    },

    aplicarBrincoMask(value){
      this.brinco =  this.brincoMask(value);
    },

    aplicarObservacaoMask(event){
      const value = event.target.value;
      this.formData.observacao = this.observacoesMask(value);
      this.contadorObservacoes = this.formData.observacao.length;
    },

    inputBrinco(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
    },

    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/vivos', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectAnimal(animal) {
      this.formData.animal = [];
      this.brinco = animal.brinco;
      this.formData.animal.push(animal.id);
      this.animaisFiltrados = [];
    },

    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/sanitarios', {});
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },

    selectProduto(produto) {
      this.nomeProduto = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
    },

    validarFormulario() {
      let valido = true;

      this.formData.dataAplicacao = this.formData.dataAplicacao.trim();
      this.isDataValida = !!this.formData.dataAplicacao;
      this.dataPlaceholder = this.isDataValida ? 'Data da Aplicação' : 'Campo obrigatório';

      this.formData.dosagem = this.formData.dosagem.trim();
      this.isDosagemValida = !!this.formData.dosagem;
      this.dosagemPlaceholder = this.isDosagemValida ? 'Dosagem do Produto' : 'Campo obrigatório';

      if (this.formData.observacao === '') {
        this.formData.observacao = null;
      }
      // Validar Brinco (apenas se for escolhido por brinco)
      if (this.radioEscolha === 'brinco') {
        this.isBrincoValido = !!this.formData.animal.length;
        this.brincoPlaceholder = this.isBrincoValido ? 'Brinco do Animal' : 'Campo obrigatório';
        if (!this.isBrincoValido) {
          valido = false;
        }
      }

      // Validar Piquete (apenas se for escolhido por piquete)
      if (this.radioEscolha === 'piquete') {
        this.isPiqueteValido = !!this.piqueteId;
        this.piquetePlaceholder = this.isPiqueteValido ? 'Piquete' : 'Campo obrigatório';
        if (!this.isPiqueteValido) {
          valido = false;
        }
      }
      
      this.isProdutoValido = !!this.formData.produto;
      this.produtoPlaceholder = this.isProdutoValido ? 'Produto' : 'Campo obrigatório';
      if (!this.isProdutoValido) {
        valido = false;
      }

      return valido;
    },


    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'aplicacoes') {
        this.$router.push('/aplicacoes-produtos');
      }
    },

    cancelarEdicao() {
      this.$router.push('/aplicacoes');
    },

    verificaVazio(){
      //DATA DA APLICAÇÃO
      if(this.formData.dataAplicacao != null){
        if(this.formData.dataAplicacao.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Digite a Data da Aplicação';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Aplicação é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Aplicação é um Campo Obrigatório';
      }

      //BRINCO || PIQUETE
      if(this.radioEscolha == 'brinco'){
        if(this.brinco != null){
          if(this.brinco.trim() != ''){
            this.isBrincoValido = true;
            this.brincoPlaceholder = 'Digite o brinco do animal';
          }
          else{
            this.isBrincoValido = false;
            this.brincoPlaceholder = 'Brinco é um Campo Obrigatório';
          }
        }
        else{
          this.isBrincoValido = false;
          this.brincoPlaceholder = 'Brinco é um Campo Obrigatório';
        }
      }
      else{
        if(this.nomePiquete != null){
          if(this.nomePiquete.trim() != ''){
            this.isPiqueteValido = true;
            this.piquetePlaceholder = 'Digite o Piquete ';
          }
          else{
            this.isPiqueteValido = false;
          this.piquetePlaceholder = 'Piquete é um Campo Obrigatório';
          }
        }
        else{
          this.isPiqueteValido = false;
          this.piquetePlaceholder = 'Piquete é um Campo Obrigatório';
        }
      }

      //PRODUTO
      if(this.nomeProduto != null){
        if(this.nomeProduto.trim() != ''){
          this.isProdutoValido = true;
          this.produtoPlaceholder = 'Digite o nome do Produto';
        }
        else{
          this.isProdutoValido = false;
          this.produtoPlaceholder = 'Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isProdutoValido = false;
        this.produtoPlaceholder = 'Produto é um Campo Obrigatório';
      }

      //DOSAGEM
      if(this.formData.dosagem != null){
        if(this.formData.dosagem.trim() != ''){
          this.isDosagemValida = true;
          this.dosagemPlaceholder = 'Digite a Dosagem do produto'
        }
        else{
          this.isDosagemValida = false;
          this.dosagemPlaceholder = 'Dosagem é um Campo Obrigatório';
        }
      }
      else{
        this.isDosagemValida = false;
        this.dosagemPlaceholder = 'Dosagem é um Campo Obrigatório';
      }
      return (
        this.isDataValida &&
        this.isBrincoValido && 
        this.isPiqueteValido && 
        this.isProdutoValido && 
        this.isDosagemValida
      );
    },

    async submitForm() {
      if (this.verificaVazio()) {
        try {
            console.log(this.formData);
          const response = await api.patch(`http://127.0.0.1:8000/aplicacoes-produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/aplicacoes-produtos');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
}

.table-container {
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.button-container {
  text-align: left;
  margin-bottom: 20px;
}

.table-container table tbody tr td {
  background-color: #ededef !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  background-color: #f0f0f0;
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}
</style>

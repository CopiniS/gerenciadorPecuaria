<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'suplementacoes' }" id="nav-vet-tab"
          @click="selectTab('suplementacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Suplementação</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Suplementação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'suplementacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Suplementação</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <label for="dataInicial" class="input-group-text" title="Data Inicial da Suplementação"><i class="fas fa-calendar-alt"></i></label>
              <input type="text" :class="{ 'is-invalid': !isDataInicialValida }" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataInicialPlaceholder" class="form-control"
                id="dataInicialCadastro" v-model="formData.dataInicial" title="Data Inicial da Suplementação">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-box"></i></span>
              <input v-model="nomeProduto" @input="filtrarProdutos" :class="{ 'is-invalid': !isProdutoValido }"
                type="text" class="form-control" :placeholder="produtoPlaceholder">
            </div>
            <div class="list-group" v-if="nomeProduto && filteredProdutos.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="produto in filteredProdutos"
                :key="produto.id" @click="selecionarProduto(produto)">
                {{ produto.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="nomePiquete" @input="filtrarPiquetes" :class="{ 'is-invalid': !isPiqueteValido }"
                type="text" class="form-control" :placeholder="piquetePlaceholder">
            </div>
            <div class="list-group" v-if="nomePiquete && filteredPiquetes.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetes"
                :key="piquete.id" @click="selecionarPiquete(piquete)">
                {{ piquete.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Quantidade de Produto na Suplementação"><i class="fas fa-boxes"></i></span>
              <input v-model="formData.quantidade" type="text" :class="{ 'is-invalid': !isQuantidadeValida }"
                @input="aplicarQuantidadeMask" class="form-control" id="quantidade" 
                :placeholder="quantidadePlaceholder" title="Quantidade de Produto na Suplementação">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('suplementacoes')">Cancelar</button>
              <button type="button" class="btn btn-success" @click="submitForm">Enviar</button>
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
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      produtos: [],
      piquetes: [],
      filteredProdutos: [],
      filteredPiquetes: [],
      nomeProduto: '',
      nomePiquete: '',
      formData: {
        id: null,
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
      },
      isProdutoValido: true,
      isPiqueteValido: true,
      isQuantidadeValida: true,
      isDataInicialValida: true,
      produtoPlaceholder: 'Produto usado na Suplementação*',
      piquetePlaceholder: 'Piquete da Suplementação*',
      quantidadePlaceholder: 'Quantidade do Produto*',
      dataInicialPlaceholder: 'Data Inicial da Suplementação*',
    };
  },

  mounted() {
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarQuantidadeMask(event){
      const value = event.target.value;
      this.formData.quantidade = this.valorMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/alimenticios');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },
    
    async submitForm() {
      if (this.verificaVazio()) {
        try {
           //FORMATA VALOR E QUANTIDADE
          this.formData.quantidade = this.replaceVirgulaPonto(this.formData.quantidade);

          const response = await api.post('http://127.0.0.1:8000/suplementacoes/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/suplementacoes');
          } else {
            alert('Erro ao cadastrar suplementacao. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filtrarProdutos(entrada) {
      if (!entrada) {
        this.filteredProdutos = this.produtos;
        return;
      }
      this.filteredProdutos = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },

    selecionarProduto(produto) {
      this.formData.produto = produto.id;
      this.nomeProduto = produto.nome;
      this.filteredProdutos = [];
    },

    filtrarPiquetes(entrada) {
      if (!entrada) {
        this.filteredPiquetes = this.piquetes;
        return;
      }
      this.filteredPiquetes = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete));
    },

    selecionarPiquete(piquete) {
      this.formData.piquete = piquete.id;
      this.nomePiquete = piquete.nome;
      this.filteredPiquetes = [];
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA INICIAL
      if(this.formData.dataInicial != null){
        if(this.formData.dataInicial.trim() != ''){
          this.isDataInicialValida = true;
          this.dataInicialPlaceholder = 'Data Inicial da Suplementação*';
        }
        else{
          this.isDataInicialValida = false;
          this.dataInicialPlaceholder = 'Data Inicial é um Campo Obrigatório';
        }
      }
      else{
        this.isDataInicialValida = false;
        this.dataInicialPlaceholder = 'Data Inicial é um Campo Obrigatório';
      }

      //PRODUTO
      if(this.nomeProduto != null){
        if(this.nomeProduto.trim() != ''){
          this.isProdutoValido = true;
          this.produtoPlaceholder = 'Produto usado na Suplementação*';
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

      //PIQUETE
      if(this.nomePiquete != null){
        if(this.nomePiquete != ''){
          this.isPiqueteValido = true;
          this.piquetePlaceholder = 'Piquete da Suplementação*';
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

      //QUANTIDADE DO PRODUTO
      if(this.formData.quantidade != null){
        if(this.formData.quantidade.trim() != ''){
          this.isQuantidadeValida = true;
          this.quantidadePlaceholder = 'Quantidade do Produto*';
        }
        else{
          this.isQuantidadeValida = false;
          this.quantidadePlaceholder = 'Quantidade do Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isQuantidadeValida = false;
        this.quantidadePlaceholder = 'Quantidade do Produto é um Campo Obrigatório';
      }

      return (
        this.isDataInicialValida &&
        this.isProdutoValido &&
        this.isPiqueteValido &&
        this.isQuantidadeValida
      );
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'suplementacoes') {
        this.$router.push('/suplementacoes');
      }
    },

    replaceVirgulaPonto(valorString){
      valorString = valorString.replace(",", ".");

      return valorString;
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

#legenda {
    font-size: 16px;
}
</style>

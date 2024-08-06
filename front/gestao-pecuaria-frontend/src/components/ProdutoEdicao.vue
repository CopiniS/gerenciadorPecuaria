<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'produtos' }" id="nav-vet-tab"
          @click="selectTab('produtos')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Produto</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Produto</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'produtos' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Produto</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-box"></i></span>
              <input v-model="formData.nome" type="text" class="form-control" id="nome" :placeholder="nomePlaceholder" :class="{'is-invalid': !isNomeValido}" >
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-clipboard-list"></i></span>
              <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                :placeholder="tipoPlaceholder" :class="{'is-invalid': !isTipoValido}" >
                <option disabled value="">{{ tipoPlaceholder }}</option>
                <option value="sanitario">Sanitário</option>
                <option value="alimenticio">Alimentício</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-balance-scale"></i></span>
              <select v-model="formData.unidade" class="form-select" id="unidade" aria-label="Unidade"
                :placeholder="unidadePlaceholder" :class="{'is-invalid': !isUnidadeValida}" >
                <option disabled value="">{{ unidadePlaceholder }}</option>
                <option value="ton">Ton</option>
                <option value="kg">Kg</option>
                <option value="gr">gr</option>
                <option value="Lt">Lt</option>
                <option value="ml">ml</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-list-alt"></i></span>
              <input v-model="formData.categoria" type="text" class="form-control" id="categoria"
                :placeholder="categoriaPlaceholder" :class="{'is-invalid': !isCategoriaValida}" >
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
              <textarea v-model="formData.descricao" @input="aplicarDescricaoMask" class="form-control" id="descricao"
                placeholder="Descrição"></textarea>
              <div>({{ contadorDescricao }} / 255)</div> 
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('produtos')">Cancelar</button>
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
      activeTab: 'edicao', // Começa na aba de edição
      contadorDescricao: 0,
      produtosDaApi: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
        unidade: '',
      },
      isNomeValido: true,
      isTipoValido: true,
      isCategoriaValida: true,
      isUnidadeValida: true,
      nomePlaceholder: 'Nome*',
      tipoPlaceholder: 'Tipo*',
      categoriaPlaceholder: 'Categoria*',
      unidadePlaceholder: 'Unidade de medida*'
    };
  },

  mounted() {
    const produtoId = this.$route.params.produtoId;
    if (produtoId) {
      this.fetchProduto(produtoId);
    }
    this.buscarProdutosDaApi();
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarDescricaoMask(event){
      const value = event.target.value;
      this.formData.descricao = this.observacoesMask(value);
      this.contadorDescricao = this.formData.descricao.length;
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchProduto(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/produtos/${id}`);
        const produto = response.data;
        this.formData.id = produto.id;
        this.formData.nome = produto.nome;
        this.formData.tipo = produto.tipo;
        this.formData.categoria = produto.categoria;
        this.formData.descricao = produto.descricao;
        this.formData.unidade = produto.unidade;
        
        if(this.formData.descricao){
          this.contadorDescricao = this.formData.descricao.length;
        }
      } catch (error) {
        console.error('Erro ao carregar dados da produto:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/produtos');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/' , {
        });
        this.produtosDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //NOME DO PRODUTO
      if(this.formData.nome != null){
        if(this.formData.nome.trim() != ''){
          this.isNomeValido = true;
          this.nomePlaceholder = 'Nome do Produto';
        }
        else{
          this.isNomeValido = false;
          this.nomePlaceholder = 'Nome do Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome do Produto é um Campo Obrigatório';
      }

      //TIPO DO PRODUTO
      if(this.formData.tipo != null){
        if(this.formData.tipo != ''){
          this.isTipoValido = true;
          this.tipoPlaceholder = 'Tipo do Produto';
        }
        else{
          this.isTipoValido = false;
          this.tipoPlaceholder = 'Tipo do Produto é um Campo Obrigatório'
        }
      }
      else{
        this.isTipoValido = false;
        this.tipoPlaceholder = 'Tipo do Produto é um Campo Obrigatório'
      }

      //DESCRIÇÃO
      if(this.formData.descricao != null && this.formData.descricao.trim() == ''){
        this.formData.descricao = null;
      }

      //CATEGORIA
      if(this.formData.categoria != null && this.formData.categoria.trim() == ''){
        this.formData.categoria = null;
      }

      //UNIDADE
      if(this.formData.unidade != null){
        if(this.formData.unidade != ''){
          this.isUnidadeValida = true;
          this.unidadePlaceholder = 'Unidade de medida*';
        }
        else{
          this.isUnidadeValida = false;
          this.unidadePlaceholder = 'Unidade de medida é um Campo Obrigatório';
        }
      }
      else{
        this.isUnidadeValida = false;
        this.unidadePlaceholder = 'Unidade de medida é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isTipoValido && 
        this.isCategoriaValida &&
        this.isUnidadeValida
      );
    },

    validarFormulario() {
      let valido = true;
      this.isNomeValido = true;
      this.nomePlaceholder = 'Nome do Produto';
      
      // Cria uma nova lista sem o item com o id atual
      let produtosComExclusao = this.produtosDaApi.filter(produto => produto.id !== this.formData.id);

      // Verifica se o nome do produto já existe na lista
      for (let i = 0; i < produtosComExclusao.length; i++) {
        if (produtosComExclusao[i].nome === this.formData.nome) {
          this.isNomeValido = false;
          this.nomePlaceholder = 'Este Produto já está cadastrado';
          this.formData.nome = null;
          valido = false;
          break;
        }
      }
      
      return valido;
    },



//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'produtos') {
        this.$router.push('/produtos');
      }
    },

    cancelarEdicao() {
      this.$router.push('/produtos');
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

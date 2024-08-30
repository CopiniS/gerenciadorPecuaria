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
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <label for="dataInicial" class="input-group-text" title="Data Inicial"><i class="fas fa-calendar-alt"></i></label>
              <input type="text" :class="{ 'is-invalid': !isDataInicialValida }" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataInicialPlaceholder" class="form-control"
                id="dataInicialCadastro" v-model="formData.dataInicial" title="Data Inicial">
            </div>
            <div ref="dropdownProduto" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsProduto('up')"
              @keydown.down.prevent="navigateOptionsProduto('down')" @keydown.enter.prevent="selectHighlightedProduto">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownProduto">
                <span class="input-group-text" title="Produto"><i class="fas fa-box"></i></span>
                <input v-model="nomeProduto" :class="{ 'is-invalid': !isProdutoValido }" @input="inputProduto"
                  @keydown.up.prevent="navigateOptionsProduto('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsProduto('down')" type="text" class="form-control"
                  :placeholder="produtoPlaceholder" id="caixa-select" title="Produto">
              </div>
              <div class="itens" v-show="dropdownProdutoOpen">
                <ul class="options">
                  <li v-for="(produto, index) in produtosFiltrados" :key="produto.id" :value="produto.id"
                    @click="selectProduto(produto)" :class="{ 'highlighted': index === highlightedIndexProduto }">{{
                    produto.nome }}</li>
                </ul>
              </div>
            </div>
            <div ref="dropdownPiquete" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsPiquete('up')"
            @keydown.down.prevent="navigateOptionsPiquete('down')" @keydown.enter.prevent="selectHighlightedPiquete">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownPiquete">
                <span class="input-group-text" title="Piquete"><i class="fas fa-box"></i></span>
                <input v-model="nomePiquete" :class="{ 'is-invalid': !isPiqueteValido }" @input="inputPiquete"
                  @click="filterPiquetes" @keydown.up.prevent="navigateOptionsPiquete('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsPiquete('down')" type="text" class="form-control"
                  :placeholder="piquetePlaceholder" id="caixa-select" title="Piquete">
              </div>
              <div class="itens" v-show="dropdownPiqueteOpen">
                <ul class="options">
                  <li v-for="(piquete, index) in piquetesFiltrados" :key="piquete.id" :value="piquete.id"
                    @click="selectPiquete(piquete)" :class="{ 'highlighted': index === highlightedIndexPiquete }">{{
                    piquete.nome }}</li>
                </ul>
              </div>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Quantidade do Produto"><i class="fas fa-boxes"></i></span>
              <input v-model="formData.quantidade" type="text" :class="{ 'is-invalid': !isQuantidadeValida }"
                @input="aplicarQuantidadeMask" class="form-control" id="quantidade" autocomplete="off"
                :placeholder="quantidadePlaceholder" title="Quantidade do Produto">
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
      produtosFiltrados: [],
      piquetesFiltrados: [],
      nomeProduto: '',
      nomePiquete: '',
      highlightedIndexProduto: -1,
      dropdownProdutoOpen: false,
      highlightedIndexPiquete: -1,
      dropdownPiqueteOpen: false,
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
      produtoPlaceholder: 'Produto*',
      piquetePlaceholder: 'Piquete*',
      quantidadePlaceholder: 'Quantidade do Produto*',
      dataInicialPlaceholder: 'Data Inicial*',
    };
  },

  mounted() {
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
    document.addEventListener('click', this.handleClickOutsideProduto);
    document.addEventListener('click', this.handleClickOutsidePiquete);
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
        const response = await api.get('http://127.0.0.1:8000/piquetes/' , {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
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


//LÓGICA DOS SELECT PRODUTO----------------------------------------------------------------------------------------------------------------------------------------------------
    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto.toLowerCase()));
    },

    selectProduto(produto) {
      this.nomeProduto = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
      this.dropdownProdutoOpen = false;
    },

    toggleDropdownProduto() {
      this.dropdownProdutoOpen = !this.dropdownProdutoOpen;
      let nomeCorreto = false;

      if(!this.dropdownProdutoOpen){
        this.produtosFiltrados.forEach(produto => {
          if(produto.nome.toLowerCase() === this.nomeProduto.toLowerCase()){
            this.nomeProduto = produto.nome;
            this.formData.produto = produto.id;
            this.produtosFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomeProduto = '';
        }
      }

      else if(this.dropdownPiqueteOpen){
        this.piquetes.forEach(piquete => {
          if(piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()){
            this.formData.piquete = piquete.id;
            this.piquetesFiltrados = [];
            nomeCorreto = true;
            
          }
        });
        if(!nomeCorreto){
          this.formData.piquete = null;
          this.nomePiquete = ''
        }
        this.dropdownPiqueteOpen = false;
        this.filterProdutos();
      }

      else{
        this.filterProdutos();
      }
    },

    handleClickOutsideProduto(event) {
      if (this.dropdownProdutoOpen && this.$refs.dropdownProduto && !this.$refs.dropdownProduto.contains(event.target)) {
        let nomeCorreto = false;
        this.produtos.forEach(produto => {
          if(produto.nome.toLowerCase() === this.nomeProduto.toLowerCase()){
            this.nomeProduto = produto.nome;
            this.formData.produto = produto.id;
            this.produtosFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.produto = null;
          this.nomeProduto = '';
        }
        this.dropdownProdutoOpen = false;
      }
    },

    inputProduto(){
      this.filterProdutos();
      this.dropdownProdutoOpen = true;
    },

    navigateOptionsProduto(direction) {
      if (direction === 'up' && this.highlightedIndexProduto > 0) {
        this.highlightedIndexProduto--;
      } else if (direction === 'down' && this.highlightedIndexProduto < this.produtosFiltrados.length - 1) {
        this.highlightedIndexProduto++;
      }
    },

    selectHighlightedProduto() {
      if (this.highlightedIndexProduto >= 0 && this.highlightedIndexProduto < this.produtosFiltrados.length) {
        this.selectProduto(this.produtosFiltrados[this.highlightedIndexProduto]);
      }
    },


//LÓGICA DOS SELECT PIQUETE----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetes() {
      this.piquetesFiltrados = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete.toLowerCase()));
    },

    selectPiquete(piquete) {
      this.nomePiquete = piquete.nome;
      this.formData.piquete = piquete.id;
      this.piquetesFiltrados = [];
      this.dropdownPiqueteOpen = false;
      this.highlightedIndexPiquete = -1; // Reseta o índice após a seleção
    },

    toggleDropdownPiquete() {
      this.dropdownPiqueteOpen = !this.dropdownPiqueteOpen;
      let nomeCorreto = false;

      if(!this.dropdownPiqueteOpen){
        this.piquetesFiltrados.forEach(piquete => {
          if(piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()){
            this.nomePiquete = piquete.nome;
            this.formData.piquete = piquete.id;
            this.piquetesFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomePiquete = '';
        }
      }
      else if(this.dropdownProdutoOpen){
        this.produtos.forEach(produto => {
          if(produto.nome.toLowerCase() === this.nomeProduto.toLowerCase()){
            this.formData.produto = produto.id;
            this.produtosFiltrados = [];
            nomeCorreto = true;
            
          }
        });
        if(!nomeCorreto){
          this.formData.piquete = null;
          this.nomeProduto = ''
        }
        this.dropdownProdutoOpen = false;
        this.filterPiquetes();
      }

      else{
        this.filterPiquetes();
      }
    },

    handleClickOutsidePiquete(event) {
      let nomeCorreto = false;
      if (this.dropdownPiqueteOpen && this.$refs.dropdownPiquete && !this.$refs.dropdownPiquete.contains(event.target)) {
        this.piquetes.forEach(piquete => {
          if(piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()){
            this.selectPiquete(piquete);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomePiquete = '';
        }
      }
      this.dropdownPiqueteOpen = false;
    },

    inputPiquete() {
    this.filterPiquetes();
    this.dropdownPiqueteOpen = true;
    this.highlightedIndexPiquete = 0; // Inicia o índice ao começar a digitação
  },

    navigateOptionsPiquete(direction) {
    if (direction === 'up' && this.highlightedIndexPiquete > 0) {
      this.highlightedIndexPiquete--;
    } else if (direction === 'down' && this.highlightedIndexPiquete < this.piquetesFiltrados.length - 1) {
      this.highlightedIndexPiquete++;
    }
  },

  selectHighlightedPiquete() {
    if (this.highlightedIndexPiquete >= 0 && this.highlightedIndexPiquete < this.piquetesFiltrados.length) {
      this.selectPiquete(this.piquetesFiltrados[this.highlightedIndexPiquete]);
    }
  },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA INICIAL
      if(this.formData.dataInicial != null){
        if(this.formData.dataInicial.trim() != ''){
          this.isDataInicialValida = true;
          this.dataInicialPlaceholder = 'Data Inicial*';
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
          this.produtoPlaceholder = 'Produto*';
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
          this.piquetePlaceholder = 'Piquete*';
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
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
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

.select-option {
  width: 100%;
  cursor: pointer;
}

.itens {
  position: absolute;
  background-color: #fff;
  color: #000;
  border: 1px solid #ccc;
  border-radius: 7px;
  width: 100%;
  margin-top: 40px;
  z-index: 999;
  padding: 20px;
}

.options {
  max-height: 200px;
  /* Ajuste a altura conforme necessário */
  overflow-y: auto;
  border: 1px solid #ddd;
  margin: 0;
  padding: 0;
  list-style: none;
}

.options li {
  padding: 10px;
  cursor: pointer;
}

.options li:hover {
  background-color: #f0f0f0;
}

.select{
  margin-bottom: 0px !important;
}
</style>

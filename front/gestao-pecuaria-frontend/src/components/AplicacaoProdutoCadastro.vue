<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'aplicacoes' }" id="nav-vet-tab"
          @click="selectTab('aplicacoes')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista
          de Aplicação</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Aplicação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Aplicação</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder"
                class="form-control" id="dataAplicacaoCadastro" v-model="formData.dataAplicacao"
                :class="{ 'is-invalid': !isDataValida }" title="Data">
            </div>
            <div ref="dropdownProduto" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsProduto('up')"
              @keydown.down.prevent="navigateOptionsProduto('down')" @keydown.enter.prevent="selectHighlightedProduto">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownProduto">
                <span class="input-group-text" title="Produto"><i class="fas fa-box"></i></span>
                <input v-model="nomeProduto" :class="{ 'is-invalid': !isProdutoValido }" @input="inputProduto"
                  @click="filterProdutos" @keydown.up.prevent="navigateOptionsProduto('up')"
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
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Dosagem"><i class="fas fa-tint"></i></span>
              <input v-model="formData.dosagem" @input="aplicarDosagemMask" type="text" class="form-control"
                id="dosagem" :placeholder="dosagemPlaceholder" :class="{ 'is-invalid': !isDosagemValida }" 
                title="Dosagem">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Observação"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacao" 
              type="text" class="form-control" id="observacao" 
              placeholder="Observação" title="Observação">
              
            </div>

            <div ref="dropdownPiquete" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsPiquete('up')"
            @keydown.down.prevent="navigateOptionsPiquete('down')" @keydown.enter.prevent="selectHighlightedPiquete">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownPiquete">
                <span class="input-group-text" title="Piquete dos Animais aplicados"><i class="fas fa-box"></i></span>
                <input v-model="nomePiquete" :class="{ 'is-invalid': !isPiqueteValido }" @input="inputPiquete"
                  @click="filterPiquetes" @keydown.up.prevent="navigateOptionsPiquete('up')"
                  @keydown.down.prevent="navigateOptionsPiquete('down')" type="text" class="form-control"
                  :placeholder="piquetePlaceholder" id="caixa-select" title="Piquete dos Animais aplicados">
              </div>
              <div class="itens" v-show="dropdownPiqueteOpen">
                <ul class="options">
                  <li v-for="(piquete, index) in piquetesFiltrados" :key="piquete.id" :value="piquete.id"
                    @click="selectPiquete(piquete)" :class="{ 'highlighted': index === highlightedIndexPiquete }">{{
                    piquete.nome }}</li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group" v-if="animaisFiltrados.length != 0">
              <div class="checkbox-container">
                <label v-if="animaisFiltrados.length != 0">
                <input type="checkbox" v-model="selecionaTodos" @change="ativaSelecaoTodos"> Selecionar todos
              </label>
              <hr>
                <label @change="desativaSelecaoTodos" v-for="animal in animaisOrdenados" :key="animal.id">
                  <input type="checkbox" :value="animal.id" v-model="formData.animal"> {{ animal.brinco }} 
                </label>
              </div>
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
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      produtos: [],
      produtosFiltrados: [],
      nomeProduto: '',
      piquetes: [],
      nomePiquete: '',
      piqueteId: null,
      piquetesFiltrados: [],
      selecionaTodos: false,
      highlightedIndexProduto: -1,
      dropdownProdutoOpen: false,
      highlightedIndexPiquete: -1,
      dropdownPiqueteOpen: false,
      formData: {
        id: null,
        produto: null,
        animal: [],
        dosagem: null,
        dataAplicacao: null,
        observacao: null,
      },
      isBrincoValido: true,
      isDataValida: true,
      isPiqueteValido: true,
      isDosagemValida: true,
      isObservacaoValida: true,
      isProdutoValido: true,
      dataPlaceholder: 'Data*',
      piquetePlaceholder: 'Piquete*',
      dosagemPlaceholder: 'Dosagem* (ml/gr)',
      produtoPlaceholder: 'Produto*',
    };
  },
  computed: {
    animaisOrdenados() {
        return this.animaisFiltrados.slice().sort((a, b) => a.brinco.localeCompare(b.brinco));
    }
},

  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
    document.addEventListener('click', this.handleClickOutsideProduto);
    document.addEventListener('click', this.handleClickOutsidePiquete);
  },
  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarDosagemMask(event) {
      const value = event.target.value;
      this.formData.dosagem = this.valorMask(value);
    },

    aplicarBrincoMask(value) {
      this.brinco = this.brincoMask(value);
    },

    inputBrinco(event) {
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
    },


    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
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

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/com-animais', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/sanitarios', {});
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        if(this.verificaVazioAnimais()){
          //FORMATA DOSAGEM
          this.formData.dosagem = this.replaceVirgulaPonto(this.formData.dosagem)

          try {
            const response = await api.post('http://127.0.0.1:8000/aplicacoes-produtos/', this.formData, {
            });

            if (response.status === 201) {
              alert('Cadastro realizado com sucesso!');
              this.$router.push('/aplicacoes-produtos');
            } else {
              alert('Erro ao cadastrar aplicacao. Tente novamente mais tarde.');
            }
          } catch (error) {
            console.error('Erro ao enviar requisição:', error);
            alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
          }
        }
        else{
          alert('Nenhum animal foi selecionado');
        }
      }
    },


    //LÓGICA DOS SELECT PIQUETE----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetes() {
      this.piquetesFiltrados = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete.toLowerCase()));
    },

    selectPiquete(piquete) {
    this.nomePiquete = piquete.nome;
    this.piqueteId = piquete.id;
    this.piquetesFiltrados = [];
    this.preencheCheckBox();

    this.dropdownPiqueteOpen = false;
    this.highlightedIndexPiquete = -1; // Reseta o índice após a seleção
  },

    toggleDropdownPiquete() {
      this.dropdownPiqueteOpen = !this.dropdownPiqueteOpen;
      let nomeCorreto = false;

      if(!this.dropdownPiqueteOpen){
        this.piquetesFiltrados.forEach(piquete => {
          if(piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()){
            this.selectPiquete(piquete);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomePiquete = '';
          this.piqueteId = null;
        }
      }

      else if(this.dropdownProdutoOpen){
        this.produtos.forEach(produto => {
          if(produto.nome === this.nomeProduto){
            this.selectProduto(produto);
            nomeCorreto = true;
            
          }
        });
        if(!nomeCorreto){
          this.formData.produto = null;
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
          this.animaisFiltrados = [];
        }
      }
      this.dropdownPiqueteOpen = false;
    },

    inputPiquete() {
      this.filterPiquetes();
      this.dropdownPiqueteOpen = true;
      this.highlightedIndexPiquete = 0; // Inicia o índice ao começar a digitação

      if (this.nomePiquete.trim() === '') {
        this.animaisFiltrados = [];
      }
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
          if(piquete.nome === this.nomePiquete){
            this.selectPiquete(piquete);
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


    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio() {
      //DATA DA APLICAÇÃO
      if (this.formData.dataAplicacao != null) {
        if (this.formData.dataAplicacao.trim() != '') {
          this.isDataValida = true;
          this.dataPlaceholder = 'Data*';
        }
        else {
          this.isDataValida = false;
          this.dataPlaceholder = 'Data é um Campo Obrigatório';
        }
      }
      else {
        this.isDataValida = false;
        this.dataPlaceholder = 'Data é um Campo Obrigatório';
      }

      //PIQUETE
      if (this.nomePiquete != null) {
        if (this.nomePiquete.trim() != '') {
          this.isPiqueteValido = true;
          this.piquetePlaceholder = 'Piquete* ';
        }
        else {
          this.isPiqueteValido = false;
          this.piquetePlaceholder = 'Piquete é um Campo Obrigatório';
        }
      }
      else {
        this.isPiqueteValido = false;
        this.piquetePlaceholder = 'Piquete é um Campo Obrigatório';
      }

      //PRODUTO
      if (this.nomeProduto != null) {
        if (this.nomeProduto.trim() != '') {
          this.isProdutoValido = true;
          this.produtoPlaceholder = 'Produto';
        }
        else {
          this.isProdutoValido = false;
          this.produtoPlaceholder = 'Produto é um Campo Obrigatório';
        }
      }
      else {
        this.isProdutoValido = false;
        this.produtoPlaceholder = 'Produto é um Campo Obrigatório';
      }

      //DOSAGEM
      if (this.formData.dosagem != null) {
        if (this.formData.dosagem.trim() != '') {
          this.isDosagemValida = true;
          this.dosagemPlaceholder = 'Dosagem*'
        }
        else {
          this.isDosagemValida = false;
          this.dosagemPlaceholder = 'Dosagem é um Campo Obrigatório';
        }
      }
      else {
        this.isDosagemValida = false;
        this.dosagemPlaceholder = 'Dosagem é um Campo Obrigatório';
      }

      //OBSERVAÇÕES
      if (this.formData.observacao != null && this.formData.observacao.trim() == '') {
        this.formData.observacao = null;
      }

      return (
        this.isDataValida &&
        this.isBrincoValido &&
        this.isPiqueteValido &&
        this.isProdutoValido &&
        this.isDosagemValida
      );
    },

    verificaVazioAnimais(){
      return (this.formData.animal.length > 0)
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },
    preencheCheckBox(){
      this.animaisFiltrados = this.animais.filter(animal => animal.piquete === this.piqueteId);
    },

    ativaSelecaoTodos(){
      this.formData.animal = [];
      if(this.selecionaTodos){
        this.animais.forEach(animal => {
          this.formData.animal.push(animal.id);
        });
      }
    },

    desativaSelecaoTodos(){
      this.selecionaTodos = false;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'aplicacoes') {
        this.$router.push('/aplicacoes-produtos');
      }
    },

    replaceVirgulaPonto(valorString) {
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


.checkbox-container {
    gap: 10px;
    border: 1px solid #6c757d;
    border-radius: 5px;
    padding: 20px;
    width: 40%; /* Largura do contêiner */
    height: 150px; /* Altura do contêiner */
    overflow-y: auto; /* Adiciona uma barra de rolagem se necessário */
}

.checkbox-container label {
    display: flex;
    align-items: center;
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
</style>

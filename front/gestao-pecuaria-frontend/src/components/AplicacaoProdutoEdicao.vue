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
            <div ref="dropdownAnimal" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsAnimal('up')"
              @keydown.down.prevent="navigateOptionsAnimal('down')" @keydown.enter.prevent="selectHighlightedAnimal">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownAnimal">
                <span class="input-group-text"><i class="fas fa-box"></i></span>
                <input v-model="brinco" :class="{ 'is-invalid': !isBrincoValido }" @input="inputBrinco"
                  @click="filterAnimais" @keydown.up.prevent="navigateOptionsAnimal('up')"
                  @keydown.down.prevent="navigateOptionsAnimal('down')" type="text" class="form-control"
                  :placeholder="brincoPlaceholder" id="caixa-select">
              </div>
              <div class="itens" v-show="dropdownAnimalOpen">
                <ul class="options">
                  <li v-for="(animal, index) in animaisFiltrados" :key="animal.id" :value="animal.id"
                    @click="selectAnimal(animal)" :class="{ 'highlighted': index === highlightedIndexAnimal }">{{
                    animal.brinco }}</li>
                </ul>
              </div>
            </div>
            <div ref="dropdownProduto" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsProduto('up')"
              @keydown.down.prevent="navigateOptionsProduto('down')" @keydown.enter.prevent="selectHighlightedProduto">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownProduto">
                <span class="input-group-text"><i class="fas fa-box"></i></span>
                <input v-model="nomeProduto" :class="{ 'is-invalid': !isProdutoValido }" @input="inputProduto"
                  @click="filterProdutos" @keydown.up.prevent="navigateOptionsProduto('up')"
                  @keydown.down.prevent="navigateOptionsProduto('down')" type="text" class="form-control"
                  :placeholder="produtoPlaceholder" id="caixa-select">
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
              <span class="input-group-text"><i class="fas fa-tint"></i></span>
              <input v-model="formData.dosagem" type="text" @input="aplicarDosagemMask" class="form-control" id="dosagem" :placeholder="dosagemPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
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
      contadorObservacoes: 0,
      highlightedIndexProduto: -1,
      dropdownProdutoOpen: false,
      highlightedIndexAnimal: -1,
      dropdownAnimalOpen: false,
      formData: {
        id: null,
        produto: '',
        animal: '',
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
      dataPlaceholder: 'Data da aplicação*',
      piquetePlaceholder: 'Piquete*',
      dosagemPlaceholder: 'Dosagem do produto (ml/gr)*',
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
    document.addEventListener('click', this.handleClickOutsideProduto);
    document.addEventListener('click', this.handleClickOutsideAnimal);
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarDosagemMask(event) {
      const value = event.target.value;
      this.formData.dosagem =  this.valorMask(value);
    },

    aplicarBrincoMask(value){
      this.brinco =  this.brincoFiltroMask(value);
    },

    aplicarObservacaoMask(event){
      const value = event.target.value;
      this.formData.observacao = this.observacoesMask(value);
      this.contadorObservacoes = this.formData.observacao.length;
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchAplicacao(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/aplicacoes-produtos/aplicacao/${id}`);
        const aplicacao = response.data;
        this.formData.id = aplicacao[0].id;
        this.formData.animal = aplicacao[0].animal.id;
        this.formData.dataAplicacao = aplicacao[0].dataAplicacao;
        this.formData.produto = aplicacao[0].produto.id;
        this.formData.dosagem = this.replacePontoVirgula(aplicacao[0].dosagem);
        this.formData.observacao = aplicacao[0].observacao;

        this.brinco = aplicacao[0].animal.brinco;
        this.nomeProduto = aplicacao[0].produto.nome;
      } catch (error) {
        console.error('Erro ao carregar dados da aplicacao:', error);
      }
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
        //FORMATA DOSAGEM
        this.formData.dosagem = this.replaceVirgulaPonto(this.formData.dosagem);

        try {
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

//LÓGICA DOS SELECT ANIMAL----------------------------------------------------------------------------------------------------------------------------------------------------
    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.includes(this.brinco));
    },

    selectAnimal(animal) {
        this.brinco = animal.brinco;
        this.formData.animal = animal.id;
        this.animaisFiltrados = [];
        this.dropdownAnimalOpen = false;
    },

    toggleDropdownAnimal() {
      this.dropdownAnimalOpen = !this.dropdownAnimalOpen;
      let nomeCorreto = false;

      if(!this.dropdownAnimalOpen){
        this.animaisFiltrados.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.brinco = '';
        }
      }
    },

    handleClickOutsideAnimal(event) {
      if (this.dropdownAnimalOpen && this.$refs.dropdownAnimal && !this.$refs.dropdownAnimal.contains(event.target)) {
        this.dropdownAnimalOpen = false;
      }
      let nomeCorreto = false;
      if(!this.dropdownAnimalOpen){
        this.animais.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.brinco = '';
        }
      }
    },

    inputBrinco(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
      this.dropdownAnimalOpen = true;
    },

    navigateOptionsAnimal(direction) {
      if (direction === 'up' && this.highlightedIndex > 0) {
        this.highlightedIndex--;
      } else if (direction === 'down' && this.highlightedIndex < this.animaisFiltrados.length - 1) {
        this.highlightedIndex++;
      }
    },

    selectHighlightedAnimal() {
      if (this.highlightedIndex >= 0 && this.highlightedIndex < this.animaisFiltrados.length) {
        this.selectAnimal(this.animaisFiltrados[this.highlightedIndex]);
      }
    },


//LÓGICA DOS SELECT ANIMAL----------------------------------------------------------------------------------------------------------------------------------------------------
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

      //OBSERVAÇÕES
      if(this.formData.observacao != null && this.formData.observacao.trim() == ''){
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


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    replacePontoVirgula(valorString){
      valorString = valorString.replace(".", ",");

      return valorString;
    },

    replaceVirgulaPonto(valorString){
      valorString = valorString.replace(",", ".");

      return valorString;
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

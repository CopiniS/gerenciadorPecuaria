<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicialCompra || loadingInicialProdutos" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'produtos' }" id="nav-produtos-tab"
          @click="selectTab('produtos')" type="button" role="tab" aria-controls="nav-produtos"
          aria-selected="true">Lista de Produtos</button>
        <button class="nav-link" :class="{ active: activeTab === 'compras' }" id="nav-vet-tab"
          @click="selectTab('compras')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Histórico
          de Compras</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Compra</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'produtos' }" id="nav-produtos" role="tabpanel"
        aria-labelledby="nav-produtos-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'compras' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Compra</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" :class="{ 'is-invalid': !isDataCompraValida }" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataCompraPlaceholder" class="form-control"
                id="dataCompraCadastro" v-model="formData.dataCompra" title="Data" autocomplete="off">
            </div>
            <div ref="dropdown" class="select mb-3 input-group" @keydown.up.prevent="navigateOptions('up')"
              @keydown.down.prevent="navigateOptions('down')" @keydown.enter.prevent="selectHighlightedProduto">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdown">
                <span class="input-group-text" @click="filterProdutos" title="Produto"><i class="fas fa-box"></i></span>
                <input v-model="nomeDigitado" :class="{ 'is-invalid': !isProdutoValido }" @input="inputProduto"
                  @click="filterProdutos" @keydown.up.prevent="navigateOptions('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptions('down')" type="text" class="form-control"
                  :placeholder="produtoPlaceholder" id="caixa-select" title="Produto">
              </div>
              <div class="itens" v-show="dropdownOpen">
                <ul class="options">
                  <li v-for="(produto, index) in produtosFiltrados" :key="produto.id" :value="produto.id"
                    @click="selectProduto(produto)" :class="{ 'highlighted': index === highlightedIndex }">{{
          produto.nome }}</li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group">
              <span class="input-group-text" title="Valor do Produto"><i class="fas fa-dollar-sign"></i></span>
              <input ref="valor" v-model="formData.valorUnitario" :class="{ 'is-invalid': !isValorUnitarioValido }" type="text"
                @input="aplicarValorMask" class="form-control" id="valorUnitario" autocomplete="off"
                :placeholder="valorUnitarioPlaceholder" title="Valor do Produto">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Quantidade do Produto"><i class="fas fa-boxes"></i></span>
              <input v-model="formData.quantidadeComprada" :class="{ 'is-invalid': !isQuantidadeCompradaValida }"
                type="text" @input="aplicarQuantidadeMask" class="form-control" id="quantidadeComprada" 
                :placeholder="quantidadeCompradaPlaceholder" title="Quantidade do Produto" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Validade do Produto"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" :class="{ 'is-invalid': !isValidadeValida }" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="validadePlaceholder" class="form-control" autocomplete="off"
                id="validadeCadastro" v-model="formData.validade" title="Validade do Produto">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Lote do Produto"><i class="fas fa-layer-group"></i></span>
              <input v-model="formData.lote" type="text" class="form-control" autocomplete="off"
                id="lote" :placeholder="lotePlaceholder" title="Lote do Produto">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('compras')">Cancelar</button>
              <button type="button" class="btn btn-success" @click="submitForm">Salvar</button>
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
import LoadSpinner from './LoadSpiner.vue';

export default {
  mixins: [masksMixin],

  components:{
    LoadSpinner,
  },

  data() {
    return {
      activeTab: 'edicao', // Começa na aba de edição
      produtos: [],
      produtosFiltrados: [],
      nomeDigitado: '',
      highlightedIndex: -1,
      dropdownOpen: false,
      loadingSubmit: false,
      loadingInicialCompra: true,
      loadingInicialProdutos: true,
      formData: {
        id: null,
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      isDataCompraValida: true,
      isProdutoValido: true,
      isValorUnitarioValido: true,
      isQuantidadeCompradaValida: true,
      isValidadeValida: true,
      dataCompraPlaceholder: 'Data*',
      produtoPlaceholder: 'Produto*',
      valorUnitarioPlaceholder: 'Valor do Produto*',
      quantidadeCompradaPlaceholder: 'Quantidade do Produto*',
      validadePlaceholder: 'Validade do produto*',
      lotePlaceholder: 'Lote do Produto',
    };
  },

  mounted() {
    const compraId = this.$route.params.compraId;
    if (compraId) {
      this.fetchCompra(compraId);
    }
    this.buscarProdutos();
    document.addEventListener('click', this.handleClickOutside);
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarValorMask(event) {
      const value = event.target.value;
      this.formData.valorUnitario =  this.valorMask(value);
    },
    
    aplicarQuantidadeMask(event) {
      const value = event.target.value;
      this.formData.quantidadeComprada =  this.digitosMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchCompra(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/compras-produtos/compra/${id}`);
        const compra = response.data;
        this.formData.id = compra[0].id;
        this.formData.dataCompra = compra[0].dataCompra;
        this.formData.produto = compra[0].produto.id;
        this.formData.valorUnitario = this.replacePontoVirgula(compra[0].valorUnitario);
        this.formData.quantidadeComprada = compra[0].quantidadeComprada;
        this.formData.validade = compra[0].validade;
        this.formData.lote = compra[0].lote;

        this.nomeDigitado = compra[0].produto.nome;

        this.loadingInicialCompra = false;
      } catch (error) {
        console.error('Erro ao carregar dados da compra:', error);
      }
    },

    async buscarProdutos() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/');
        this.produtos = response.data;
        this.loadingInicialProdutos = false;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        this.loadingSubmit = true;
        try {
          //FORMATA VALOR E QUANTIDADE
          this.formData.valorUnitario = this.replaceVirgulaPonto(this.formData.valorUnitario);

          const response = await api.patch(`http://127.0.0.1:8000/compras-produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            this.loadingSubmit = false;
            setTimeout(() => {
              alert('Alterações salvas com sucesso!');
              this.$router.push('/compraprodutos');
            }, 100)
          } else {
            this.loadingSubmit = false;
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          this.loadingSubmit = false;
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeDigitado.toLowerCase()));
    },

    selectProduto(produto) {
      this.nomeDigitado = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
      this.dropdownOpen = false;
    },

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
      let nomeCorreto = false;

      if(!this.dropdownOpen){
        this.produtosFiltrados.forEach(produto => {
          if(produto.nome.toLowerCase() === this.nomeDigitado.toLowerCase()){
            this.nomeDigitado = produto.nome;
            this.formData.produto = produto.id;
            this.produtosFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomeDigitado = '';
        }
      }
    },

    handleClickOutside(event) {
      if (this.dropdownOpen && this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.dropdownOpen = false;
        this.nomeDigitado = '';
      }
    },

    inputProduto(){
      this.filterProdutos();
      this.dropdownOpen = true;
    },

    navigateOptions(direction) {
      if (direction === 'up' && this.highlightedIndex > 0) {
        this.highlightedIndex--;
      } else if (direction === 'down' && this.highlightedIndex < this.produtosFiltrados.length - 1) {
        this.highlightedIndex++;
      }
    },

    selectHighlightedProduto() {
      if (this.highlightedIndex >= 0 && this.highlightedIndex < this.produtosFiltrados.length) {
        this.selectProduto(this.produtosFiltrados[this.highlightedIndex]);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DA COMPRA
      if(this.formData.dataCompra != null){
        if(this.formData.dataCompra.trim() != ''){
          this.isDataCompraValida = true;
          this.dataCompraPlaceholder = 'Data*';
        }
        else{
          this.isDataCompraValida = false;
          this.dataCompraPlaceholder = 'Data é um Campo Obrigatório';
        }
      }
      else{
        this.isDataCompraValida = false;
        this.dataCompraPlaceholder = 'Data é um Campo Obrigatório';
      }

      //PRODUTO DA COMPRADO
      if(this.nomeDigitado != null){
        if(this.nomeDigitado.trim() != ''){
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

      //VALOR DO PRODUTO
      if(this.formData.valorUnitario != null){
        if(this.formData.valorUnitario.trim() != ''){
          this.isValorUnitarioValido = true;
          this.valorUnitarioPlaceholder = 'Valor do Produto*';
        }
        else{
          this.isValorUnitarioValido = false;
          this.valorUnitarioPlaceholder = 'Valor do Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isValorUnitarioValido = false;
        this.valorUnitarioPlaceholder = 'Valor do Produto é um Campo Obrigatório';
      }

      //QUANTIDADE COMPRADA
      if(this.formData.quantidadeComprada != null){
        if(this.formData.quantidadeComprada != ''){
          this.isQuantidadeCompradaValida = true;
          this.quantidadeCompradaPlaceholder = 'Quantidade do Produto*';
        }
        else{
          this.isQuantidadeCompradaValida = false;
          this.quantidadeCompradaPlaceholder = 'Quantidade do Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isQuantidadeCompradaValida = false;
        this.quantidadeCompradaPlaceholder = 'Quantidade do Produto é um Campo Obrigatório';
      }

      //VALIDADE DO PRODUTO
      if(this.formData.validade != null){
        if(this.formData.validade.trim() != ''){
          this.isValidadeValida = true;
          this.validadePlaceholder = 'Validade do Produto*';
        }
        else{
          this.isValidadeValida = false;
          this.validadePlaceholder = 'Validade do Produto é um Campo Obrigatório';
        }
      }
      else{
        this.isValidadeValida = false;
        this.validadePlaceholder = 'Validade do Produto é um Campo Obrigatório';
      }

      //LOTE DO PRODUTO
      if(this.formData.lote != null){
        if(this.formData.lote.trim() == ''){
          this.formData.lote = null;
        }
      }

      return(
        this.isDataCompraValida &&
        this.isProdutoValido &&
        this.isValorUnitarioValido && 
        this.isQuantidadeCompradaValida && 
        this.isValidadeValida
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
      if (tab === 'compras') {
        this.$router.push('/compraprodutos');
      }
      if (tab === 'produtos') {
        this.$router.push('/produtos');
      }
    },

    cancelarEdicao() {
      this.$router.push('/compraprodutos');
    },

    replacePontoVirgula(valorString){
      valorString = valorString.replace(".", ",");

      return valorString;
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
  /* Um tom mais escuro que o branco */
  min-height: 100vh;
  /* Garante que o fundo cubra toda a altura da tela */
  padding: 20px;
}

.table-container {
  margin-left: 20px;
  margin-right: 20px;
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
  /* Cor de fundo das células da tabela */
}

.table-container table tbody tr td {
  background-color: #f0f0f0;
  /* Cor de fundo das células da tabela */
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

#legenda {
    font-size: 16px;
}

.select{
  margin-bottom: 0px !important;
}

.highlighted {
  background-color: #f0f0f0;
}
</style>

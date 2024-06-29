<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'compras' }" id="nav-vet-tab" @click="selectTab('compras')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Histórico de Compra</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Compra</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'compras' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Compra</h1>
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input type="text" :class="{'is-invalid': !isDataCompraValida}" onfocus="(this.type='date')" onblur="(this.type='text')" 
                :placeholder="dataCompraPlaceholder" class="form-control" id="dataCompraCadastro" v-model="formData.dataCompra">
              </div>
              <div ref="dropdown" class="select mb-3 input-group">
                <div class="select-option mb-3 input-group" @click.stop="toggleDropdown">
                  <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                  <input v-model="nomeDigitado" :class="{'is-invalid': !isProdutoValido}" @input="filterProdutos" @click="filterProdutos()" type="text"
                    class="form-control" :placeholder="produtoPlaceholder" id="caixa-select">
                </div>
                <div class="itens" v-show="dropdownOpen">
                  <ul class="options">
                    <li v-for="produto in produtosFiltrados" :key="produto.id" :value="produto.id"
                      @click="selectProduto(produto)">{{ produto.nome }}</li>
                  </ul>
                </div>
              </div>

              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                <input v-model="formData.valorUnitario" :class="{'is-invalid': !isValorUnitarioValido}" type="number" class="form-control" id="valorUnitario"
                  :placeholder="valorUnitarioPlaceholder">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-boxes"></i></span>
                <input v-model="formData.quantidadeComprada" :class="{'is-invalid': !isQuantidadeCompradaValida}" type="number" class="form-control" id="quantidadeComprada"
                  :placeholder="quantidadeCompradaPlaceholder">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input type="text" :class="{'is-invalid': !isValidadeValida}" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="validadePlaceholder"
                  class="form-control" id="validadeCadastro" v-model="formData.validade" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-layer-group"></i></span>
                <input v-model="formData.lote" :class="{'is-invalid': !isLoteValido}" type="text" 
                class="form-control" id="lote" :placeholder="lotePlaceholder">
              </div>
              <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('compras')">Cancelar</button>
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

export default {
  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      produtos: [],
      produtosFiltrados: [],
      nomeDigitado: '',
      dropdownOpen: false,
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
      isLoteValido: true,
      dataCompraPlaceholder: 'Data da Compra',
      produtoPlaceholder: 'Produto',
      valorUnitarioPlaceholder: 'Valor do Produto',
      quantidadeCompradaPlaceholder: 'Quantidade Comprada',
      validadePlaceholder: 'Validade do produto',
      lotePlaceholder: 'Lote do Produto',
    };
  },

  mounted() {
    this.buscarProdutos();
    document.addEventListener('click', this.handleClickOutside);
  },
  
  methods: {

    async buscarProdutos() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    toggleDropdown() {
        this.dropdownOpen = !this.dropdownOpen;
    },

    handleClickOutside(event) {
        if (this.dropdownOpen && !this.$refs.dropdown.contains(event.target)) {
            this.dropdownOpen = false;
            this.nomeDigitado = '';
        }
    },
    

    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeDigitado));
    },
    selectProduto(produto) {
      this.nomeDigitado = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
      this.dropdownOpen = false;
    },

    validarFormulario(){
        //AQUI FALTA FAZER A VALIDAÇÂO. VER PAGINA DE VETERINARIOS
        return true;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'compras') {
        this.$router.push('/compraprodutos');
      }
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/compras-produtos/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.$router.push('/compraprodutos');
          } else {
            alert('Erro ao cadastrar compra. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
    },

    resetForm() {
      this.formData = {
        id: null,
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      this.isDataCompraValido = true,
      this.isProdutoValido = true,
      this.isValorUnitarioValido = true,
      this.isQuantidadeCompradaValida = true,
      this.isValidadeValida = true,
      this.isLoteValido = true,
      this.dataCompraPlaceholder = 'Data da Compra',
      this.produtoPlaceholder = 'Produto',
      this.valorUnitarioPlaceholder = 'Valor do Produto',
      this.quantidadeCompradaPlaceholder = 'Quantidade Comprada',
      this.validadePlaceholder = 'Validade do produto',
      this.lotePlaceholder = 'Lote do Produto'
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
</style>
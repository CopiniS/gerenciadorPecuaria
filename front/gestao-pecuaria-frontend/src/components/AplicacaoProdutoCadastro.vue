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
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder"
                class="form-control" id="dataAplicacaoCadastro" v-model="formData.dataAplicacao"
                :class="{ 'is-invalid': !isDataValida }">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-box"></i></span>
              <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control"
                :placeholder="produtoPlaceholder" :class="{ 'is-invalid': !isProdutoValido }">
            </div>
            <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados"
                :key="produto.id" @click="selectProduto(produto)">
                {{ produto.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tint"></i></span>
              <input v-model="formData.dosagem" @input="aplicarDosagemMask" type="text" class="form-control"
                id="dosagem" :placeholder="dosagemPlaceholder" :class="{ 'is-invalid': !isDosagemValida }">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacao" 
              @input="aplicarObservacaoMask" type="text" class="form-control" id="observacao" :placeholder="observacaoPlaceholder">
              <div class="character-counter">({{ contadorObservacoes }} / 255)</div>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="nomePiquete" @input="filtrarPiquetes" type="text" class="form-control"
                :placeholder="piquetePlaceholder" :class="{ 'is-invalid': !isPiqueteValido }">
            </div>
            <div class="list-group" v-if="nomePiquete && piquetesFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="piquete in piquetesFiltrados"
                :key="piquete.id" @click="selectPiquete(piquete)">
                {{ piquete.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <label v-if="animaisFiltrados.length != 0">
                <input type="checkbox" v-model="selecionaTodos" @change="ativaSelecaoTodos"> Selecionar todos
              </label>
              <div class="checkbox-container">
                <label @change="desativaSelecaoTodos" v-for="animal in animaisFiltrados" :key="animal.id">
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
      contadorObservacoes: 0,
      selecionaTodos: false,
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
      brincoPlaceholder: 'Brinco do animal*',
      dataPlaceholder: 'Data da aplicação*',
      piquetePlaceholder: 'Piquete*',
      dosagemPlaceholder: 'Dosagem do produto (ml/gr)*',
      observacaoPlaceholder: 'Observação',
      produtoPlaceholder: 'Produto*',
    };
  },

  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
  },
  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarDosagemMask(event) {
      const value = event.target.value;
      this.formData.dosagem = this.valorMask(value);
    },

    aplicarObservacaoMask(event) {
      const value = event.target.value;
      this.formData.observacao = this.observacoesMask(value);
      this.contadorObservacoes = this.formData.observacao.length;
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
    },


    //LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filtrarPiquetes() {
      this.piquetesFiltrados = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete));
    },

    selectPiquete(piquete) {
      this.piqueteId = piquete.id;
      this.nomePiquete = piquete.nome;
      this.piquetesFiltrados = [];
      this.preencheCheckBox()
    },

    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },

    selectProduto(produto) {
      this.nomeProduto = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
    },


    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio() {
      //DATA DA APLICAÇÃO
      if (this.formData.dataAplicacao != null) {
        if (this.formData.dataAplicacao.trim() != '') {
          this.isDataValida = true;
          this.dataPlaceholder = 'Digite a Data da Aplicação';
        }
        else {
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Aplicação é um Campo Obrigatório';
        }
      }
      else {
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Aplicação é um Campo Obrigatório';
      }

      //BRINCO || PIQUETE
      if (this.radioEscolha == 'brinco') {
        if (this.brinco != null) {
          if (this.brinco.trim() != '') {
            this.isBrincoValido = true;
            this.brincoPlaceholder = 'Digite o brinco do animal';
          }
          else {
            this.isBrincoValido = false;
            this.brincoPlaceholder = 'Brinco é um Campo Obrigatório';
          }
        }
        else {
          this.isBrincoValido = false;
          this.brincoPlaceholder = 'Brinco é um Campo Obrigatório';
        }
      }
      else {
        if (this.nomePiquete != null) {
          if (this.nomePiquete.trim() != '') {
            this.isPiqueteValido = true;
            this.piquetePlaceholder = 'Digite o Piquete ';
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
      }

      //PRODUTO
      if (this.nomeProduto != null) {
        if (this.nomeProduto.trim() != '') {
          this.isProdutoValido = true;
          this.produtoPlaceholder = 'Digite o nome do Produto';
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
          this.dosagemPlaceholder = 'Digite a Dosagem do produto'
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


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
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

.position-relative {
  position: relative;
}

.character-counter {
  position: absolute;
  top: 35px;
  right: 10px;
  font-size: 12px;
  color: #6c757d;
}

.checkbox-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    border: 1px solid #000;
    padding: 20px;
    width: 100%; /* Largura do contêiner */
    height: 150px; /* Altura do contêiner */
    overflow-y: auto; /* Adiciona uma barra de rolagem se necessário */
}

.checkbox-container label {
    display: flex;
    align-items: center;
}
</style>

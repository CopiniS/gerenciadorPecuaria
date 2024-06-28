
<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'suplementacoes' }" id="nav-vet-tab"
          @click="selectTab('suplementacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Suplementações</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Suplementação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'suplementacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Suplementação</h1>
          <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <label for="dataInicial" class="input-group-text"><i class="fas fa-calendar-alt"></i></label>
                <input type="text" :class="{'is-invalid': !isDataInicialValida}" onfocus="(this.type='date')" onblur="(this.type='text')" 
                :placeholder="dataInicialPlaceholder" class="form-control" id="dataInicialCadastro" v-model="formData.dataInicial">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                <input v-model="nomeProduto" @input="filtrarProdutos" :class="{'is-invalid': !isProdutoValido}" type="text" class="form-control"
                  :placeholder="produtoPlaceholder">
              </div>
              <div class="list-group" v-if="nomeProduto && filteredProdutos.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="produto in filteredProdutos"
                  :key="produto.id" @click="selecionarProduto(produto)">
                  {{ produto.nome }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                <input v-model="nomePiquete" @input="filtrarPiquetes" :class="{'is-invalid': !isPiqueteValido}" type="text" class="form-control"
                  :placeholder="piquetePlaceholder">
              </div>
              <div class="list-group" v-if="nomePiquete && filteredPiquetes.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetes"
                  :key="piquete.id" @click="selecionarPiquete(piquete)">
                  {{ piquete.nome }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                <input v-model="formData.quantidade" type="number" :class="{'is-invalid': !isQuantidadeValida}" class="form-control" id="quantidade"
                  :placeholder="quantidadePlaceholder">
              </div>
              <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('suplementacoes')">Cancelar</button>
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

export default {
    data() {
        return {
            activeTab: 'edicao', // Começa na aba de edição
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
            produtoPlaceholder: 'Produto usado na Suplementação',
            piquetePlaceholder: 'Piquete da Suplementação',
            quantidadePlaceholder: 'Quantidade de produto',
            dataInicialPlaceholder: 'Data Inicial da Suplementação',
        };
    },
 
    mounted() {
        const suplementacaoId = this.$route.params.suplementacaoId;
        if (suplementacaoId) {
            this.fetchSuplementacao(suplementacaoId);
        }
        this.buscarProdutosDaApi();
        this.buscarPiquetesDaApi();
    },
    methods: {
    async fetchSuplementacao(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/suplementacoes/${id}`);
        const suplementacao = response.data;
        this.formData.id = suplementacao.id;
        this.formData.produto = suplementacao.produto;
        this.formData.piquete = suplementacao.piquete;
        this.formData.quantidade = suplementacao.quantidade;
        this.formData.dataInicial = suplementacao.dataInicial;
        this.formData.dataFinal = suplementacao.dataFinal;
        this.nomeProduto = suplementacao.produto.nome;
        this.nomePiquete = suplementacao.piquete.nome;
      } catch (error) {
        console.error('Erro ao carregar dados da suplementacao:', error);
      }
    },

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

    validarFormulario() {
      return true;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'suplementacoes') {
        this.$router.push('/suplementacoes');
      }
    },

    cancelarEdicao() {
      this.$router.push('/suplementacoes');
    },

    async submitForm() {
      if (this.validarFormulario()) {
       try {
          const response = await api.patch(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.$router.push('/suplementacoes');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    resetForm() {
      this.nomeProduto = '',
      this.nomePiquete = '',
      this.formData = {
        id: null,
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
      },
      this.isProdutoValido = true,
      this.isPiqueteValido = true,
      this.isQuantidadeValida = true,
      this.isDataInicialValida = true,
      this.produtoPlaceholder = 'Produto usado na Suplementação',
      this.piquetePlaceholder = 'Piquete da Suplementação',
      this.quantidadePlaceholder = 'Quantidade de produto',
      this.dataInicialPlaceholder = 'Data Inicial da Suplementação'
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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}
</style>

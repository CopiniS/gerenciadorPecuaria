<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'aplicacoes' }" id="nav-vet-tab" @click="selectTab('aplicacoes')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Aplicação</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Aplicação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacoes' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Aplicação</h1>
            <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                placeholder="Data da aplicação" class="form-control" id="dataAplicacaoCadastro"
                v-model="formData.dataAplicacao" required>
            </div>
            <div class="mb-3 input-group">
              <input type="radio" v-model="radioEscolha" value="brinco"> Brinco
            </div>
            <div class="mb-3 input-group">
              <input type="radio" v-model="radioEscolha" value="piquete"> Piquete
            </div>
            <div class="mb-3 input-group" v-if="radioEscolha === 'brinco'">
              <input v-model="brinco" @input="filterAnimais" type="text" class="form-control"
                placeholder="Digite o brinco...">
            </div>
            <div class="list-group" v-if="brinco && animaisFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados"
                :key="animal.id" @click="selectAnimal(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group" v-if="radioEscolha === 'piquete'">
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="nomePiquete" @input="filtrarPiquetes" type="text" class="form-control"
                placeholder="Digite o nome do piquete...">
            </div>
            <div class="list-group" v-if="nomePiquete && piquetesFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="piquete in piquetesFiltrados"
                :key="piquete.id" @click="selectPiquete(piquete)">
                {{ piquete.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control"
                placeholder="Digite o produto...">
            </div>
            <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                {{ produto.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.dosagem" type="text" class="form-control" id="dosagem"
                :disabled="!((camposHabilitadosPiquete || camposHabilitadosAnimal) && camposHabilitadosProduto)"
                placeholder="Dosagem" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.observacao" type="text" class="form-control" id="observacao"
                :disabled="!((camposHabilitadosPiquete || camposHabilitadosAnimal) && camposHabilitadosProduto)"
                placeholder="Observação">
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

export default {
  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      produtos: [],
      produtosFiltrados: [],
      nomeProduto: '',
      piquetes: [],
      nomePiquete: '',
      piqueteId: null,
      piquetesFiltrados: [],
      radioEscolha: 'brinco',
      formData: {
        id: null,
        produto: '',
        animal: [],
        dosagem: '',
        dataAplicacao: '',
        observacao: null,
      },
      isAnimalValido: true,
      isDataValida: true,
      isPiqueteValido: true,
      isDosagemValida: true,
      isObservacaoValida: true,
      animalPlaceholder: 'Brinco do animal',
      dataPlaceholder: 'Data da aplicacao',
      piquetePlaceholder: 'Piquete',
      dosagemPlaceholder: 'Dosagem do produto',
      observacaoPlaceholder: 'Observação',
    };
  },

    mounted() {
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
  },

  methods: {
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
      this.camposHabilitadosAnimal = true;
      this.animaisFiltrados = [];
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    filtrarPiquetes() {
      this.piquetesFiltrados = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete));
    },

    selectPiquete(piquete) {
      this.camposHabilitadosPiquete = true;
      this.piqueteId = piquete.id;
      this.nomePiquete = piquete.nome;
      this.piquetesFiltrados = [];
      this.preencheListaAnimais()
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
      this.camposHabilitadosProduto = true;
      this.produtosFiltrados = [];
    },

    preencheListaAnimais() {
      this.formData.animal = [];
      let listaAnimais;
      listaAnimais = this.animais.filter(animal => animal.piquete == this.piqueteId);
      listaAnimais.forEach(animal => {
        this.formData.animal.push(animal.id);
      });
    },

    validarFormulario() {
      return true;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'aplicacoes') {
        this.$router.push('/aplicacoes-produtos');
      }
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/aplicacoes-produtos/', this.formData , {
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

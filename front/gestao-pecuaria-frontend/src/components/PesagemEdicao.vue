<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'pesagens' }" id="nav-vet-tab"
          @click="selectTab('pesagens')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Pesagens</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Pesagem</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'pesagens' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Pesagem</h1>
          <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data de pesagem" 
                class="form-control" id="dataPesagemCadastro" v-model="formData.dataPesagem">
              </div>
              <hr>
              <div class="mb-3 input-group">
                <input v-model="brinco" @input="filterAnimais" type="text" class="form-control" placeholder="Digite o brinco...">
              </div>
              <div class="list-group" v-if="brinco && animaisFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                  {{ animal.brinco }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-weight"></i></span>
                <input v-model="formData.peso" type="text" class="form-control" id="peso" :disabled="!camposHabilitados " placeholder="Peso" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-comment"></i></span>
                <input v-model="formData.observacao" type="text" class="form-control" id="observacao" :disabled="!camposHabilitados" placeholder="Observação" required>
              </div>
              <div class="button-group justify-content-end">
                <button type="button" class="btn btn-secondary" @click="selectTab('pesagens')">Cancelar</button>
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
       animais: [],
      animaisFiltrados: [],
      brinco: '',
      camposHabilitados: false,
      formData: {
        id: null,
        dataPesagem: '',
        peso: '',
        observacao: null,
        animal: null
      },
      isAnimalValido: true,
      isDataValida: true,
      isPesoValido: true,
      isValorValido: true,
      animalPlaceholder: 'Brinco do animal',
      dataPlaceholder: 'Data da pesagem',
      pesoPlaceholder: 'Peso do animal',
      observacaoPlaceholder: 'Observação',
    };
  },

  mounted() {
    console.log('pesagemId: ', this.$route.params.pesagemId);
    const pesagemId = this.$route.params.pesagemId;
    if (pesagemId) {
      this.fetchPesagem(pesagemId);
    }
    this.buscarAnimaisDaApi();
  },
  methods: {
    async fetchPesagem(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/pesagens/pesagem/${id}`);
        const pesagem = response.data;
        this.formData.id = pesagem[0].id;
        this.formData.animal = pesagem[0].animal.id;
        this.formData.dataPesagem = pesagem[0].dataPesagem;
        this.formData.peso = pesagem[0].peso;
        this.formData.observacao = pesagem[0].observacao;

        this.brinco = pesagem[0].animal.brinco;
        this.dataSelecionada = pesagem[0].dataPesagem
        this.camposHabilitados = true;
      } catch (error) {
        console.error('Erro ao carregar dados da pesagem:', error);
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

    filterAnimais() {
        this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
        if(this.brinco === ''){
            this.camposHabilitados = false;
        }
    },

    selectAnimal(animal) {
      this.brinco = animal.brinco;
      this.formData.animal = animal.id;
      this.animaisFiltrados = [];
      this.camposHabilitados = true;
    },

    validarFormulario() {
        return true;
    },


    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'pesagens') {
        this.$router.push('/pesagens');
      }
    },

    cancelarEdicao() {
      this.$router.push('/pesagens');
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/pesagens/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.$router.push('/pesagens');
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
      this.formData = {
        id: null,
        dataPesagem: '',
        peso: '',
        observacao: '',
        animal: null
      },
      this.isAnimalValido = true,
      this.isDataValida = true,
      this.isPesoValido = true,
      this.isValorValido = true,
      this.animalPlaceholder = 'Brinco do animal',
      this.dataPlaceholder = 'Data da pesagem',
      this.pesoPlaceholder = 'Peso do animal',
      this.observacaoPlaceholder = 'Observação'
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

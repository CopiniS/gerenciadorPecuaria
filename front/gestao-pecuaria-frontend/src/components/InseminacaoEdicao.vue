<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'inseminacoes' }" id="nav-vet-tab"
          @click="selectTab('inseminacoes')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Inseminações</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Inseminação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'inseminacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Inseminação</h1>
          <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                  <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                    placeholder="Data da inseminação" class="form-control" id="dataInseminacaoCadastro"
                    v-model="formData.dataInseminacao">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                  <input v-model="nomeVet" @input="filterVeterinario" type="text" class="form-control"
                    placeholder="Digite o Veterinario">
                </div>
                <div class="list-group" v-if="nomeVet && veterinariosFiltrados.length">
                  <button type="button" class="list-group-item list-group-item-action"
                    v-for="veterinario in veterinariosFiltrados" :key="veterinario.id"
                    @click="selectVeterinario(veterinario)">
                    {{ veterinario.nome }}
                  </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                  <input v-model="formData.identificadorTouro" type="text" class="form-control" id="identificadorTouro"
                    placeholder="Indentificador Touro" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-venus"></i></span>
                  <input v-model="brinco" @input="filterFemeas()" type="text" class="form-control"
                    placeholder="Digite o animal">
                </div>
                <div class="list-group" v-if="brinco && femeasFiltradas.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                    :key="animal.id" @click="selectMae(animal)">
                    {{ animal.brinco }}
                  </button>
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('inseminacoes')">Cancelar</button>
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
      femeas: [],
      femeasFiltradas: [],
      brinco: '',
      veterinarios: [],
      veterinariosFiltrados: [],
      nomeVet: '',
      formData: {
        id: null,
        dataInseminacao: '',
        veterinario: '',
        animal: '',
        identificadorTouro: '',
      },
      isAnimalValido: true,
      isDataValida: true,
      isVeterinarioValido: true,
      isIdentificadorTouroValido: true,
      animalPlaceholder: 'Brinco do animal',
      dataPlaceholder: 'Data da inseminacao',
      veterinarioPlaceholder: 'Veterinário',
      identificadorTouroPlaceholder: 'Identificador do Touro',
    };
  },

  mounted() {
    const inseminacaoId = this.$route.params.inseminacaoId;
    if (inseminacaoId) {
      this.fetchInseminacao(inseminacaoId);
    }
    this.buscarFemeasVivasDaApi();
    this.buscarVeterinariossDaApi();
  },
  methods: {
    async fetchInseminacao(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/inseminacoes/inseminacao/${id}`);
        const inseminacao = response.data;
        this.formData.id = inseminacao[0].id;
        this.formData.animal = inseminacao[0].animal.id;
        this.formData.dataInseminacao = inseminacao[0].dataInseminacao;
        this.formData.veterinario = inseminacao[0].veterinario.id;
        this.formData.identificadorTouro = inseminacao[0].identificadorTouro;

        this.brinco = inseminacao[0].animal.brinco;
        this.nomeVet = inseminacao[0].veterinario.nome;
        this.dataSelecionada = inseminacao[0].dataInseminacao
      } catch (error) {
        console.error('Erro ao carregar dados da inseminacao:', error);
      }
    },

    async buscarFemeasVivasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/femeas/vivas', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.femeas = response.data;
      } catch (error) {
        console.error('Erro ao buscar inseminacoes da API:', error);
      }
    },

    filterFemeas() {
      this.femeasFiltradas = this.femeas.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectMae(animal) {
      this.formData.animal = animal.id;
      this.brinco = animal.brinco;
      this.femeasFiltradas = [];
    },

    async buscarVeterinariossDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/', {
        });
        this.veterinarios = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinarios da API:', error);
      }
    },
    filterVeterinario() {
      this.veterinariosFiltrados = this.veterinarios.filter(veterinario => veterinario.nome.toLowerCase().includes(this.nomeVet));
    },
    selectVeterinario(veterinario) {
      this.nomeVet = veterinario.nome;
      this.formData.veterinario = veterinario.id;
      this.veterinariosFiltrados = [];
    },

    validarFormulario() {
      return true;
    },


    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'inseminacoes') {
        this.$router.push('/inseminacoes');
      }
    },

    cancelarEdicao() {
      this.$router.push('/inseminacoes');
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
            console.log(this.formData);
          const response = await api.patch(`http://127.0.0.1:8000/inseminacoes/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.$router.push('/inseminacoes');
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
        dataInseminacao: '',
        veterinario: '',
        animal: '',
        identificadorTouro: '',
      },
      this.isAnimalValido = true,
      this.isDataValida = true,
      this.isVeterinarioValido = true,
      this.isIdentificadorTouroValido = true,
      this.animalPlaceholder = 'Brinco do animal',
      this.dataPlaceholder = 'Data da inseminacao',
      this.veterinarioPlaceholder = 'Veterinário',
      this.identificadorTouroPlaceholder = 'Identificador do Touro'
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

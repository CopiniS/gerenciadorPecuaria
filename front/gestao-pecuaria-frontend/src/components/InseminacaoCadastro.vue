<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'inseminacoes' }" id="nav-vet-tab"
          @click="selectTab('inseminacoes')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista
          de Inseminacao</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Inseminacao</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'inseminacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Inseminacao</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i></span>
              <input v-model="formData.dataInseminacao" :class="{'is-invalid': !isDataValida}" type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder" class="form-control" id="dataInseminacaoCadastro">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
              <input v-model="nomeVet" @input="filterVeterinario" type="text" class="form-control"
              :placeholder="veterinarioPlaceholder" :class="{'is-invalid': !isVeterinarioValido}">
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
              :placeholder="identificadorTouroPlaceholder" required :class="{'is-invalid': !isIdentificadorTouroValido}">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-venus"></i></span>
              <input v-model="brinco" @input="filterFemeas()" type="text" class="form-control"
              :placeholder="animalPlaceholder" :class="{'is-invalid': !isAnimalValido}">
            </div>

            <div class="list-group" v-if="brinco && femeasFiltradas.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                :key="animal.id" @click="selectMae(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('inseminacoes')">Cancelar</button>
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
import $ from 'jquery'; // Importe o jQuery aqui
import 'jquery-mask-plugin'; // Importe o plugin jQuery Mask Plugin

export default {
  data() {
    return {
      activeTab: 'cadastro',
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
      animalPlaceholder: 'Brinco do animal*',
      dataPlaceholder: 'Data da inseminacao*',
      veterinarioPlaceholder: 'Veterinário*',
      identificadorTouroPlaceholder: 'Identificador do Touro*',
    };
  },

  mounted() {
    this.buscarFemeasVivasDaApi();
    this.buscarVeterinariosDaApi();
    // Aplicando máscaras e validações
    $('#dataInseminacaoCadastro').mask('00/00/0000');
    $('#identificadorTouro').mask('000000000'); // Máscara para aceitar apenas números
    $('#vetInput').on('input', this.filterVeterinario); // Adicionando validação para aceitar apenas letras
    $('#animalInput').on('input', this.filterFemeas); // Adicionando validação para aceitar apenas letras
  },

  methods: {
    async buscarFemeasVivasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/femeas/vivas', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.femeas = response.data;
      } catch (error) {
        console.error('Erro ao buscar inseminações da API:', error);
      }
    },

    filterFemeas() {
      this.femeasFiltradas = this.femeas.filter(animal => /^\d+$/.test(animal.brinco) && animal.brinco.includes(this.brinco));
    },


    selectMae(animal) {
      // Seleciona a fêmea e limpa o campo de busca
      this.formData.animal = animal.id;
      this.brinco = animal.brinco;
      this.femeasFiltradas = [];
    },

    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/');
        this.veterinarios = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },

    filterVeterinario(event) {
      // Filtra veterinários com base no nome
      const inputValue = event.target.value.trim().replace(/[^a-zA-ZÀ-ÿ ]/g, ''); // Remove caracteres não alfabéticos
      this.nomeVet = inputValue;
      this.veterinariosFiltrados = this.veterinarios.filter(veterinario => {
        const regex = new RegExp(inputValue.toLowerCase());
        return regex.test(veterinario.nome.toLowerCase());
      });
    },

    selectVeterinario(veterinario) {
      // Seleciona o veterinário
      this.nomeVet = veterinario.nome;
      this.formData.veterinario = veterinario.id;
      this.veterinariosFiltrados = [];
    },

    validarFormulario() {
      this.isDataValida = !!this.formData.dataInseminacao.trim();
      if (!this.isDataValida) this.formData.dataInseminacao = '';

      this.isVeterinarioValido = !!this.formData.veterinario;
      if (!this.isVeterinarioValido) this.formData.veterinario = '';

      this.isAnimalValido = !!this.formData.animal;
      if (!this.isAnimalValido) this.formData.animal = '';

      this.isIdentificadorTouroValido = !!this.formData.identificadorTouro;
      if (!this.isIdentificadorTouroValido) this.formData.identificadorTouro = '';

      this.dataPlaceholder = this.isDataValida ? 'Data da Inseminação' : 'Campo Data da Inseminação é obrigatório';
      this.veterinarioPlaceholder = this.isVeterinarioValido ? 'Veterinário' : 'Campo Veterinário é obrigatório';
      this.animalPlaceholder = this.isAnimalValido ? 'Animal' : 'Campo Animal é obrigatório';
      this.identificadorTouroPlaceholder = this.isIdentificadorTouroValido ? 'Identificador do Touro' : 'Campo Identificador do Touro é obrigatório';

      return this.isDataValida && this.isVeterinarioValido && this.isAnimalValido && this.isIdentificadorTouroValido;
    },




    selectTab(tab) {
      // Seleciona a aba do formulário
      this.activeTab = tab;
      if (tab === 'inseminacoes') {
        this.$router.push('/inseminacoes');
      }
    },

    async submitForm() {
      // Submete o formulário
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/inseminacoes/', this.formData);
          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.$router.push('/inseminacoes');
          } else {
            alert('Erro ao cadastrar inseminação. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    resetForm() {
      // Reseta o formulário
      this.formData = {
        id: null,
        dataInseminacao: '',
        veterinario: '',
        animal: '',
        identificadorTouro: '',
      };
      this.isAnimalValido = true;
      this.isDataValida = true;
      this.isVeterinarioValido = true;
      this.isIdentificadorTouroValido = true;
      this.animalPlaceholder = 'Brinco do animal';
      this.dataPlaceholder = 'Data da inseminação';
      this.veterinarioPlaceholder = 'Veterinário';
      this.identificadorTouroPlaceholder = 'Identificador do Touro';
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
</style>

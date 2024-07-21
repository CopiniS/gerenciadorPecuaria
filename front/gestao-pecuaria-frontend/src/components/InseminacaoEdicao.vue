<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'inseminacoes' }" id="nav-vet-tab"
          @click="selectTab('inseminacoes')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista
          de Inseminacao</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Inseminacao</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'inseminacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Inseminacao</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i></span>
              <input v-model="formData.dataInseminacao" :class="{'is-invalid': !isDataValida}" type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder" class="form-control" id="dataInseminacaoEdicao">
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
              <input v-model="brinco" @input="inputBrinco" type="text" class="form-control"
              :placeholder="animalPlaceholder" :class="{'is-invalid': !isAnimalValido}">
            </div>

            <div class="list-group" v-if="brinco && femeasFiltradas.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                :key="animal.id" @click="selectMae(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-comment"></i></span>
                <input v-model="formData.observacao" type="text" @input="aplicarObservacaoMask" class="form-control" id="observacao" placeholder="Observação">
                <div>({{ contadorObservacoes }} / 255)</div>
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
import { masksMixin } from '../mixins/maks';

export default {
  mixins: [masksMixin],

  data() {
    return {
      activeTab: 'edicao',
      femeas: [],
      femeasFiltradas: [],
      brinco: '',
      veterinarios: [],
      veterinariosFiltrados: [],
      nomeVet: '',
      contadorObservacoes: 0,
      formData: {
        id: null,
        dataInseminacao: null,
        veterinario: null,
        animal: null,
        identificadorTouro: null,
        observacao: null,
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
    this.buscarVeterinariosDaApi();
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(value){
      this.brinco =  this.brincoMask(value);
    },

    inputBrinco(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterFemeas();
    },

    aplicarObservacaoMask(event){
      const value = event.target.value;
      this.formData.observacao = this.observacoesMask(value);
      this.contadorObservacoes = this.formData.observacao.length;
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchInseminacao(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/inseminacoes/inseminacao/${id}`);
        const inseminacao = response.data;
        this.formData.id = inseminacao[0].id;
        this.formData.dataInseminacao = inseminacao[0].dataInseminacao;
        this.formData.veterinario = inseminacao[0].veterinario.id;
        this.formData.animal = inseminacao[0].animal.id;
        this.formData.identificadorTouro = inseminacao[0].identificadorTouro;
        this.formData.observacao = inseminacao[0].observacao;
        
        this.brinco = inseminacao[0].animal.brinco;
        this.nomeVet = inseminacao[0].veterinario.nome;
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
        console.error('Erro ao buscar inseminações da API:', error);
      }
    },

    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/');
        this.veterinarios = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },

    async submitForm() {
      // Submete o formulário
      if (this.verificaVazio()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/inseminacoes/${this.formData.id}/`, this.formData);
          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/inseminacoes');
          } else {
            alert('Erro ao alterar inseminação. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filterFemeas() {
      this.femeasFiltradas = this.femeas.filter(animal => /^\d+$/.test(animal.brinco) && animal.brinco.includes(this.brinco));
    },

    selectMae(animal) {
      // Seleciona a fêmea e limpa o campo de busca
      this.formData.animal = animal.id;
      this.brinco = animal.brinco;
      this.femeasFiltradas = [];
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


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DA INSEMINAÇÃO
      if(this.formData.dataInseminacao != null){
        if(this.formData.dataInseminacao.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Digite a Data da Inseminação';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Inseminação é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Inseminação é um Campo Obrigatório';
      }

      //BRINCO
      if(this.brinco != null){
        if(this.brinco.trim() != ''){
          this.isAnimalValido = true;
          this.animalPlaceholder = 'Digite o brinco do Animal';
        }
        else{
          this.isAnimalValido = false;
          this.animalPlaceholder = 'Brinco do animal é um Campo Obrigatório';
        }
      }
      else{
        this.isAnimalValido = false;
        this.animalPlaceholder = 'Brinco do animal é um Campo Obrigatório';
      }

      //VETERINÁRIO
      if(this.nomeVet != null){
        if(this.nomeVet.trim() != ''){
          this.isVeterinarioValido = true;
          this.veterinarioPlaceholder = 'Digite o Veterinário';
        }
        else{
          this.isVeterinarioValido = false;
          this.veterinarioPlaceholder = 'Veterinário é um Campo Obrigatório'
        }
      }
      else{
        this.isVeterinarioValido = false;
        this.veterinarioPlaceholder = 'Veterinário é um Campo Obrigatório'
      }

      //IDENTIFICADOR TOURO
      if(this.formData.identificadorTouro != null){
        if(this.formData.identificadorTouro.trim() != ''){
          this.isIdentificadorTouroValido = true;
          this.identificadorTouroPlaceholder = 'Digite o Identificador do Touro';
        }
        else{
          this.isIdentificadorTouroValido = false;
          this.identificadorTouroPlaceholder = 'Identificador Touro é um Campo Obrigatório';
        }
      }
      else{
          this.isIdentificadorTouroValido = false;
          this.identificadorTouroPlaceholder = 'Identificador Touro é um Campo Obrigatório';
      }

      //OBSERVAÇÃO
      if(this.formData.observacao != null && this.formData.observacao.trim() == ''){
        this.formData.observacao = null;
      }

      return (
        this.isDataValida &&
        this.isAnimalValido && 
        this.isVeterinarioValido && 
        this.isIdentificadorTouroValido
      );
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      // Seleciona a aba do formulário
      this.activeTab = tab;
      if (tab === 'inseminacoes') {
        this.$router.push('/inseminacoes');
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

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}
</style>

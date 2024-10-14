<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicialFemeas || loadingInicialVeterinarios" />
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
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <input v-model="formData.dataInseminacao" :class="{ 'is-invalid': !isDataValida }" type="text"
                onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder"
                class="form-control" id="dataInseminacaoCadastro" title="Data">
            </div>
            <div ref="dropdownVeterinario" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsVeterinario('up')"
              @keydown.down.prevent="navigateOptionsVeterinario('down')" @keydown.enter.prevent="selectHighlightedVeterinario">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownVeterinario">
                <span class="input-group-text" title="Veterinario"><i class="fas fa-box"></i></span>
                <input v-model="nomeVeterinario" :class="{ 'is-invalid': !isVeterinarioValido }" @input="inputVeterinario"
                  @keydown.up.prevent="navigateOptionsVeterinario('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsVeterinario('down')" type="text" class="form-control"
                  :placeholder="veterinarioPlaceholder" id="caixa-select" title="Veterinario">
              </div>
              <div class="itens" v-show="dropdownVeterinarioOpen">
                <ul class="options">
                  <li v-for="(veterinario, index) in veterinariosFiltrados" :key="veterinario.id" :value="veterinario.id"
                    @click="selectVeterinario(veterinario)" :class="{ 'highlighted': index === highlightedIndexVeterinario }">{{
                    veterinario.nome }}</li>
                </ul>
              </div>
            </div>
            <div class="list-group" v-if="nomeVeterinario && veterinariosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="veterinario in veterinariosFiltrados" :key="veterinario.id"
                @click="selectVeterinario(veterinario)">
                {{ veterinario.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Identificador do Touro"><i class="fas fa-id-card"></i></span>
              <input v-model="formData.identificadorTouro" type="text" class="form-control" id="identificadorTouro"
                :placeholder="identificadorTouroPlaceholder" title="Identificador do Touro"
                :class="{ 'is-invalid': !isIdentificadorTouroValido }" autocomplete="off">
            </div>
            <div ref="dropdownFemea" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsFemea('up')"
            @keydown.down.prevent="navigateOptionsFemea('down')" @keydown.enter.prevent="selectHighlightedFemea">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownFemea">
                <span class="input-group-text" title="Fêmea"><i class="fas fa-box"></i></span>
                <input v-model="brinco" :class="{ 'is-invalid': !isFemeaValida }" @input="inputFemea"
                  @click="filterFemeas" @keydown.up.prevent="navigateOptionsFemea('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsFemea('down')" type="text" class="form-control"
                  :placeholder="femeaPlaceholder" id="caixa-select" title="Fêmea">
              </div>
              <div class="itens" v-show="dropdownFemeaOpen">
                <ul class="options">
                  <li v-for="(femea, index) in femeasFiltradas" :key="femea.id" :value="femea.id"
                    @click="selectFemea(femea)" :class="{ 'highlighted': index === highlightedIndexFemea }">{{
                    femea.brinco }}</li>
                </ul>
              </div>
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Observação"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacao" type="text" class="form-control" autocomplete="off"
                id="observacao" placeholder="Observação" title="Observação">
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
import LoadSpinner from './LoadSpiner.vue';

export default {
  mixins: [masksMixin],

  components: {
    LoadSpinner,
  },

  data() {
    return {
      activeTab: 'cadastro',
      femeas: [],
      femeasFiltradas: [],
      brinco: '',
      veterinarios: [],
      veterinariosFiltrados: [],
      nomeVeterinario: '',
      highlightedIndexVeterinario: -1,
      dropdownVeterinarioOpen: false,
      highlightedIndexFemea: -1,
      dropdownFemeaOpen: false,
      loadingSubmit: false,
      loadingInicialFemeas: true,
      loadingInicialVeterinarios: true,
      formData: {
        id: null,
        dataInseminacao: null,
        veterinario: null,
        animal: null,
        identificadorTouro: null,
        observacao: null,
      },
      isFemeaValida: true,
      isDataValida: true,
      isVeterinarioValido: true,
      isIdentificadorTouroValido: true,
      femeaPlaceholder: 'Fêmea*',
      dataPlaceholder: 'Data*',
      veterinarioPlaceholder: 'Veterinário*',
      identificadorTouroPlaceholder: 'Identificador do Touro*',
    };
  },

  mounted() {
    this.buscarFemeasVivasDaApi();
    this.buscarVeterinariosDaApi();
    document.addEventListener('click', this.handleClickOutsideVeterinario);
    document.addEventListener('click', this.handleClickOutsideFemea);
  },

  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(value) {
      this.brinco = this.brincoFiltroMask(value);
    },


    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarFemeasVivasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/femeas/vivas', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.femeas = response.data;
        this.loadingInicialFemeas = false;
      } catch (error) {
        console.error('Erro ao buscar inseminações da API:', error);
      }
    },

    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/');
        this.veterinarios = response.data;
        this.loadingInicialVeterinarios = false;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },

    async submitForm() {
      // Submete o formulário
      if (this.verificaVazio()) {
        this.loadingSubmit = true;
        try {
          const response = await api.post('http://127.0.0.1:8000/inseminacoes/', this.formData);
          if (response.status === 201) {
            this.loadingSubmit = false;

            setTimeout(() => {
              alert('Cadastro realizado com sucesso!');
              this.$router.push('/inseminacoes');
              
            }, 100);
          } else {
            this.loadingSubmit = false;
            alert('Erro ao cadastrar inseminação. Tente novamente mais tarde.');
          }
        } catch (error) {
          this.loadingSubmit = false;
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECT VETERINARIO----------------------------------------------------------------------------------------------------------------------------------------------------
    filterVeterinarios() {
      this.veterinariosFiltrados = this.veterinarios.filter(veterinario => veterinario.nome.toLowerCase().includes(this.nomeVeterinario.toLowerCase()));
    },

    selectVeterinario(veterinario) {
      this.nomeVeterinario = veterinario.nome;
      this.formData.veterinario = veterinario.id;
      this.veterinariosFiltrados = [];
      this.dropdownVeterinarioOpen = false;
    },

    toggleDropdownVeterinario() {
      this.dropdownVeterinarioOpen = !this.dropdownVeterinarioOpen;
      let nomeCorreto = false;
      let brincoCorreto = false;

      if(!this.dropdownVeterinarioOpen){
        this.veterinariosFiltrados.forEach(veterinario => {
          if(veterinario.nome.toLowerCase() === this.nomeVeterinario.toLowerCase()){
            this.nomeVeterinario = veterinario.nome;
            this.formData.veterinario = veterinario.id;
            this.veterinariosFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomeVeterinario = '';
        }
      }

      else if(this.dropdownFemeaOpen){
        this.femeas.forEach(femea => {
          if(femea.brinco === this.brinco){
            this.formData.animal = femea.id;
            this.femeasFiltradas = [];
            brincoCorreto = true;
            
          }
        });
        if(!brincoCorreto){
          this.formData.animal = null;
          this.brinco = ''
        }
        this.dropdownFemeaOpen = false;
        this.filterVeterinarios();
      }

      else{
        this.filterVeterinarios();
      }
    },

    handleClickOutsideVeterinario(event) {
      if (this.dropdownVeterinarioOpen && this.$refs.dropdownVeterinario && !this.$refs.dropdownVeterinario.contains(event.target)) {
        let nomeCorreto = false;
        this.veterinarios.forEach(veterinario => {
          if(veterinario.nome.toLowerCase() === this.nomeVeterinario.toLowerCase()){
            this.nomeVeterinario = veterinario.nome;
            this.formData.veterinario = veterinario.id;
            this.veterinariosFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.veterinario = null;
          this.nomeVeterinario = '';
        }
        this.dropdownVeterinarioOpen = false;
      }
    },

    inputVeterinario(){
      this.filterVeterinarios();
      this.dropdownVeterinarioOpen = true;
    },

    navigateOptionsVeterinario(direction) {
      if (direction === 'up' && this.highlightedIndexVeterinario > 0) {
        this.highlightedIndexVeterinario--;
      } else if (direction === 'down' && this.highlightedIndexVeterinario < this.veterinariosFiltrados.length - 1) {
        this.highlightedIndexVeterinario++;
      }
    },

    selectHighlightedVeterinario() {
      if (this.highlightedIndexVeterinario >= 0 && this.highlightedIndexVeterinario < this.veterinariosFiltrados.length) {
        this.selectVeterinario(this.veterinariosFiltrados[this.highlightedIndexVeterinario]);
      }
    },


//LÓGICA DOS SELECT FEMEA----------------------------------------------------------------------------------------------------------------------------------------------------
    filterFemeas() {
      this.femeasFiltradas = this.femeas.filter(femea => femea.brinco.includes(this.brinco));
    },

    selectFemea(femea) {
      this.brinco = femea.brinco;
      this.formData.animal = femea.id;
      this.femeasFiltradas = [];
      this.dropdownFemeaOpen = false;
      this.highlightedIndexFemea = -1; // Reseta o índice após a seleção
    },

    toggleDropdownFemea() {
      this.dropdownFemeaOpen = !this.dropdownFemeaOpen;
      let brincoCorreto = false;
      let nomeCorreto = false;

      if(!this.dropdownFemeaOpen){
        this.femeasFiltradas.forEach(femea => {
          if(femea.brinco === this.brinco){
            this.brinco = femea.brinco;
            this.formData.animal = femea.id;
            this.femeasFiltradas = [];
            brincoCorreto = true;
          }
        });
        if(!brincoCorreto){
          this.brinco = '';
        }
      }
      else if(this.dropdownVeterinarioOpen){
        this.veterinarios.forEach(veterinario => {
          if(veterinario.nome.toLowerCase() === this.nomeVeterinario.toLowerCase()){
            this.formData.veterinario = veterinario.id;
            this.veterinariosFiltrados = [];
            nomeCorreto = true;
            
          }
        });
        if(!nomeCorreto){
          this.formData.veterinario = null;
          this.nomeVeterinario = ''
        }
        this.dropdownVeterinarioOpen = false;
        this.filterFemeas();
      }

      else{
        this.filterFemeas();
      }
    },

    handleClickOutsideFemea(event) {
      let brincoCorreto = false;
      if (this.dropdownFemeaOpen && this.$refs.dropdownFemea && !this.$refs.dropdownFemea.contains(event.target)) {
        this.femeas.forEach(femea => {
          if(femea.brinco === this.brinco){
            this.selectFemea(femea);
            brincoCorreto = true;
          }
        });
        if(!brincoCorreto){
          this.brinco = '';
          this.formData.animal = null;
        }
      }
      this.dropdownFemeaOpen = false;
    },

    inputFemea(event) {
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterFemeas();
      this.dropdownFemeaOpen = true;
      this.highlightedIndexFemea = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsFemea(direction) {
    if (direction === 'up' && this.highlightedIndexFemea > 0) {
      this.highlightedIndexFemea--;
    } else if (direction === 'down' && this.highlightedIndexFemea < this.femeasFiltradas.length - 1) {
      this.highlightedIndexFemea++;
    }
  },

  selectHighlightedFemea() {
    if (this.highlightedIndexFemea >= 0 && this.highlightedIndexFemea < this.femeasFiltradas.length) {
      this.selectFemea(this.femeasFiltradas[this.highlightedIndexFemea]);
    }
  },


    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio() {
      //DATA DA INSEMINAÇÃO
      if (this.formData.dataInseminacao != null) {
        if (this.formData.dataInseminacao.trim() != '') {
          this.isDataValida = true;
          this.dataPlaceholder = 'Digite a Data da Inseminação';
        }
        else {
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Inseminação é um Campo Obrigatório';
        }
      }
      else {
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Inseminação é um Campo Obrigatório';
      }

      //BRINCO
      if (this.brinco != null) {
        if (this.brinco.trim() != '') {
          this.isFemeaValida = true;
          this.femeaPlaceholder = 'Fêmea';
        }
        else {
          this.isFemeaValida = false;
          this.femeaPlaceholder = 'Fêmea é um Campo Obrigatório';
        }
      }
      else {
        this.isFemeaValida = false;
        this.femeaPlaceholder = 'Fêmea é um Campo Obrigatório';
      }

      //VETERINÁRIO
      if (this.nomeVeterinario != null) {
        if (this.nomeVeterinario.trim() != '') {
          this.isVeterinarioValido = true;
          this.veterinarioPlaceholder = 'Veterinário';
        }
        else {
          this.isVeterinarioValido = false;
          this.veterinarioPlaceholder = 'Veterinário é um Campo Obrigatório'
        }
      }
      else {
        this.isVeterinarioValido = false;
        this.veterinarioPlaceholder = 'Veterinário é um Campo Obrigatório'
      }

      //IDENTIFICADOR TOURO
      if (this.formData.identificadorTouro != null) {
        if (this.formData.identificadorTouro.trim() != '') {
          this.isIdentificadorTouroValido = true;
          this.identificadorTouroPlaceholder = 'Identificador do Touro';
        }
        else {
          this.isIdentificadorTouroValido = false;
          this.identificadorTouroPlaceholder = 'Identificador Touro é um Campo Obrigatório';
        }
      }
      else {
        this.isIdentificadorTouroValido = false;
        this.identificadorTouroPlaceholder = 'Identificador Touro é um Campo Obrigatório';
      }

      //OBSERVAÇÃO
      if (this.formData.observacao != null && this.formData.observacao.trim() == '') {
        this.formData.observacao = null;
      }

      return (
        this.isDataValida &&
        this.isFemeaValida &&
        this.isVeterinarioValido &&
        this.isIdentificadorTouroValido
      );
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },
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

#legenda {
  font-size: 16px;
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

.select{
  margin-bottom: 0px !important;
}

.highlighted {
  background-color: #f0f0f0;
}
</style>

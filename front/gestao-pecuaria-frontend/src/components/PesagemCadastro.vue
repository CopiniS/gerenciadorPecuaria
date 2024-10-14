<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicial" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'pesagens' }" id="nav-vet-tab"
          @click="selectTab('pesagens')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Pesagem</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Pesagem</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'pesagens' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Pesagem</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <DateComponent type="text" :placeholder="dataPlaceholder" class="form-control" id="dataPesagemCadastro"
                v-model="formData.dataPesagem" :class="{ 'is-invalid': !isDataValida }" title="Data" autocomplete="off"
                @update:selectedDate="updateDataPesagem" />
            </div>
            <hr>
            <div ref="dropdown" class="select mb-3 input-group" @keydown.up.prevent="navigateOptions('up')"
              @keydown.down.prevent="navigateOptions('down')" @keydown.enter.prevent="selectHighlightedAnimal">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdown">
                <span class="input-group-text" title="Animal"><i class="fas fa-user-tag"></i></span>
                <input v-model="brinco" :class="{ 'is-invalid': !isAnimalValido }" @input="inputBrinco"
                  @keydown.up.prevent="navigateOptions('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptions('down')" type="text" class="form-control"
                  :placeholder="animalPlaceholder" id="caixa-select" title="Animal">
              </div>
              <div class="itens" v-show="dropdownOpen">
                <ul class="options">
                  <li v-for="(animal, index) in animaisFiltrados" :key="animal.id" :value="animal.id"
                    @click="selectAnimal(animal)" :class="{ 'highlighted': index === highlightedIndex }">{{
                      animal.brinco }}</li>
                </ul>
              </div>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Peso"><i class="fas fa-weight"></i></span>
              <input v-model="formData.peso" type="text" @input="aplicarPesoMask" class="form-control"
                autocomplete="off" id="peso" :placeholder="pesoPlaceholder" :class="{ 'is-invalid': !isPesoValido }"
                title="Peso">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Observação"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacao" type="text" autocomplete="off" class="form-control" id="observacao"
                placeholder="Observação" title="Observação">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('pesagens')">Cancelar</button>
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
import DateComponent from './DateComponent.vue';

export default {
  mixins: [masksMixin],

  components: {
    LoadSpinner,
    DateComponent
  },

  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      highlightedIndex: -1,
      dropdownOpen: false,
      loadingSubmit: false,
      loadingInicial: true,
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
      animalPlaceholder: 'Animal*',
      dataPlaceholder: 'Data*',
      pesoPlaceholder: 'Peso*',
    };
  },

  mounted() {
    this.buscarAnimaisDaApi();
    document.addEventListener('click', this.handleClickOutside);
  },

  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarPesoMask(event) {
      const value = event.target.value;
      this.formData.peso = this.valorMask(value);
    },

    aplicarBrincoMask(value) {
      this.brinco = this.brincoFiltroMask(value);
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
        this.loadingInicial = false;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        this.loadingSubmit = true;
        try {
          //FORMATA PESO
          this.formData.peso = this.replaceVirgulaPonto(this.formData.peso);

          const response = await api.post('http://127.0.0.1:8000/pesagens/', this.formData, {
          });

          if (response.status === 201) {
            this.loadingSubmit = false;
            setTimeout(() => {
              alert('Cadastro realizado com sucesso!');
              this.$router.push('/pesagens');
            }, 100);
          } else {
            this.loadingSubmit = false;
            alert('Erro ao cadastrar pesagem. Tente novamente mais tarde.');
          }
        } catch (error) {
          this.loadingSubmit = false;
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


    //LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.includes(this.brinco));
    },

    selectAnimal(animal) {
      this.brinco = animal.brinco;
      this.formData.animal = animal.id;
      this.animaisFiltrados = [];
      this.dropdownOpen = false;
    },

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
      let nomeCorreto = false;

      if (!this.dropdownOpen) {
        this.animaisFiltrados.forEach(animal => {
          if (animal.brinco === this.brinco) {
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.brinco = '';
        }
      }
      else {
        this.filterAnimais();
      }
    },

    handleClickOutside(event) {
      if (this.dropdownOpen && this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.dropdownOpen = false;
      }
      let nomeCorreto = false;
      if (!this.dropdownOpen) {
        this.animais.forEach(animal => {
          if (animal.brinco === this.brinco) {
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.brinco = '';
        }
      }
    },

    inputBrinco(event) {
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
      this.dropdownOpen = true;
    },

    navigateOptions(direction) {
      if (direction === 'up' && this.highlightedIndex > 0) {
        this.highlightedIndex--;
      } else if (direction === 'down' && this.highlightedIndex < this.animaisFiltrados.length - 1) {
        this.highlightedIndex++;
      }
    },

    selectHighlightedAnimal() {
      if (this.highlightedIndex >= 0 && this.highlightedIndex < this.animaisFiltrados.length) {
        this.selectAnimal(this.animaisFiltrados[this.highlightedIndex]);
      }
    },


    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio() {
      //DATA DA PESAGEM
      if (this.formData.dataPesagem != null) {
        if (this.formData.dataPesagem.trim() != '') {
          this.isDataValida = true;
          this.dataPlaceholder = 'Data*';
        }
        else {
          this.isDataValida = false;
          this.dataPlaceholder = 'Data é um Campo Obrigatório';
        }
      }
      else {
        this.isDataValida = false;
        this.dataPlaceholder = 'Data é um Campo Obrigatório';
      }

      //BRINCO
      if (this.brinco != null) {
        if (this.brinco.trim() != '') {
          this.isAnimalValido = true;
          this.animalPlaceholder = 'Animal*';
        }
        else {
          this.isAnimalValido = false;
          this.animalPlaceholder = 'Animal é um Campo Obrigatório';
        }
      }
      else {
        this.isAnimalValido = false;
        this.animalPlaceholder = 'Animal é um Campo Obrigatório';
      }

      //PESO DO ANIMAL
      if (this.formData.peso != null) {
        if (this.formData.peso.trim() != '') {
          this.isPesoValido = true;
          this.pesoPlaceholder = 'Peso*';
        }
        else {
          this.isPesoValido = false;
          this.pesoPlaceholder = 'Peso é um Campo Obrigatório';
        }
      }

      //OBSERVAÇÕES
      if (this.formData.observacao != null && this.formData.observacao.trim() == '') {
        this.formData.observacao = null;
      }

      return (
        this.isDataValida &&
        this.isAnimalValido &&
        this.isPesoValido
      );
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    updateDataPesagem(data) {
      this.formData.dataPesagem = data;
    },
    checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'pesagens') {
        this.$router.push('/pesagens');
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

.select {
  margin-bottom: 0px !important;
}

.highlighted {
  background-color: #f0f0f0;
}
</style>

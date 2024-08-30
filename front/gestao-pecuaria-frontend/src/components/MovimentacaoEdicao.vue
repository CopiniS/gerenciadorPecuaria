<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'movimentacoes' }" id="nav-vet-tab"
          @click="selectTab('movimentacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Movimentação</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Movimentação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'movimentacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Movimentação</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group" >
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :placeholder="dataPlaceholder" class="form-control" id="dataMovimentacaoEdicao"
                v-model="formData.dataMovimentacao" :class="{ 'is-invalid': !isDataValida }" title="Data">
            </div>
            <div ref="dropdownAnimal" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsAnimal('up')"
              @keydown.down.prevent="navigateOptionsAnimal('down')" @keydown.enter.prevent="selectHighlightedAnimal">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownAnimal">
                <span class="input-group-text" title="Animal"><i class="fas fa-box"></i></span>
                <input v-model="brinco" :class="{ 'is-invalid': !isAnimalValido }" @input="inputAnimal"
                  @click="filterAnimais" @keydown.up.prevent="navigateOptionsAnimal('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsAnimal('down')" type="text" class="form-control"
                  :placeholder="animalPlaceholder" id="caixa-select" title="Animal">
              </div>
              <div class="itens" v-show="dropdownAnimalOpen">
                <ul class="options">
                  <li v-for="(animal, index) in animaisFiltrados" :key="animal.id" :value="animal.id"
                    @click="selectAnimal(animal)" :class="{ 'highlighted': index === highlightedIndexAnimal }">{{
                    animal.brinco }}</li>
                </ul>
              </div>
            </div>
            <div class="mb-3 input-group" >
              <span class="input-group-text" title="Piquete de Origem"><i class="fas fa-hashtag"></i></span>
              <input v-model="nomePiqueteOrigem" title="Piquete de Origem" type="text" autocomplete="off"
              class="form-control" :placeholder="piqueteOrigemPlaceholder" :disabled="true">
            </div>

            <div ref="dropdownPiqueteDestino" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsPiqueteDestino('up')"
            @keydown.down.prevent="navigateOptionsPiqueteDestino('down')" @keydown.enter.prevent="selectHighlightedPiqueteDestino">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownPiqueteDestino">
                <span class="input-group-text" title="Piquete de Destino"><i class="fas fa-box"></i></span>
                <input v-model="nomePiqueteDestino" :class="{ 'is-invalid': !isPiqueteDestinoValido }" @input="inputPiqueteDestino"
                  @click="filterPiquetesDestino" @keydown.up.prevent="navigateOptionsPiqueteDestino('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsPiqueteDestino('down')" type="text" class="form-control"
                  :placeholder="piqueteDestinoPlaceholder" id="caixa-select" title="Piquete de Destino">
              </div>
              <div class="itens" v-show="dropdownPiqueteDestinoOpen">
                <ul class="options">
                  <li v-for="(piqueteDestino, index) in piquetesDestinoFiltrados" :key="piqueteDestino.id" :value="piqueteDestino.id"
                    @click="selectPiqueteDestino(piqueteDestino)" :class="{ 'highlighted': index === highlightedIndexPiqueteDestino }">{{
                    piqueteDestino.nome}} - {{ piqueteDestino.propriedade.nome}}</li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group">
                    <span class="input-group-text" title="Motivo"><i class="fas fa-comment"></i></span>
                    <input v-model="formData.motivo" type="text" class="form-control" id="motivo" 
                    placeholder="Motivo" title="Motivo" autocomplete="off">
                </div>

            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('movimentacoes')">Cancelar</button>
              <button type="submit" class="btn btn-success">Salvar</button>
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
      activeTab: 'edicao', // Começa na aba de edição
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      piquetesDestino: [],
      piquetesDestinoFiltrados: [],
      nomePiqueteOrigem: '',
      nomePiqueteDestino: '',
      highlightedIndexPiqueteDestino: -1,
      dropdownPiqueteDestinoOpen: false,
      highlightedIndexAnimal: -1,
      dropdownAnimalOpen: false,
      formData: {
          id: null,
          animal: null,
          dataMovimentacao: null,
          piqueteOrigem: null,
          piqueteDestino: null,
          motivo: null,
      },
      isAnimalValido: true,
      isDataValida: true,
      isPiqueteDestinoValido: true,
      animalPlaceholder: 'Animal*',
      dataPlaceholder: 'Data*',
      piqueteOrigemPlaceholder: 'Piquete de Origem*',
      piqueteDestinoPlaceholder: 'Piquete de Destino*'
        };
    },
 
    mounted() {
        const movimentacaoId = this.$route.params.movimentacaoId;
        if (movimentacaoId) {
            this.fetchMovimentacao(movimentacaoId);
        }
        this.buscarAnimaisDaApi();
        this.buscarPiquetesDaApi();
        document.addEventListener('click', this.handleClickOutsidePiqueteDestino);
        document.addEventListener('click', this.handleClickOutsideAnimal);
    },
    methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarBrincoMask(value){
        this.brinco =  this.brincoFiltroMask(value);
      },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
      async fetchMovimentacao(id) {
        try {
          const response = await api.get(`http://127.0.0.1:8000/movimentacoes/movimentacao/${id}`);
          const movimentacao = response.data;
          this.formData.id = movimentacao[0].id;
          this.formData.animal = movimentacao[0].animal.id;
          this.formData.dataMovimentacao = movimentacao[0].dataMovimentacao;
          this.formData.piqueteOrigem = movimentacao[0].piqueteOrigem.id;
          this.formData.piqueteDestino = movimentacao[0].piqueteDestino.id;
          this.formData.motivo = movimentacao[0].motivo;

          this.brinco = movimentacao[0].animal.brinco;
          this.nomePiqueteOrigem = movimentacao[0].piqueteOrigem.nome
          this.nomePiqueteDestino = movimentacao[0].piqueteDestino.nome
          
        } catch (error) {
          console.error('Erro ao carregar dados da movimentacao:', error);
        }
      },

      async buscarAnimaisDaApi() {
          try {
              const response = await api.get('http://127.0.0.1:8000/animais/vivos-piquetes' , {
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
          const response = await api.get('http://127.0.0.1:8000/piquetes/piquetes-propriedades');
          this.piquetesDestino = response.data;
        } catch (error) {
          console.error('Erro ao buscar piquetes da API:', error);
        }
      },

      async submitForm() {
        if (this.verificaVazio()) {
          if(this.verificaDuploPiquete()){
            try {
                const response = await api.patch(`http://127.0.0.1:8000/movimentacoes/${this.formData.id}/`, this.formData , {
              });

              if (response.status === 200) {
                alert('Alterações salvas com sucesso!');
                this.selectTab('movimentacoes');
              } else {
                alert('Erro ao salvar alterações. Tente novamente mais tarde.');
              }
            } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
          }
          else{
            alert('Não é possível movimentar o Animal dentro do mesmo Piquete');
          }
        }
      },


//LÓGICA DOS SELECT ANIMAL----------------------------------------------------------------------------------------------------------------------------------------------------
    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.includes(this.brinco));
    },

    selectAnimal(animal) {
        this.brinco = animal.brinco;
        this.formData.animal = animal.id;
        this.formData.piqueteOrigem = animal.piquete.id;
        this.nomePiqueteOrigem = animal.piquete.nome;
        this.animaisFiltrados = [];
        this.dropdownAnimalOpen = false;
    },

    toggleDropdownAnimal() {
      this.dropdownAnimalOpen = !this.dropdownAnimalOpen;
      let nomeCorreto = false;
      let brincoCorreto = false;

      if(!this.dropdownAnimalOpen){
        this.animaisFiltrados.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.selectAnimal(animal);
            brincoCorreto = true;
          }
        });
        if(!brincoCorreto){
          this.brinco = '';
          this.formData.animal = null;
          this.formData.piqueteOrigem = null;
          this.nomePiqueteOrigem = '';
        }
      }
      else if(this.dropdownPiqueteDestinoOpen){
        this.piquetesDestino.forEach(piqueteDestino => {
          if(piqueteDestino.nome.toLowerCase() === this.nomePiqueteDestino.toLowerCase()){
            this.selectPiqueteDestino(piqueteDestino);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.piqueteDestino = null;
          this.nomePiqueteDestino = '';
        }
        this.dropdownPiqueteDestinoOpen = false;
        this.filterAnimais();
      }

      else{
        this.filterAnimais();
      }
    },

    handleClickOutsideAnimal(event) {
      if (this.dropdownAnimalOpen && this.$refs.dropdownAnimal && !this.$refs.dropdownAnimal.contains(event.target)) {
        this.dropdownAnimalOpen = false;
      }
      let nomeCorreto = false;
      if(!this.dropdownAnimalOpen){
        this.animais.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.selectAnimal(animal);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.brinco = '';
          this.formData.animal = null;
          this.formData.piqueteOrigem = null;
          this.nomePiqueteOrigem = '';
        }
      }
    },

    inputAnimal(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
      this.dropdownAnimalOpen = true;
    },

    navigateOptionsAnimal(direction) {
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


//LÓGICA DOS SELECT PIQUETE DESTINO----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetesDestino() {
      this.piquetesDestinoFiltrados = this.piquetesDestino.filter(piqueteDestino => piqueteDestino.nome.toLowerCase().includes(this.nomePiqueteDestino.toLowerCase()));
    },

    async selectPiqueteDestino(piqueteDestino) {
      this.nomePiqueteDestino = piqueteDestino.nome + " - " + piqueteDestino.propriedade.nome;
      this.formData.piqueteDestino = piqueteDestino.id;
      this.piquetesDestinoFiltrados = [];
      this.dropdownPiqueteDestinoOpen = false;
      this.highlightedIndexPiqueteDestino = -1; // Reseta o índice após a seleção
    },

    toggleDropdownPiqueteDestino() {
      this.dropdownPiqueteDestinoOpen = !this.dropdownPiqueteDestinoOpen;
      let nomeCorreto = false;
      let brincoCorreto = false;

      if(!this.dropdownPiqueteDestinoOpen){
        this.piquetesDestinoFiltrados.forEach(piqueteDestino => {
          if(piqueteDestino.nome.toLowerCase() === this.nomePiqueteDestino.toLowerCase()){
            this.selectPiqueteDestino(piqueteDestino);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomePiqueteDestino = '';
          this.formData.piqueteDestino = null;
        }
      }
      else if(this.dropdownAnimalOpen){
        this.animais.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.selectAnimal(animal);
            brincoCorreto = true;
            
          }
        });
        if(!brincoCorreto){
          this.brinco = '';
          this.formData.animal = null;
          this.formData.piqueteOrigem = null;
          this.nomePiqueteOrigem = '';
        }
        this.dropdownAnimalOpen = false;
        this.filterPiquetesDestino();
      }

      else{
        this.filterPiquetesDestino();
      }
    },

    handleClickOutsidePiqueteDestino(event) {
      let nomeCorreto = false;
      if (this.dropdownPiqueteDestinoOpen && this.$refs.dropdownPiqueteDestino && !this.$refs.dropdownPiqueteDestino.contains(event.target)) {
        this.piquetesDestino.forEach(piqueteDestino => {
          if(piqueteDestino.nome.toLowerCase() === this.nomePiqueteDestino.toLowerCase()){
            this.selectPiqueteDestino(piqueteDestino);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.nomePiqueteDestino = '';
          this.formData.piqueteDestino = null;
        }
      }
      this.dropdownPiqueteDestinoOpen = false;
    },

    inputPiqueteDestino() {
      this.filterPiquetesDestino();
      this.dropdownPiqueteDestinoOpen = true;
      this.highlightedIndexPiqueteDestino = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsPiqueteDestino(direction) {
      if (direction === 'up' && this.highlightedIndexPiqueteDestino > 0) {
        this.highlightedIndexPiqueteDestino--;
      } else if (direction === 'down' && this.highlightedIndexPiqueteDestino < this.piquetesDestinoFiltrados.length - 1) {
        this.highlightedIndexPiqueteDestino++;
      }
    },

  selectHighlightedPiqueteDestino() {
    if (this.highlightedIndexPiqueteDestino >= 0 && this.highlightedIndexPiqueteDestino < this.piquetesDestinoFiltrados.length) {
      this.selectPiqueteDestino(this.piquetesDestinoFiltrados[this.highlightedIndexPiqueteDestino]);
    }
  },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
      verificaVazio(){
        //DATA DA MOVIMENTAÇÃO
        if(this.formData.dataMovimentacao != null){
          if(this.formData.dataMovimentacao.trim() != ''){
            this.isDataValida = true;
            this.dataPlaceholder = 'Data*';
          }
          else{
            this.isDataValida = false;
            this.dataPlaceholder = 'Data é um Campo Obrigatório';
          }
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data é um Campo Obrigatório';
        }
        
        //BRINCO  
          if(this.brinco != null){
            if(this.brinco.trim() != ''){
              this.isAnimalValido = true;
              this.animalPlaceholder = 'Animal*'
            }
            else{
            this.isAnimalValido = false;
            this.animalPlaceholder = 'Animal é um Campo Obrigatório';
            }
          }
          else{
            this.isAnimalValido = false;
            this.animalPlaceholder = 'Animal é um Campo Obrigatório';
          }

        //PIQUETE DE DESTINO
        if(this.nomePiqueteDestino != null){
            if(this.nomePiqueteDestino.trim() != ''){
              this.isPiqueteDestinoValido = true;
              this.piqueteDestinoPlaceholder = 'Piquete de Destino*';
            }
            else{
              this.isPiqueteDestinoValido = false;
              this.piqueteDestinoPlaceholder = 'Piquete de Destino é um Campo Obrigatório'
            }
        }
        else{
          this.isPiqueteDestinoValido = false;
          this.piqueteDestinoPlaceholder = 'Piquete de Destino é um Campo Obrigatório'
        }

        //MOTIVO
        if(this.formData.motivo != null && this.formData.motivo.trim() == ''){
          this.formData.motivo = null;
        }

        return (
          this.isDataValida &&
          this.isAnimalValido &&
          this.isPiqueteDestinoValido
        );
      },

      verificaDuploPiquete(){
        return (this.formData.piqueteOrigem != this.formData.piqueteDestino);
      },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },      
selectTab(tab) {
        this.activeTab = tab;
        if (tab === 'movimentacoes') {
          this.$router.push('/movimentacoes');
        }
      },

      cancelarEdicao() {
        this.$router.push('/movimentacoes');
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
</style>

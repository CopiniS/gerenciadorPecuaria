<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
        @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais"
        aria-selected="true">Lista de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-visualizacao-tab"
          @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-visualizacao" 
          aria-selected="true">Visualização do Animal</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Ocorrência</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'ocorrencias' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Ocorrência</h1>
          <h2 class="title fs-5" id="cadastroLabel">Animal: {{ brinco }}</h2>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group" >
              <span class="input-group-text" title="Data da Ocorrência"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :placeholder="dataPlaceholder" class="form-control" id="dataOcorrencia"
                v-model="formData.dataOcorrencia" :class="{ 'is-invalid': !isDataValida }" title="Data da Ocorrência">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Tipo da Ocorrência"><i class="fas fa-venus-mars"></i></span>
              <select v-model="formData.tipo" :class="{ 'is-invalid': !isTipoValido }" class="form-select" id="tipo"
                aria-label="Tipo" :placeholder="tipoPlaceholder" title="Tipo da Ocorrência">
                <option disabled :value="null">{{ tipoPlaceholder }}</option>
                <option value="morte">Morte</option>
                <option value="doenca">Doença</option>
                <option value="desaparecido">Desaparecido</option>
                <option value="outro">Outro</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Descrição da Ocorrência"><i class="fas fa-tags"></i></span>
              <input v-model="formData.descricao" type="text" class="form-control" id="descricao"
                placeholder="Descrição" title="Descrição da Ocorrência">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('visualizacao')">Cancelar</button>
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
      brinco: null,
      formData: {
        id: null,
        dataOcorrencia: null,
        animal: null,
        tipo: null,
        descricao: null,
      },
      isDataValida: true,
      isTipoValido: true,
      dataPlaceholder: 'Data da Ocorrência*',
      tipoPlaceholder: 'Tipo da Ocorrencia*',
    };
  },

  mounted(){
    const animalId = this.$route.params.animalId;
    if (animalId) {
      this.fetchAnimal(animalId);
    }
  },

  methods: {
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
   async fetchAnimal(animalId) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/animais/animal/${animalId}/`);
        const animal = response.data;
        this.formData.animal = animal[0].id;
        this.brinco = animal[0].brinco;
        
      } catch (error) {
        console.error('Erro ao buscar animal da API:', error);
      }
    },
   
   async submitForm() {
      if (this.verificaVazio()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/ocorrencias/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.selectTab('visualizacao');
          } else {
            alert('Erro ao cadastrar ocorrencia. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DA OCORRENCIA
      if(this.formData.dataOcorrencia != null){
        if(this.formData.dataOcorrencia.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Data da Ocorrência';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Ocorrência é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Ocorrência é um Campo Obrigatório';
      }

      //TIPO
      if(this.formData.tipo != null){
        if(this.formData.tipo.trim() != ''){
          this.isTipoValido = true;
          this.tipoPlaceholder = 'Tipo da Ocorrência';
        }
        else{
          this.isTipoValido = false;
          this.tipoPlaceholder = 'Tipo da Ocorrência é um Campo Obrigatório';
        }
      }
      else{
        this.isTipoValido = false;
        this.tipoPlaceholder = 'Tipo da Ocorrência é um Campo Obrigatório';
      }

      //DESCRIÇÃO
      if(this.formData.descricao != null && this.formData.descricao.trim() == ''){
        this.formData.descricao = null;
      }

      return (
        this.isDataValida &&
        this.isTipoValido
      );
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
      else if(tab==='visualizacao'){
        this.$router.push({
            name: 'VizualizarAnimal', 
            params: { animalId: this.formData.animal } 
        })
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
</style>

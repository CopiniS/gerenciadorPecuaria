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
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab" @click="selectTab('edicao')" 
        type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição de Ocorrência</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel" aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Ocorrência</h1>
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
              <input v-model="formData.descricao" @input="aplicarDescricaoMask" type="text" class="form-control" id="descricao"
                placeholder="Descrição" title="Descrição da Ocorrência">
              <div>({{ contadorDescricao }} / 255)</div>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('visualizacao')">Cancelar</button>
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
        activeTab: 'edicao',
        contadorDescricao: 0,
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

  mounted() {
    const ocorrenciaId = this.$route.params.ocorrenciaId;
    if (ocorrenciaId) {
      this.fetchOcorrencia(ocorrenciaId);
    }

  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarDescricaoMask(event){
      const value = event.target.value;
      this.formData.descricao = this.observacoesMask(value);
      this.contadorDescricao = this.formData.descricao.length;
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchOcorrencia(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/ocorrencias/ocorrencia/${id}`);
        const ocorrencia = response.data;
        this.formData.id = ocorrencia[0].id;
        this.formData.animal = ocorrencia[0].animal.id;
        this.formData.dataOcorrencia = ocorrencia[0].dataOcorrencia;
        this.formData.tipo = ocorrencia[0].tipo;
        this.formData.descricao = ocorrencia[0].descricao;

        this.brinco = ocorrencia[0].animal.brinco;
      } catch (error) {
        console.error('Erro ao carregar dados da ocorrencia:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/ocorrencias/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.selectTab('visualizacao');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
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
        console.log('animal: ', this.formData.animal);
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

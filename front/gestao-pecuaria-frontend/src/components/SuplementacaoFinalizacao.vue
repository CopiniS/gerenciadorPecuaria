
<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'suplementacoes' }" id="nav-vet-tab"
          @click="selectTab('suplementacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Suplementações</button>
        <button class="nav-link" :class="{ active: activeTab === 'finalizacao' }" id="nav-finalizacao-tab"
          @click="selectTab('finalizacao')" type="button" role="tab" aria-controls="nav-finalizacao"
          aria-selected="false">Finalização de Suplementação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'suplementacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'finalizacao' }" id="nav-finalizacao" role="tabpanel"
        aria-labelledby="nav-finalizacao-tab">
        <div class="table-container" id="finalizacao" tabindex="-1" aria-labelledby="finalizacaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="finalizacaoLabel">Finalização de Suplementação</h1>
          <form @submit.prevent="finalizarSuplementoSubmit">
              <div class="mb-3 input-group">
                <label for="dataFinal" title="Data Final" class="input-group-text"><i class="fas fa-calendar-alt"></i></label>
                <input type="text" title="Data Final" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataFinalPlaceholder" 
                class="form-control" id="dataFinalFi" v-model="formData.dataFinal" :class="{'is-invalid': !isDataFinalValida}">
              </div>
              <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('suplementacoes')">Cancelar</button>
                    <button type="button" class="btn btn-success" @click="submitForm">Finalizar</button>
              </div>
            </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';
import LoadSpinner from './LoadSpiner.vue';

export default {

  components: {
    LoadSpinner,
  },

  data() {
      return {
          activeTab: 'finalizacao', // Começa na aba de edição
          loadingSubmit: false,
          formData: {
              id: null,
              dataFinal: null,
          },
          isDataFinalValida: true,
          dataFinalPlaceholder: 'Data Final*',
      };
  },

  mounted() {
      const suplementacaoId = this.$route.params.suplementacaoId;
      if (suplementacaoId) {
          this.formData.id = suplementacaoId;
      }
  },
  methods: {
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async submitForm() {
      if (this.verificaVazio()) {
        this.loadingSubmit = true;
       try {
          const response = await api.patch(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            this.loadingSubmit = false;

            setTimeout(() => {
              
              alert('Finalização salvas com sucesso!');
              this.$router.push('/suplementacoes');
            }, 100);
          } else {
            this.loadingSubmit = false;
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          this.loadingSubmit = false;
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA FINAL
      if(this.formData.dataFinal != null){
        if(this.formData.dataFinal.trim() != ''){
          this.isDataFinalValida = true;
          this.dataFinalPlaceholder = 'Data Final*'
        }
        else{
          this.isDataFinalValida = false;
          this.dataFinalPlaceholder = 'Data Final é um Campo Obrigatório';
        }
      }
      else{
        this.isDataFinalValida = false;
        this.dataFinalPlaceholder = 'Data Final é um Campo Obrigatório';
      }

      return this.isDataFinalValida;
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'suplementacoes') {
        this.$router.push('/suplementacoes');
      }
    },

    cancelarEdicao() {
      this.$router.push('/suplementacoes');
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

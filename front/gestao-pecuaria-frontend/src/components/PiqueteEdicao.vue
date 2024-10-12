
<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicialPiqueteId || loadingInicialPiquetesDaApi" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'propriedades' }" id="nav-propriedades-tab" @click="selectTab('propriedades')" 
        type="button" role="tab" aria-controls="nav-propriedades" aria-selected="true">Lista de Propriedades</button>
        
        <button class="nav-link" :class="{ active: activeTab === 'piquetes' }" id="nav-vet-tab"
          @click="selectTab('piquetes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Piquetes</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Piquete</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'propriedades' }" id="nav-propriedades" role="tabpanel" aria-labelledby="nav-propriedades-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'piquetes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Piquete</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
              <div class="mb-3 input-group">
                <span class="input-group-text" title="Nome"><i class="fas fa-hashtag"></i></span>
                <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" class="form-control" 
                id="nome" :placeholder="nomePlaceholder" title="Nome" autocomplete="off">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text" title="Tipo do cultivo"><i class="fas fa-seedling"></i></span>
                <select v-model="formData.tipoCultivo" :class="{'is-invalid': !isTipoCultivoValido}" 
                class="form-select" id="tipoCultivo" aria-label="Tipo de Cultivo" title="Tipo do cultivo">
                  <option disabled value="">{{ tipoCultivoPlaceholder }}</option>
                  <option>Pastagem Natural</option>
                  <option>Lavoura</option>
                  <option>Confinamento</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text" title="Área"><i class="fas fa-ruler-combined"></i></span>
                <input v-model="formData.area" :class="{'is-invalid': !isAreaValida}" type="text" class="form-control" 
                @input="aplicarAreaMask" id="area" :placeholder="areaPlaceholder" title="Área" autocomplete="off">
              </div>
              <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('piquetes')">Cancelar</button>
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
import { masksMixin } from '../mixins/maks';
import LoadSpinner from './LoadSpiner.vue';


export default {
  mixins: [masksMixin],

  components: {
    LoadSpinner,
  },

  data() {
    return {
      activeTab: 'edicao',  // Aba inicial é 'edicao'
      piquetesDaApi: null,
      loadingSubmit: false,
      loadingInicialPiqueteId: true,
      loadingInicialPiquetesDaApi: true,
      formData: {
        id: null,
        nome: '',
        tipoCultivo: '',
        area: '',
        propriedade: localStorage.getItem('propriedadeSelecionada')
      },
      isNomeValido: true,
      isTipoCultivoValido: true,
      isAreaValida: true,
      nomePlaceholder: 'Nome*',
      tipoCultivoPlaceholder: 'Tipo do cultivo*',
      areaPlaceholder: 'Área*',
    };
  },
 
  mounted() {
    const piqueteId = this.$route.params.piqueteId;
    if (piqueteId) {
        this.fetchPiquete(piqueteId);
    }
    
    this.buscarPiquetesDaApi();
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarAreaMask(event){
      const value = event.target.value;
      this.formData.area = this.valorMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchPiquete(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/piquetes/${id}`);
        const piquete = response.data;
        this.formData.id = piquete.id;
        this.formData.nome = piquete.nome;
        this.formData.tipoCultivo = piquete.tipoCultivo;
        this.formData.area = this.replacePontoVirgula(piquete.area);

        this.loadingInicialPiqueteId = false;
      } catch (error) {
        console.error('Erro ao carregar dados da piquete:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        this.loadingSubmit = true;
       try {
          //FORMATA AREA
          this.formData.area = this.replaceVirgulaPonto(this.formData.area);

          const response = await api.patch(`http://127.0.0.1:8000/piquetes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            this.loadingSubmit = false;
            setTimeout(() => {
              alert('Alterações salvas com sucesso!');
              this.$router.push('/piquetes');
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

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/' , {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetesDaApi = response.data;
        this.loadingInicialPiquetesDaApi = false;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      let valido = true;
      this.isNomeValido = true;
      this.nomePlaceholder = 'Nome*';
      
      // Cria uma nova lista sem o item com o id atual
      let piquetesComExclusao = this.piquetesDaApi.filter(piquete => piquete.id !== this.formData.id);

      // Verifica se o nome do piquete já existe na lista
      for (let i = 0; i < piquetesComExclusao.length; i++) {
        if (piquetesComExclusao[i].nome === this.formData.nome) {
          this.isNomeValido = false;
          this.nomePlaceholder = '"' + this.formData.nome + '"' + ' já está cadastrado no sistema';
          this.formData.nome = null;
          valido = false;
          break;
        }
      }
      
      return valido;
    },
    
    verificaVazio(){
      //NOME DO PIQUETE
      if(this.formData.nome != null){
        if(this.formData.nome.trim() != ''){
          this.isNomeValido = true;
          this.nomePlaceholder = 'Nome*';
        }
        else{
          this.isNomeValido = false;
          this.nomePlaceholder = 'Nome é um Campo Obrigatório';
        }
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome é um Campo Obrigatório';
      }

      //TIPO DO CULTIVO
      if(this.formData.tipoCultivo != null){
        if(this.formData.tipoCultivo.trim() != ''){
          this.isTipoCultivoValido = true;
          this.tipoCultivoPlaceholder = 'Tipo do cultivo*';
        }
        else{
          this.isTipoCultivoValido = false;
          this.tipoCultivoPlaceholder = 'Tipo do cultivo é um Campo Obrigatório';
        }
      }
      else{
        this.isTipoCultivoValido = false;
        this.tipoCultivoPlaceholder = 'Tipo do cultivo é um Campo Obrigatório';
      }

      //ÁREA DO PIQUETE
      if(this.formData.area != null){
        if(this.formData.area.trim() != ''){
          this.isAreaValida = true;
          this.areaPlaceholder = 'Área*';
        }
        else{
          this.isAreaValida = false;
          this.areaPlaceholder = 'Área é um Campo Obrigatório';
        }
      }
      else{
        this.isAreaValida = false;
        this.areaPlaceholder = 'Área é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isTipoCultivoValido &&
        this.isAreaValida
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
      if (tab === 'piquetes') {
        this.$router.push('/piquetes');
      }
      if (tab === 'propriedades') {
        this.$router.push('/propriedades');
      }
    },

    cancelarEdicao() {
      this.$router.push('/piquetes');
    },

    replacePontoVirgula(valorString){
      valorString = valorString.replace(".", ",");

      return valorString;
    },

    replaceVirgulaPonto(valorString){
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
</style>


<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'propriedades' }" id="nav-vet-tab"
          @click="selectTab('propriedades')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Propriedades</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Propriedade</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'propriedades' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Propriedade</h1>
          <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                    <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" class="form-control" :placeholder="nomePlaceholder"
                        id="nome" >
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>
                    <input v-model="formData.endereco" :class="{'is-invalid': !isEnderecoValido}" type="text" class="form-control"
                        :placeholder="enderecoPlaceholder" id="endereco">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-flag"></i></span>
                    <select v-model="formData.estado" :class="{'is-invalid': !isEstadoValido}" class="form-select"
                        @change="buscarCidadesPorEstado($event.target.value)">
                        <option value="" disabled>{{ estadoPlaceholder }}</option>
                        <option v-for="estado in estados" :key="estado.id" :value="estado.nome">{{ estado.nome
                            }}</option>
                    </select>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-city"></i></span>
                    <select v-model="formData.cidade" :class="{'is-invalid': !isCidadeValida}" class="form-select" >
                        <option value="" disabled>{{ cidadePlaceholder }}</option>
                        <option v-for="cidade in cidades" :key="cidade.id" :value="cidade.nome">{{
                cidade.nome }}</option>
                    </select>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.latitude" :class="{'is-invalid': !isLatitudeValida}" type="text" class="form-control"
                        :placeholder="latitudePlaceholder" @input="aplicarLatMask" id="latitude">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.longitude" :class="{'is-invalid': !isLongitudeValida}" type="text" class="form-control"
                        :placeholder="longitudePlaceholder" @input="aplicarLongMask" id="longitude" >
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.area" :class="{'is-invalid': !isAreaValida}" type="text" class="form-control"
                        @input="aplicarAreaMask" :placeholder="areaPlaceholder" id="area" >
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('propriedades')">Cancelar</button>
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
            activeTab: 'edicao', // Começa na aba de edição
            estados: [],
            cidades: [],
            formData: {
                id: null,
                nome: '',
                endereco: '',
                estado: '',
                cidade: '',
                latitude: '',
                longitude: '',
                area: '',
                produtor: [],
            },
            isNomeValido: true,
            isCidadeValida: true,
            isEstadoValido: true,
            isEnderecoValido: true,
            isLatitudeValida: true,
            isLongitudeValida: true,
            isAreaValida: true,
            nomePlaceholder: 'Nome da propriedade',
            cidadePlaceholder: 'Cidade',
            estadoPlaceholder: 'Estado',
            enderecoPlaceholder: 'Endereço',
            latitudePlaceholder: 'Latitude',
            longitudePlaceholder: 'Longitude',
            areaPlaceholder: 'Área'
        };
    },
 
    mounted() {
        const propriedadeId = this.$route.params.propriedadeId;
        if (propriedadeId) {
            this.fetchPropriedade(propriedadeId);
        }
        this.buscarEstadosDaApi();
    },
    methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarAreaMask(event){
      const value = event.target.value;
      this.formData.area = this.valorMask(value);
    },

    aplicarLatMask(event){
      const value = event.target.value;
      this.formData.latitude = this.latLongMask(value);
    },

    aplicarLongMask(event){
      const value = event.target.value;
      this.formData.longitude = this.latLongMask(value);
    },



//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchPropriedade(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/propriedades/${id}`);
        const propriedade = response.data;
        this.formData.id = propriedade.id;
        this.formData.nome = propriedade.nome;
        this.formData.endereco = propriedade.endereco;
        this.formData.cidade = propriedade.cidade;
        this.formData.estado = propriedade.estado;
        this.formData.latitude = this.replacePontoVirgula(propriedade.latitude);
        this.formData.longitude = this.replacePontoVirgula(propriedade.longitude);
        this.formData.area = this.replacePontoVirgula(propriedade.area);
        this.formData.produtor = propriedade.produtor;

        this.buscarCidadesPorEstado(this.formData.estado);
      } catch (error) {
        console.error('Erro ao carregar dados da propriedade:', error);
      }
    },

    async buscarCidadesPorEstado(estadoNome) {
        let estadoId;

        this.estados.forEach(estado => {
            if(estadoNome === estado.nome){
                estadoId = estado.id;
            }
        });

        try {
            const response = await api.get(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`);
            this.cidades = response.data;
        } catch (error) {
            console.error('Erro ao buscar cidades da API:', error);
        }
    },

    async buscarEstadosDaApi() {
      try {
          const response = await api.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome');
          this.estados = response.data;
      } catch (error) {
          console.error('Erro ao buscar cidades da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
       try {
        //FORMATA AREA
        this.formData.longitude = this.replaceVirgulaPonto(this.formData.longitude);
        this.formData.latitude = this.replaceVirgulaPonto(this.formData.latitude);
        this.formData.area = this.replaceVirgulaPonto(this.formData.area);

          console.log('formdata: ', this.formData);
          const response = await api.patch(`http://127.0.0.1:8000/propriedades/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/propriedades');
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
   validarFormulario(){
      
      if(this.validarLatitude()){
        this.isLatitudeValida = true;
        this.latitudePlaceholder = 'Latitude';
      }
      else{
        this.isLatitudeValida = false;
        this.latitudePlaceholder = 'Latitude Inválida'
        this.formData.latitude = null;
      }
      
      
      if(this.validarLongitude()){
        this.isLongitudeValida = true;
        this.longitudePlaceholder = 'Longitude';
      }
      else{
        this.isLongitudeValida = false;
        this.longitudePlaceholder = 'Longitude Inválida';
        this.formData.longitude = null;
      }
      
      return(this.isLatitudeValida && this.isLongitudeValida)
    },

    verificaVazio(){
      //NOME DA PROPRIEDADE
      if(this.formData.nome != null){
        if(this.formData.nome.trim() != ''){
          this.isNomeValido = true;
          this.nomePlaceholder = 'Nome da Propriedade*';
        }
        else{
          this.isNomeValido = false;
          this.nomePlaceholder = 'Nome da Propriedade é um Campo Obrigatório';
        }
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome da Propriedade é um Campo Obrigatório';
      }

      //ENDEREÇO
      if(this.formData.endereco != null){
        if(this.formData.endereco.trim() != ''){
          this.isEnderecoValido = true;
          this.enderecoPlaceholder = 'Endereço da Propriedade*'
        }
        else{
          this.isEnderecoValido = false;
          this.enderecoPlaceholder = 'Endereço da Propriedade é um Campo Obrigatório';
        }
      }
      else{
        this.isEnderecoValido = false;
        this.enderecoPlaceholder = 'Endereço da Propriedade é um Campo Obrigatório';
      }

      //ESTADO
      if(this.formData.estado != null){
        if(this.formData.estado != ''){
          this.isEstadoValido = true;
          this.estadoPlaceholder = 'Estado*';
        }
        else{
          this.isEstadoValido = false;
          this.estadoPlaceholder = 'Estado é um Campo Obrigatório';
        }
      }
      else{
        this.isEstadoValido = false;
        this.estadoPlaceholder = 'Estado é um Campo Obrigatório';
      }

      //CIDADE
      if(this.formData.cidade != null){
        if(this.formData.cidade != ''){
          this.isCidadeValida = true;
          this.cidadePlaceholder = 'Cidade*';
        }
        else{
          this.isCidadeValida = false;
          this.cidadePlaceholder = 'Cidade é um Campo Obrigatório'
        }
      }
      else{
        this.isCidadeValida = false;
        this.cidadePlaceholder = 'Cidade é um Campo Obrigatório'
      }

      //LATITUDE
      if(this.formData.latitude != null && this.formData.latitude.trim() == ''){
        this.formData.latitude = null;
      }
      
      //LONGITUDE
      if(this.formData.longitude != null && this.formData.longitude.trim() == ''){
        this.formData.longitude = null;
      }

      //ÁREA
      if(this.formData.area != null){
        if(this.formData.area.trim() != ''){
          this.isAreaValida = true;
          this.areaPlaceholder = 'Área da Propriedade*'
        }
        else{
          this.isAreaValida = false;
          this.areaPlaceholder = 'Área da Propriedade é um Campo Obrigatório';
        }
      }
      else{
        this.isAreaValida = false;
        this.areaPlaceholder = 'Área da Propriedade é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isEnderecoValido &&
        this.isEstadoValido &&
        this.isCidadeValida &&
        this.isAreaValida
      );
    },

    validarLatitude() {
      if(this.formData.latitude != null){
        const lat = parseFloat(this.replaceVirgulaPonto(this.formData.latitude));
        return (lat >= -90 && lat <= 90);
      }
      else{
        return true;
      }
    },

    validarLongitude() {
      if(this.formData.longitude != null){
        const lon = parseFloat(this.replaceVirgulaPonto(this.formData.longitude));
        return (lon >= -180 && lon <= 180);
      }
      else{
        return true;
      }
    },



//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'propriedades') {
        this.$router.push('/propriedades');
      }
    },

    cancelarEdicao() {
      this.$router.push('/propriedades');
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

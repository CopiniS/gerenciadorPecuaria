
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
          <form @submit.prevent="submitForm" @keydown="checkEnter">
              <div class="mb-3 input-group">
                    <h2 id="legenda">* Campos Obrigatórios</h2>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text" title="Nome da Popriedade"><i class="fas fa-landmark"></i></span>
                    <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" 
                    class="form-control" :placeholder="nomePlaceholder" id="nome" title="Nome da Propriedade">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text" title="Endereço da Propriedade"><i class="fas fa-map-marker-alt"></i></span>
                    <input v-model="formData.endereco" :class="{'is-invalid': !isEnderecoValido}" type="text" class="form-control"
                        :placeholder="enderecoPlaceholder" id="endereco" title="Endereço da Propriedade">
                </div>
                <div ref="dropdownEstado" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsEstado('up')"
                  @keydown.down.prevent="navigateOptionsEstado('down')" @keydown.enter.prevent="selectHighlightedEstado">
                  <div class="select-option mb-3 input-group" @click.stop="toggleDropdownEstado">
                    <span class="input-group-text" @click="filterEstados" title="Estado da Propriedade"><i class="fas fa-user-tag"></i></span>
                    <input v-model="formData.estado" :class="{ 'is-invalid': !isEstadoValido }" @input="inputEstado"
                      @click="filterEstados" @keydown.up.prevent="navigateOptionsEstado('up')"
                      @keydown.down.prevent="navigateOptionsEstado('down')" type="text" class="form-control"
                      :placeholder="estadoPlaceholder" id="caixa-select" title="Estado da Propriedade">
                  </div>
                  <div class="itens" v-show="dropdownEstadoOpen">
                    <ul class="options">
                      <li v-for="(estado, index) in estadosFiltrados" :key="estado.id" :value="estado.nome"
                        @click="selectEstado(estado)" :class="{ 'highlighted': index === highlightedIndexEstado }">{{
                        estado.nome }}</li>
                    </ul>
                  </div>
                </div>
                
                <div ref="dropdownCidade" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsCidade('up')"
                  @keydown.down.prevent="navigateOptionsCidade('down')" @keydown.enter.prevent="selectHighlightedCidade">
                  <div class="select-option mb-3 input-group" @click.stop="toggleDropdownCidade">
                    <span class="input-group-text" @click="filterCidades" title="Cidade da Propriedade"><i class="fas fa-user-tag"></i></span>
                    <input v-model="formData.cidade" :class="{ 'is-invalid': !isCidadeValida }" @input="inputCidade"
                      @click="filterCidades" @keydown.up.prevent="navigateOptionsCidade('up')"
                      @keydown.down.prevent="navigateOptionsCidade('down')" type="text" class="form-control"
                      :placeholder="cidadePlaceholder" id="caixa-select" title="Cidade da Propriedade">
                  </div>
                  <div class="itens" v-show="dropdownCidadeOpen">
                    <ul class="options">
                      <li v-for="(cidade, index) in cidadesFiltradas" :key="cidade.id" :value="cidade.nome"
                        @click="selectCidade(cidade)" :class="{ 'highlighted': index === highlightedIndexCidade }">{{
                        cidade.nome }}</li>
                    </ul>
                  </div>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"  title="Latitude da Propriedade"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.latitude" :class="{'is-invalid': !isLatitudeValida}" type="text" class="form-control"
                    :placeholder="latitudePlaceholder" @input="aplicarLatMask" id="latitude" title="Latitude da Propriedade">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text" title="Longitude da Propriedade"><i class="fas fa-map" ></i></span>
                    <input v-model="formData.longitude" :class="{'is-invalid': !isLongitudeValida}" type="text" class="form-control"
                        :placeholder="longitudePlaceholder" @input="aplicarLongMask" id="longitude" title="Longitude da Propriedade">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text" title="Área da Propriedade"><i class="fas fa-ruler-combined"></i></span>
                    <input v-model="formData.area" type="text" class="form-control"  :class="{'is-invalid': !isAreaValida}"
                        @input="aplicarAreaMask" :placeholder="areaPlaceholder" id="area" title="Área da Propriedade">
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('propriedades')">Cancelar</button>
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

export default {
  mixins: [masksMixin],
  
    data() {
        return {
            activeTab: 'edicao', // Começa na aba de edição
            estados: [],
            estadosFiltrados: [],
            dropdownEstadoOpen: false,
            highlightedIndexEstado: -1,
            cidades: [],
            cidadesFiltradas: [],
            dropdownCidadeOpen: false,
            highlightedIndexCidade: -1,
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
        document.addEventListener('click', this.handleClickOutsideEstado);
        document.addEventListener('click', this.handleClickOutsideCidade);
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


//LÓGICA DOS SELECT ESTADO----------------------------------------------------------------------------------------------------------------------------------------------------
    filterEstados() {
        this.estadosFiltrados = this.estados.filter(estado => estado.nome.toLowerCase().includes(this.formData.estado.toLowerCase()));        
    },

    selectEstado(estado) {
        this.formData.estado = estado.nome;
        this.estadosFiltrados = [];
        this.dropdownEstadoOpen = false;
        this.buscarCidadesPorEstado(estado.nome);
    },

    toggleDropdownEstado() {
      this.dropdownEstadoOpen = !this.dropdownEstadoOpen;
      let nomeCorreto = false;
      
      if(!this.dropdownEstadoOpen){
        this.estadosFiltrados.forEach(estado => {
          if(estado.nome.toLowerCase() == this.formData.estado.toLowerCase()){
            this.formData.estado = estado.nome;
            this.estadosFiltrados = [];
            this.buscarCidadesPorEstado(estado.nome);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.estado = '';
          this.cidades = [];
          this.formData.cidade = '';
        }
      }

      else if(this.dropdownCidadeOpen){
        this.cidades.forEach(cidade => {
          if(cidade.nome.toLowerCase() === this.formData.cidade.toLowerCase()){
            this.formData.cidade = cidade.nome;
            this.cidadesFiltradas = [];
            nomeCorreto = true;
            
          }
        });
        if(!nomeCorreto){
          this.formData.cidade = '';
        }
        this.dropdownCidadeOpen = false;
      }
    },

    handleClickOutsideEstado(event) {
      if (this.dropdownEstadoOpen && this.$refs.dropdownEstado && !this.$refs.dropdownEstado.contains(event.target)) {
        this.dropdownEstadoOpen = false;
      }
      let nomeCorreto = false;
      if(!this.dropdownEstadoOpen){
        this.estados.forEach(estado => {
          if(estado.nome.toLowerCase() === this.formData.estado.toLowerCase()){
            this.formData.estado = estado.nome;
            this.estadosFiltrados = [];
            this.buscarCidadesPorEstado(estado.nome);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.estado = '';
          this.cidades = [];
          this.formData.cidade = '';
        }
      }
    },

    inputEstado(){
      this.filterEstados();
      this.dropdownEstadoOpen = true;
    },

    navigateOptionsEstado(direction) {
      if (direction === 'up' && this.highlightedIndexEstado > 0) {
        this.highlightedIndexEstado--;
      } else if (direction === 'down' && this.highlightedIndexEstado < this.estadosFiltrados.length - 1) {
        this.highlightedIndexEstado++;
      }
    },

    selectHighlightedEstado() {
      if (this.highlightedIndexEstado >= 0 && this.highlightedIndexEstado < this.estadosFiltrados.length) {
        this.selectEstado(this.estadosFiltrados[this.highlightedIndexEstado]);
      }
    },



//LÓGICA DOS SELECT CIDADE----------------------------------------------------------------------------------------------------------------------------------------------------
    filterCidades() {
        this.cidadesFiltradas = this.cidades.filter(cidade => cidade.nome.toLowerCase().includes(this.formData.cidade.toLowerCase()));        
    },

    selectCidade(cidade) {
        this.formData.cidade = cidade.nome;
        this.cidadesFiltradas = [];
        this.dropdownCidadeOpen = false;
    },

    toggleDropdownCidade() {
      this.dropdownCidadeOpen = !this.dropdownCidadeOpen;
      let nomeCorreto = false;

      if(!this.dropdownCidadeOpen){
        this.cidadesFiltradas.forEach(cidade => {
          if(cidade.nome.toLowerCase() === this.formData.cidade.toLowerCase()){
            this.formData.cidade = cidade.nome;
            this.cidadesFiltradas = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.cidade = '';
        }
      }
      
      else if(this.dropdownEstadoOpen){
        this.estados.forEach(estado => {
          if(estado.nome.toLowerCase() === this.formData.estado.toLowerCase()){
            this.formData.estado = estado.nome;
            this.estadosFiltrados = [];
            this.buscarCidadesPorEstado(estado.nome);
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.estado = '';
          this.cidades = [];
          this.cidadesFiltradas = [];
          this.formData.cidade = '';
        }
        this.dropdownEstadoOpen = false;
      }
    },

    handleClickOutsideCidade(event) {
      if (this.dropdownCidadeOpen && this.$refs.dropdownCidade && !this.$refs.dropdownCidade.contains(event.target)) {
        this.dropdownCidadeOpen = false;
      }
      let nomeCorreto = false;
      if(!this.dropdownCidadeOpen){
        this.cidades.forEach(cidade => {
          if(cidade.nome.toLowerCase() === this.formData.cidade.toLowerCase()){
            this.formData.cidade = cidade.nome;
            this.cidadesFiltradas = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.formData.cidade = '';
        }
      }
    },

    inputCidade(){
      this.filterCidades();
      this.dropdownCidadeOpen = true;
    },

    navigateOptionsCidade(direction) {
      if (direction === 'up' && this.highlightedIndexCidade > 0) {
        this.highlightedIndexCidade--;
      } else if (direction === 'down' && this.highlightedIndexCidade < this.cidadesFiltradas.length - 1) {
        this.highlightedIndexCidade++;
      }
    },

    selectHighlightedCidade() {
      if (this.highlightedIndexCidade >= 0 && this.highlightedIndexCidade < this.cidadesFiltradas.length) {
        this.selectCidade(this.cidadesFiltradas[this.highlightedIndexCidade]);
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
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
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
</style>

<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'propriedades' }" id="nav-vet-tab" @click="selectTab('propriedades')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Propriedade</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Propriedade</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'propriedades' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Propriedade</h1>
            <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                    <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" class="form-control" :placeholder="nomePlaceholder"
                        id="nome">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>
                    <input v-model="formData.endereco" :class="{'is-invalid': !isEnderecoValido}" type="text" class="form-control"
                        :placeholder="enderecoPlaceholder" id="endereco">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-flag"></i></span>
                    <select v-model="formData.estado" :class="{'is-invalid': !isCidadeValida}" class="form-select"
                        @change="buscarCidadesPorEstado($event.target.value)">
                        <option value="" disabled>{{ estadoPlaceholder }}</option>
                        <option v-for="estado in estados" :key="estado.id" :value="estado.nome">{{ estado.nome
                            }}</option>
                    </select>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-city"></i></span>
                    <select v-model="formData.cidade" :class="{'is-invalid': !isEstadoValido}" class="form-select" required>
                        <option value="">{{ cidadePlaceholder }}</option>
                        <option v-for="cidade in cidades" :key="cidade.id" :value="cidade.nome">{{
                cidade.nome }}</option>
                    </select>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.latitude" :class="{'is-invalid': !isLatitudeValida}" type="text" class="form-control"
                        :placeholder="latitudePlaceholder" id="latitude">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.longitude" :class="{'is-invalid': !isLongitudeValida}" type="text" class="form-control"
                        :placeholder="longitudePlaceholder" id="longitude">
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-globe"></i></span>
                    <input v-model="formData.area" :class="{'is-invalid': !isAreaValida}" type="text" class="form-control"
                        :placeholder="areaPlaceholder" id="area">
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

export default {
  data() {
    return {
        activeTab: 'cadastro',  // Aba inicial é 'cadastro'
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
        this.buscarEstadosDaApi();
    },
    
    methods: {

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

    validarFormulario(){
      this.isNomeValido = !!this.nome;
      this.isCidadeValida = !!this.cidade;
      this.isEstadoValido = !!this.estado;
      this.isEnderecoValido = !!this.endereco;
      this.isLatitudeValida = this.validarLatitude(this.latitude);
      this.isLongitudeValida = this.validarLongitude(this.longitude);
      this.isAreaValida = !!this.area;

      return this.isNomeValido && this.isCidadeValida && this.isEstadoValido && this.isEnderecoValido && this.isLatitudeValida && this.isLongitudeValida && this.isAreaValida;
    },
    validarLatitude(latitude) {
      const lat = parseFloat(latitude);
      return !isNaN(lat) && lat >= -90 && lat <= 90;
    },
    validarLongitude(longitude) {
      const lon = parseFloat(longitude);
      return !isNaN(lon) && lon >= -180 && lon <= 180;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'propriedades') {
        this.$router.push('/propriedades');
      }
    },

    async submitForm() {
        try {
            const response = await api.post('http://127.0.0.1:8000/propriedades/', this.formData);

            if (response.status === 201) {
                alert('Cadastro realizado com sucesso!');
                this.$router.push('/propriedades');
            } else {
                alert('Erro ao cadastrar propriedade. Tente novamente mais tarde');
            }
        } catch (error) {
            console.error('Erro ao enviar requisição:', error);
            alert('Erro ao enviar requisição. Verifique o console para mais detalhes');
        }
        this.$router.push('/propriedades');
    },

    resetForm() {
      this.formData = {
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
        this.isNomeValido = true,
        this.isCidadeValida = true,
        this.isEstadoValido = true,
        this.isEnderecoValido = true,
        this.isLatitudeValida = true,
        this.isLongitudeValida = true,
        this.isAreaValida = true,
        this.nomePlaceholder = 'Nome da propriedade',
        this.cidadePlaceholder = 'Cidade',
        this.estadoPlaceholder = 'Estado',
        this.enderecoPlaceholder = 'Endereço',
        this.latitudePlaceholder = 'Latitude',
        this.longitudePlaceholder = 'Longitude',
        this.areaPlaceholder = 'Área'
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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}

</style>

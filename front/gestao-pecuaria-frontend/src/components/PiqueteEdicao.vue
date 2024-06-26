
<template>
  <div class="background">
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
          <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" class="form-control" 
                id="nome" :placeholder="nomePlaceholder">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <select v-model="formData.tipoCultivo" :class="{'is-invalid': !isTipoCultivoValido}" 
                class="form-select" id="tipoCultivo" aria-label="Tipo de Cultivo">
                  <option disabled value="">{{ tipoCultivoPlaceholder }}</option>
                  <option>Pastagem Natural</option>
                  <option>Lavoura</option>
                  <option>Confinamento</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.area" :class="{'is-invalid': !isAreaValida}" type="text" class="form-control" 
                id="area" :placeholder="areaPlaceholder">
              </div>
              <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('piquetes')">Cancelar</button>
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
            activeTab: 'edicao', // Começa na aba de edição
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
            nomePlaceholder: 'Nome do Piquete',
            tipoCultivoPlaceholder: 'Tipo do cultivo',
            areaPlaceholder: 'Área do Piquete',
        };
    },
 
    mounted() {
        const piqueteId = this.$route.params.piqueteId;
        if (piqueteId) {
            this.fetchPiquete(piqueteId);
        }
    },
    methods: {
    async fetchPiquete(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/piquetes/${id}`);
        const piquete = response.data;
        this.formData.id = piquete.id;
        this.formData.nome = piquete.nome;
        this.formData.tipoCultivo = piquete.tipoCultivo;
        this.formData.area = piquete.area;
      } catch (error) {
        console.error('Erro ao carregar dados da piquete:', error);
      }
    },
    validarFormulario() {
      this.isNomeValido = !!this.formData.nome.trim();
      if (!this.isNomeValido) this.nomePlaceholder = 'Campo Nome do Piquete é obrigatório';

      this.isTipoCultivoValido = !!this.formData.tipoCultivo.trim();
      if (!this.isTipoCultivoValido) this.tipoCultivoPlaceholder = 'Campo Tipo do cultivo é obrigatório';

      this.isAreaValida = !!this.formData.area.trim();
      if (!this.isAreaValida) this.areaPlaceholder = 'Campo Área do Piquete é obrigatório';

      return this.isNomeValido && this.isTipoCultivoValido && this.isAreaValida;
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

    async submitForm() {
      if (this.validarFormulario()) {
       try {
          const response = await api.patch(`http://127.0.0.1:8000/piquetes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.$router.push('/piquetes');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipoCultivo: '',
        area: '',
        propriedade: localStorage.getItem('propriedadeSelecionada')
      };

      this.isNomeValido = true,
      this.isTipoCultivoValido = true,
      this.isAreaValida = true,
      this.nomePlaceholder = 'Nome do Piquete',
      this.tipoCultivoPlaceholder = 'Tipo do cultivo'
      this.areaPlaceholder = 'Área do Piquete'
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

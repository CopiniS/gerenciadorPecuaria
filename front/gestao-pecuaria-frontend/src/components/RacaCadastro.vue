<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'racas' }" id="nav-vet-tab" @click="selectTab('racas')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Raca</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Raca</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'racas' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Raca</h1>
            <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tag"></i></span>
                  <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" 
                  class="form-control" id="nome" :placeholder="nomePlaceholder" required>
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('racas')">Cancelar</button>
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
      formData: {
        id: null,
        nome: ''
      },
      isNomeValido: true,
      nomePlaceholder: 'Nome da Raca',
    };
  },
  methods: {

    validarFormulario(){
      this.isNomeValido = !!this.formData.racaPredominante && this.formData.racaPredominante.trim() !== '';
      return this.isNomeValido;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'racas') {
        this.$router.push('/racas');
      }
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/racas/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.$router.push('/racas');
          } else {
            alert('Erro ao cadastrar raca. Tente novamente mais tarde.');
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
        nome: ''
      },
      this.isNomeValido = true,
      this.nomePlaceholder = 'Nome da Raca'
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

<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'veterinarios' }" id="nav-vet-tab"
          @click="selectTab('veterinarios')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Veterinário</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Veterinário</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'veterinarios' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Veterinário</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.nome" :class="{ 'is-invalid': !isNomeValido }" type="text" class="form-control"
                id="nome" :placeholder="nomePlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-phone"></i></span>
              <input v-model="formData.telefone" @input="aplicarTelefoneMask" :class="{ 'is-invalid': !isTelefoneValido }"
                type="text" class="form-control" id="telefone" :placeholder="telefonePlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-envelope"></i></span>
              <input v-model="formData.email" :class="{ 'is-invalid': !isEmailValido }" type="email" class="form-control"
                id="email" :placeholder="emailPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-id-card"></i></span>
              <input v-model="formData.crmv" :class="{ 'is-invalid': !isCrmvValido }" type="text" class="form-control"
                id="crmv" :placeholder="crmvPlaceholder">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="cancelarEdicao">Cancelar</button>
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

  name: 'TelaVeterinarios',
  data() {
    return {
      activeTab: 'edicao', // Começa na aba de edição
      formData: {
        id: null,
        nome: '',
        telefone: '',
        email: '',
        crmv: '',
      },
      isNomeValido: true,
      isTelefoneValido: true,
      isEmailValido: true,
      isCrmvValido: true,
      nomePlaceholder: 'Nome*',
      telefonePlaceholder: 'Telefone*',
      emailPlaceholder: 'Email',
      crmvPlaceholder: 'CRMV*',
    };
  },
  mounted() {
    const veterinarioId = this.$route.params.veterinarioId;
    if (veterinarioId) {
      this.fetchVeterinario(veterinarioId);
    }
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarTelefoneMask(event) {
      const value = event.target.value;
      this.formData.telefone = this.telefoneMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchVeterinario(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/veterinarios/${id}`);
        const veterinario = response.data;
        this.formData.id = veterinario.id;
        this.formData.nome = veterinario.nome;
        this.formData.telefone = veterinario.telefone;
        this.formData.email = veterinario.email;
        this.formData.crmv = veterinario.crmv;
      } catch (error) {
        console.error('Erro ao carregar dados do veterinário:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/veterinarios/${this.formData.id}/`, this.formData, {});
          if (response.status === 200) {
            alert('Veterinário atualizado com sucesso!');
            this.$router.push('/veterinarios');
          } else {
            alert('Erro ao atualizar veterinário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },



//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(this.formData.telefone)){
        this.isTelefoneValido = true;
        this.telefonePlaceholder = 'Telefone';
      }
      else{
        this.isTelefoneValido = false;
        this.formData.telefone = null;
        this.telefonePlaceholder = 'Telefone Inválido';
      }

      if (this.formData.email == null || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.formData.email)){
          this.isEmailValido = true;
          this.emailPlaceholder = 'Email';
      }
      else{
        this.isEmailValido = false;
         this.formData.email = null;
         this.emailPlaceholder = 'Email Inválido';
      }
      return (this.isTelefoneValido && this.isEmailValido);
    },

    verificaVazio(){
      //NOME
      if(this.formData.nome != null && this.formData.nome.trim() != ''){
        this.isNomeValido = true;
        this.nomePlaceholder = 'Nome do Veterinário*';
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome do Veterinário é um Campo Obrigatório';
      }
      
      //TELEFONE
      if(this.formData.telefone != null && this.formData.telefone.trim() != ''){
        this.isTelefoneValido = true;
        this.telefonePlaceholder = 'Telefone do Veterinário*';
      }
      else{
        this.isTelefoneValido = false;
        this.telefonePlaceholder = 'Telefone do Veterinário é um Campo Obrigatório';
      }
      //EMAIL
      if(this.formData.email != null && this.formData.email.trim() == ''){
        this.formData.email = null;
      }

      //CRMV
      if(this.formData.crmv != null && this.formData.crmv.trim() != ''){
        this.isCrmvValido = true;
        this.crmvPlaceholder = 'CRMV do Veterinário*';
      }
      else{
        this.isCrmvValido = false;
        this.crmvPlaceholder = 'CRMV do Veterinário é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isTelefoneValido &&
        this.isCrmvValido
      );

    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'veterinarios') {
        this.$router.push('/veterinarios');
      }
    },

    cancelarEdicao() {
      this.$router.push('/veterinarios');
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

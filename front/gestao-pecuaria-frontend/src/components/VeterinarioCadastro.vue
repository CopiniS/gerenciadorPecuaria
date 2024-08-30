<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'veterinarios' }" id="nav-vet-tab" @click="selectTab('veterinarios')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Veterinários</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Veterinários</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'veterinarios' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Veterinários</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Nome"><i class="fas fa-user-md"></i></span>
              <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" 
              class="form-control" id="nome" :placeholder="nomePlaceholder" title="Nome" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Telefone"><i class="fas fa-phone"></i></span>
              <input
                v-model="formData.telefone"
                @input="aplicarTelefoneMask"
                :class="{'is-invalid': !isTelefoneValido}"
                autocomplete="off"
                type="text"
                class="form-control"
                id="telefone"
                :placeholder="telefonePlaceholder" title="Telefone">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Email"><i class="fas fa-envelope"></i></span>
              <input v-model="formData.email" :class="{'is-invalid': !isEmailValido}" type="email" 
              class="form-control" id="email" :placeholder="emailPlaceholder" title="Email" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="CRMV"><i class="fas fa-id-card"></i></span>
              <input v-model="formData.crmv" :class="{'is-invalid': !isCrmvValido}" type="text" 
              class="form-control" id="crmv" :placeholder="crmvPlaceholder" title="CRMV" autocomplete="off">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('veterinarios')">Cancelar</button>
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

  name: 'TelaVeterinarios',
  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      veterinariosDaApi: null,
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
    this.buscarVeterinariosDaApi();
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarTelefoneMask(event) {
      const value = event.target.value;
      this.formData.telefone = this.telefoneMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/veterinarios/', this.formData, {});
          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/veterinarios');
          } else {
            alert('Erro ao cadastrar veterinário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
    },

    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/' , {
          // Parâmetros da requisição (se houver)
        });
        this.veterinariosDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(this.formData.telefone)){
        this.isTelefoneValido = true;
        this.telefonePlaceholder = 'Telefone*';
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

      this.isCrmvValido = true;
      this.crmvPlaceholder = 'CRMV*';

      for (let veterinario of this.veterinariosDaApi) {
        if (veterinario.crmv === this.formData.crmv) {
          this.isCrmvValido = false;
          this.crmvPlaceholder = 'Este CRMV já está cadastrado no sistema';
          this.formData.crmv = null;
          break;
        }
      }
      return (this.isTelefoneValido && this.isEmailValido && this.isCrmvValido);
    },

    verificaVazio(){
      //NOME
      if(this.formData.nome != null && this.formData.nome.trim() != ''){
        this.isNomeValido = true;
        this.nomePlaceholder = 'Nome*';
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome é um Campo Obrigatório';
      }
      
      //TELEFONE
      if(this.formData.telefone != null && this.formData.telefone.trim() != ''){
        this.isTelefoneValido = true;
        this.telefonePlaceholder = 'Telefone*';
      }
      else{
        this.isTelefoneValido = false;
        this.telefonePlaceholder = 'Telefone é um Campo Obrigatório';
      }
      //EMAIL
      if(this.formData.email != null && this.formData.email.trim() == ''){
        this.formData.email = null;
      }

      //CRMV
      if(this.formData.crmv != null && this.formData.crmv.trim() != ''){
        this.isCrmvValido = true;
        this.crmvPlaceholder = 'CRMV*';
      }
      else{
        this.isCrmvValido = false;
        this.crmvPlaceholder = 'CRMV é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isTelefoneValido &&
        this.isCrmvValido
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
      if (tab === 'veterinarios') {
        this.$router.push('/veterinarios');
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

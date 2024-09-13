<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Meu Perfil</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Meu Perfil</h1>
          <form @submit.prevent="submitForm">
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text" title="Nome"><i class="fas fa-user"></i></span>
            <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" 
            class="form-control" id="nome" :placeholder="nomePlaceholder" title="Nome" autocomplete="off">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text" title="CPF"><i class="fas fa-id-card"></i></span>
            <input v-model="formData.cpf" type="text" class="form-control" id="cpf" @input="aplicarCpfMask"
            :class="{'is-invalid': !isCpfValido}" :placeholder="cpfPlaceholder" title="CPF" autocomplete="off">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text" title="Telefone 1"><i class="fas fa-phone"></i></span>
            <input v-model="formData.telefone1" type="tel" class="form-control" @input="aplicarTelefone1Mask"
            :class="{'is-invalid': !isTelefone1Valido}" id="telefone1" :placeholder="telefone1Placeholder"
            title="Telefone 1" autocomplete="off">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text" title="Telefone 2"><i class="fas fa-phone"></i></span>
            <input v-model="formData.telefone2" type="tel" class="form-control" id="telefone2" 
            :placeholder="telefone2Placeholder" @input="aplicarTelefone2Mask" :class="{'is-invalid': !isTelefone2Valido}"
            title="Telefone 2" autocomplete="off">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
            <input v-model="formData.email" type="email" :class="{'is-invalid': !isEmailValido}" class="form-control" id="email" :placeholder="emailPlaceholder" >
          </div>
        </div>
        <div class="mb-4 input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input 
            v-model="formData.password" 
            :type="passwordType" 
            class="form-control" 
            id="password" 
            :placeholder="passwordPlaceholder" 
          >
          <span class="input-group-text" @click="togglePasswordVisibility">
            <i :class="passwordType === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
          </span>
        </div>
        <div class="button-group justify-content-end">
            <button type="button" class="btn btn-secondary" @click="voltar">Cancelar</button>
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
      activeTab: 'edicao',
      formData: {
        id: '',
        nome: '',
        cpf: '',
        telefone1: '',
        telefone2: null,
        email: '',
        password: '',
      },
      isNomeValido: true,
      isCpfValido: true,
      isTelefone1Valido: true,
      isTelefone2Valido: true,
      isEmailValido: true,
      isPasswordValido: true,
      nomePlaceholder: 'Nome*',
      cpfPlaceholder: 'CPF*',
      telefone1Placeholder: 'Telefone 1*',
      telefone2Placeholder: 'Telefone 2*',
      emailPlaceholder: 'Email',
      passwordPlaceholder: 'Senha',
      passwordType: 'password', // Controla o tipo do input da senha
    };
  },

  mounted() {
    this.fetchUsuario();
  },
  
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarCpfMask(event) {
      const value = event.target.value;
      this.formData.cpf = this.cpfMask(value);
    },
    
    aplicarTelefone1Mask(event) {
      const value = event.target.value;
      this.formData.telefone1 = this.telefoneMask(value);
    },

    aplicarTelefone2Mask(event) {
      const value = event.target.value;
      this.formData.telefone2 = this.telefoneMask(value);
    },

//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchUsuario() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/meuperfil/`);
        const usuario = response.data;
        this.formData.id = usuario.id;
        this.formData.nome = usuario.nome;
        this.formData.cpf = usuario.cpf;
        this.formData.telefone1 = usuario.telefone1;
        this.formData.telefone2 = usuario.telefone2;
        this.formData.email = usuario.email;
      } catch (error) {
        console.error('Erro ao carregar dados da usuario:', error);
      }
    },
    
    async submitForm() {
      if(this.verificaVazio() && this.validarFormulario()){
        try {
          const response = await api.put('http://127.0.0.1:8000/meuperfil/', this.formData);
          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.fetchUsuario();
          } else {
            alert('Erro ao alterar produtor. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      //CPF
      if (/^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(this.formData.cpf)){
        this.isCpfValido = true;
        this.cpfPlaceholder = 'CPF*';
      }
      else{
        this.isCpfValido = false;
        this.formData.cpf = null;
        this.cpfPlaceholder = 'CPF Inválido';
      }

      //TELEFONE 1
      if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(this.formData.telefone1)){
        this.isTelefone1Valido = true;
        this.telefone1Placeholder = 'Telefone 1*';
      }
      else{
        this.isTelefone1Valido = false;
        this.formData.telefone1 = null;
        this.telefone1Placeholder = 'Telefone 1 Inválido';
      }

      //TELEFONE 2
      if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(this.formData.telefone2) || this.formData.telefone2 == null){
        this.isTelefone2Valido = true;
        this.telefone2Placeholder = 'Telefone 2*';
      }
      else{
        this.isTelefone2Valido = false;
        this.formData.telefone2 = null;
        this.telefone2Placeholder = 'Telefone 2 Inválido';
      }
      //EMAIL
      if (this.formData.email == null || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.formData.email)){
          this.isEmailValido = true;
          this.emailPlaceholder = 'Email*';
      }
      else{
        this.isEmailValido = false;
         this.formData.email = null;
         this.emailPlaceholder = 'Email Inválido';
      }
      return (this.isCpfValido && this.isTelefone1Valido && this.isEmailValido && this.isTelefone2Valido);
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

        //CPF
        if(this.formData.cpf != null && this.formData.cpf.trim() != ''){
            this.isCpfValido = true;
            this.cpfPlaceholder = 'CPF*';
        }
        else{
          this.isCpfValido = false;
          this.cpfPlaceholder = 'CPF é um Campo Obrigatório';
        }

        //Telefone 1
        if(this.formData.telefone1 != null && this.formData.telefone1.trim() != ''){
            this.isTelefone1Valido = true;
            this.telefone1Placeholder = 'Telefone 1*';
        }
        else{
          this.isTelefone1Valido = false;
          this.telefone1Placeholder = 'Telefone 1 é um Campo Obrigatório';
        }

        //Telefone 2
        if(this.formData.telefone2 != null && this.formData.telefone2.trim() == ''){
            this.formData.telefone2 = null;
        }

        //EMAIL
        if(this.formData.email != null && this.formData.email != ''){
            this.isEmailValido = true;
            this.emailPlaceholder = 'Email*';
        }
        else{
          this.isEmailValido = false;
          this.emailPlaceholder = 'Email é um Campo Obrigatório';
        }
        
        return (
          this.isNomeValido &&
          this.isCpfValido &&
          this.isTelefone1Valido &&
          this.isEmailValido
        );
    },

//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    voltar() {
      this.$router.push('/inicio');
    },
    togglePasswordVisibility() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
    },
  }
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

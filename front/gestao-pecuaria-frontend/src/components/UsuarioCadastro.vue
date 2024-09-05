<template>
  <div class="vh-100 vw-100 cadastro-container">
    <div sm="7" class="cadastro-form">
      <h2 class="text-center mb-5 title-cadastro">Faça o cadastro</h2>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-user"></i></span>
            <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" class="form-control" id="nome" :placeholder="nomePlaceholder" >
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-id-card"></i></span>
            <input v-model="formData.cpf" type="text" class="form-control" id="cpf" @input="aplicarCpfMask"
            :class="{'is-invalid': !isCpfValido}" :placeholder="cpfPlaceholder" title="Insira um CPF válido">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="formData.telefone1" type="tel" class="form-control" @input="aplicarTelefone1Mask"
            :class="{'is-invalid': !isTelefone1Valido}" id="telefone1" :placeholder="telefone1Placeholder">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="formData.telefone2" type="tel" class="form-control" id="telefone2" 
            :placeholder="telefone2Placeholder" @input="aplicarTelefone2Mask" :class="{'is-invalid': !isTelefone2Valido}">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
            <input v-model="formData.email" type="email" :class="{'is-invalid': !isEmailValido}" class="form-control" id="email" :placeholder="emailPlaceholder" >
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input v-model="formData.password" :class="{'is-invalid': !isPasswordValida}" type="password" class="form-control" id="senha" :placeholder="passwordPlaceholder" >
          </div>
        </div>

        <button type="button" class="btn btn-primary btn-block" @click="submitForm">
          <i class="fas fa-sign-in-alt"></i> Cadastrar
        </button>
        <hr />
        <button type="button" class="btn btn-outline-secondary" @click="voltar">
          <i class="fas fa-arrow-left"></i> Voltar
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { masksMixin } from '../mixins/maks';

export default {
  mixins: [masksMixin],

  data() {
    return {
      formData: {
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
      isPasswordValida: true,
      nomePlaceholder: 'Nome*',
      cpfPlaceholder: 'CPF*',
      telefone1Placeholder: 'Telefone 1*',
      telefone2Placeholder: 'Telefone 2*',
      emailPlaceholder: 'Email*',
      passwordPlaceholder: 'Senha*',
    };
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
    async submitForm() {
      if(this.verificaVazio() && this.validarFormulario()){
        try {
          const response = await axios.post('http://127.0.0.1:8000/singup', this.formData);
          if (response.status === 200) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/login')
          } else {
            alert('Erro ao cadastrar produtor. Tente novamente mais tarde.');
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

        //SEnha
        if(this.formData.password != null && this.formData.password != ''){
            this.isPasswordValida = true;
            this.passwordPlaceholder = 'Senha*';
        }
        else{
          this.isPasswordValida = false;
          this.passwordPlaceholder = 'Senha é um Campo Obrigatório';
        }
        
        return (
          this.isNomeValido &&
          this.isCpfValido &&
          this.isTelefone1Valido &&
          this.isEmailValido &&
          this.isPasswordValida
        );
    },

//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    voltar() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.cadastro-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-image: url('../assets/fundo.jpg');
  background-size: cover;
  background-position: center;
  padding: 20px; /* Adiciona algum espaçamento interno para evitar que o conteúdo toque as bordas da tela */
}

.cadastro-form {
  flex: 1;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #c2e0a6;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adiciona uma sombra suave ao formulário */
  margin: 0 auto; /* Centraliza o formulário horizontalmente */
}

.btn-primary {
  background-color: #125601;
  border-color: #125601;
}

.btn-outline-secondary {
  border-color: #125601;
  color: #125601;
}

.btn-primary:hover, .btn-outline-secondary:hover {
  background-color: #259406;
  border-color: #259406;
  color: white;
}

.btn-block {
  width: 100%;
}

.alert-custom {
  padding: 0.5rem 1rem; /* Diminui o padding do alerta */
  font-size: 0.875rem;
}


/* Ajustes para telas menores */
@media (max-width: 550px) {
  .login-container {
    padding: 10px;
  }

  .login-form {
    width: 100%;
    max-width: 100%; /* Garante que o formulário não exceda a largura da tela */
    margin: 0; /* Remove as margens laterais */
  }

  .input-group {
    flex-wrap: wrap; /* Permite que os inputs ocupem a largura total em dispositivos menores */
  }
}
</style>

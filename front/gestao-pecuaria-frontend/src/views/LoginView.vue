<template>
  <div class="login-container">
    <div class="login-form">
      <h2 class="text-center mb-5 title-login">Login</h2>
      <div v-if="errorMessage" class="alert alert-danger alert-custom mt-3">{{ errorMessage }}</div>

      <form @submit.prevent="submitForm">
        <div class="mb-4 input-group">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
          <input v-model="email" type="email" class="form-control" id="email" placeholder="Email" required>
        </div>
        <div class="mb-4 input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input v-model="password" type="password" class="form-control" id="password" placeholder="Senha" required>
        </div>

        <button type="button" class="btn btn-primary btn-block" @click="login">
          <i class="fas fa-sign-in-alt"></i> Entrar
        </button>

        <hr>

        <button type="button" class="btn btn-outline-secondary btn-block" @click="registrar">
          <i class="fas fa-user-plus"></i> Não tenho conta
        </button>
      </form>
    </div>
  </div>
</template>
<script>
import axios from 'axios'; 
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '', // Mensagem de erro
    };
  },
  methods: {
    async login() {
      this.errorMessage = ''; // Limpa a mensagem de erro antes de fazer o login

      try {
        const response = await axios.post('http://127.0.0.1:8000/token/', { 
          email: this.email, 
          password: this.password 
        });

        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('access_exp', response.data.access_exp);
        localStorage.setItem('refresh_exp', response.data.refresh_exp);
        
        this.$router.push('/propriedades-escolha');
      } catch (error) {
        this.errorMessage = 'Email ou senha incorretos.'; // Define a mensagem de erro
      }
    },
    registrar() {
      this.$router.push('/cadastro');
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.login-container {
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

.login-form {
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

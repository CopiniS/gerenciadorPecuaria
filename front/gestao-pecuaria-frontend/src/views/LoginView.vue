<template>
  <div class="login-container">
    <div class="login-content">
      <!-- Div para a logo -->
      <div class="logo-section">
        <img src="@/assets/logo-sem-fundo.png" alt="Logo" class="logo-img" />
      </div>

      <!-- Div para o formulário de login -->
      <div class="login-form-section">
        <h2 class="text-center mb-5 title-login">Login</h2>
        <div v-if="errorMessage" class="alert alert-danger alert-custom mt-3">{{ errorMessage }}</div>

        <form @submit.prevent="submitForm">
          <div class="mb-4 input-group">
            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
            <input v-model="email" type="email" class="form-control" id="email" placeholder="Email" required>
          </div>
          <div class="mb-4 input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input 
              v-model="password" 
              :type="passwordType" 
              class="form-control" 
              id="password" 
              placeholder="Senha" 
              required
            >
            <span class="input-group-text" @click="togglePasswordVisibility">
              <i :class="passwordType === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
            </span>
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
  </div>
</template>

<script>
import axios from 'axios'; 
import api from '/src/interceptadorAxios';
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '', // Mensagem de erro
      passwordType: 'password', // Controla o tipo do input da senha
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
        
        const nome = await this.retornaNomeProdutor();
        
        localStorage.setItem('produtorNome', nome);
        this.$router.push('/propriedades-escolha');
        
      } catch (error) {
        this.errorMessage = 'Email ou senha incorretos.'; // Define a mensagem de erro
      }
    },
    registrar() {
      this.$router.push('/cadastro');
    },
    
    async retornaNomeProdutor(){
      try {
        const response = await api.get('http://127.0.0.1:8000/meuperfil/', {});
        return response.data.nome;
      } catch (error) {
        console.error('Erro ao buscar propriedades da API:', error);
        return ''
      }
    },
    togglePasswordVisibility() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
    },
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('../assets/fundo.jpg');
  background-size: cover;
  background-position: center;
}

.login-content {
  display: flex;
  width: 800px;
  height: 400px;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.logo-section {
  flex: 1;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-img {
  max-width: 100%;
  height: auto;
}

.login-form-section {
  flex: 1;
  padding: 40px;
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
  padding: 0.5rem 1rem;
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

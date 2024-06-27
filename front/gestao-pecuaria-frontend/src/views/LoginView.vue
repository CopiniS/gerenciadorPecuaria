<template>
  <div class="vh-100 vw-100 login-container">
    <div sm="7" class="login-form">
      <h2 class="text-center mb-5 title-login">Login</h2>
      <form @submit.prevent="submitForm">
        <div class="mb-5 input-group">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
          <input v-model="email" type="email" class="form-control" id="email" placeholder="Email" required>
        </div>
        <div class="mb-5 input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input v-model="password" type="password" class="form-control" id="password" placeholder="Senha" required>
        </div>

        <button type="button" class="btn btn-primary" @click="login">
          <i class="fas fa-sign-in-alt"></i> Entrar
        </button>

        <hr>

        <button type="button" class="btn btn-outline-secondary" @click="this.registrar()">
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
    };
  },
  methods: {
    async login() {
      const response = await axios.post('http://127.0.0.1:8000/token/', { 
        email: this.email, 
        password: this.password 
      });

      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('access_exp', response.data.access_exp);
      localStorage.setItem('refresh_exp', response.data.refresh_exp);
      
      alert('Login feito com sucesso');
      this.$router.push('/propriedades-escolha');
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
  background-image: url('../assets/fundo.jpg');
  background-size: cover;
  background-position: center;
}

.login-form {
  flex: 1;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #358137;
  border-radius: 5px;
  margin-left: 150px;
  margin-right: 150px;
}
.title-login {
  color: #358137;
}

.input-group-text {
  background-color: #358137;
  color: white;
  border: 1px solid #358137;
}

.form-control {
  border: 1px solid #358137;
}

.btn-primary {
  background-color: #358137;
  border-color: #358137;
}

.btn-outline-secondary {
  border-color: #358137;
  color: #358137;
}

.btn-primary:hover, .btn-outline-secondary:hover {
  background-color: #3be949;
  border-color: #3be949;
  color: white;
}

.btn-block {
  width: 100%;
}
</style>
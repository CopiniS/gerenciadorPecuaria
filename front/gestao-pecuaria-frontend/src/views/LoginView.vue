<template>
  <div class="vh-100 vw-100 login-container">
    <div sm="7" class="login-form">
      <h2 class="text-center mb-5 title-login">Faça o login</h2>
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

        <button type="button" class="btn btn-outline-secondary" @click="registrar">
          <i class="fas fa-user-plus"></i> Não tenho conta
        </button>
      </form>
    </div>
    <div sm="5" class="vh-100 login-image">
      <img src="../assets/login.svg" width="600" height="600">
    </div>

  </div>
</template>

<script>
import axios from 'axios'; // Certifique-se de importar o axios se ainda não estiver importado

export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      console.log(this.email);
      console.log(this.password);
      axios.post('http://127.0.0.1:8000/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
          alert('Login bem-sucedido!');
          setTimeout(() => {
            const access_token = response.data.access_token; 
            localStorage.setItem('access_token', access_token);
            console.log(access_token);
          }, 1000);
          this.$router.push('/propriedades');
          console.log('Login bem-sucedido!', response.data);
        })
        .catch(error => {
          alert('Login ou senha invalidos');
          console.error('Erro durante o login:', error.response.data);
        });
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
}

.login-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f2f2f2;
}


.login-form {
  flex: 1;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-left: 150px;
  margin-right: 150px;
}
</style>
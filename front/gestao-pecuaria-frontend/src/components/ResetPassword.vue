<template>
    <div class="reset-password-container">
      <div class="reset-password-form">
        <h2 class="text-center mb-5">Redefinir Senha</h2>
        <div v-if="message" :class="['alert', message.type === 'success' ? 'alert-success' : 'alert-danger']">
          {{ message.text }}
        </div>

        <form @submit.prevent="resetPassword" v-if="!message.type">
          <div class="mb-4 input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input v-model="newPassword" :type="passwordType" class="form-control" id="newPassword" placeholder="Nova Senha" required>
            <span class="input-group-text" @click="togglePasswordVisibility">
              <i :class="passwordType === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
            </span>
          </div>
          <div class="mb-4 input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input v-model="confirmPassword" :type="passwordType" class="form-control" id="confirmPassword" placeholder="Confirmar Nova Senha" required>
          </div>

          <button type="submit" class="btn btn-primary btn-block">
            <i class="fas fa-save"></i> Salvar Nova Senha
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
        newPassword: '',
        confirmPassword: '',
        passwordType: 'password',
        message: { type: '', text: '' },
        uid: '',
        token: ''
      };
    },
    created() {
      // Extrair UID e token da URL
      this.uid = this.$route.params.uid;
      this.token = this.$route.params.token;
    },
    methods: {
      togglePasswordVisibility() {
        this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
      },
      async resetPassword() {
        if (this.newPassword !== this.confirmPassword) {
          this.message = { type: 'error', text: 'As senhas não coincidem.' };
          return;
        }
  
        try {
          const response = await axios.post('http://127.0.0.1:8000/redefinir-senha/', {
            uid: this.uid,
            token: this.token,
            new_password: this.newPassword
          });
  
          if (response.status === 200) {
            this.message = { type: 'success', text: 'Senha redefinida com sucesso. Você será redirecionado para a página de login.' };
            setTimeout(() => {
              this.$router.push('/login');
            }, 3000);
          }
        } catch (error) {
          console.error('Erro ao redefinir a senha:', error);
          this.message = { type: 'error', text: 'Ocorreu um erro ao redefinir a senha. Por favor, tente novamente.' };
        }
      }
    }
  };
  </script>

  <style scoped>
  .reset-password-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('../assets/fundo.jpg');
    background-size: cover;
    background-position: center;
    padding: 20px;
  }
  
  .reset-password-form {
    width: 100%;
    max-width: 400px;
    padding: 20px;
    background-color: white;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .btn-block {
    width: 100%;
  }
  </style>
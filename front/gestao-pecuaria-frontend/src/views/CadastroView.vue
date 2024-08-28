<template>
  <div class="vh-100 vw-100 cadastro-container">
    <div sm="7" class="cadastro-form">
      <h2 class="text-center mb-5 title-cadastro">Faça o cadastro</h2>
      <div v-if="errorMessage" class="alert alert-danger alert-custom mt-3">{{ errorMessage }}</div>
      
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-user"></i></span>
            <input v-model="nome" type="text" class="form-control" id="nome" placeholder="Nome*" >
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-id-card"></i></span>
            <input v-model="cpf" type="text" class="form-control" id="cpf" placeholder="CPF*" title="Insira um CPF válido">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="telefone1" type="tel" class="form-control" id="telefone1" placeholder="Telefone 1*">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="telefone2" type="tel" class="form-control" id="telefone2" placeholder="Telefone 2">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
            <input v-model="email" type="email" class="form-control" id="email" placeholder="Email*" >
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input v-model="senha" type="password" class="form-control" id="senha" placeholder="Senha*" >
          </div>
        </div>

        <button type="button" class="btn btn-primary btn-block" @click="cadastrar">
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
export default {
  data() {
    return {
      nome: '',
      cpf: '',
      telefone1: '',
      telefone2: '',
      email: '',
      senha: '',
      errorMessage: '',
    };
  },
  methods: {
    async cadastrar() {
      this.errorMessage = ''; // Limpa a mensagem de erro antes da validação

      // Validação simples dos campos
      if (!this.nome || !this.cpf || !this.telefone1 || !this.email || !this.senha) {
        this.errorMessage = 'Por favor, preencha todos os campos obrigatórios.';
        return; // Não prossegue se houver campos obrigatórios não preenchidos
      }

      // if (!/\d{3}\.\d{3}\.\d{3}-\d{2}/.test(this.cpf)) {
      //   this.errorMessage = 'CPF inválido.';
      //   return;
      // }
      // if (!/\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})/.test(this.telefone1)) {
      //   this.errorMessage = 'Telefone 1 inválido.';
      //   return;
      // }
      // if (this.telefone2 && !/\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})/.test(this.telefone2)) {
      //   this.errorMessage = 'Telefone 2 inválido.';
      //   return;
      // }
      // if (!/.+@.+\..+/.test(this.email)) {
      //   this.errorMessage = 'Email inválido.';
      //   return;
      // }

      const dadosProdutor = {
        nome: this.nome,
        cpf: this.cpf,
        telefone1: this.telefone1,
        telefone2: this.telefone2,
        email: this.email,
        password: this.senha
      };

      try {
        const response = await axios.post('http://127.0.0.1:8000/singup', dadosProdutor);
        if (response.status === 200) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
        } else {
          this.errorMessage = 'Erro ao cadastrar produtor. Tente novamente mais tarde.';
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        this.errorMessage = 'Erro ao enviar requisição. Verifique o console para mais detalhes.';
      }
    },

    resetForm() {
      this.nome = '';
      this.cpf = '';
      this.telefone1 = '';
      this.telefone2 = '';
      this.email = '';
      this.senha = '';
    },

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

<template>
  <div class="vh-100 vw-100 cadastro-container">
    <div sm="7" class="cadastro-form">
      <h2 class="text-center mb-5 title-cadastro">Faça o cadastro</h2>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-user"></i></span>
            <input v-model="nome" type="text" class="form-control" id="nome" placeholder="Nome*" required>
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-id-card"></i></span>
            <input v-model="cpf" type="text" class="form-control" id="cpf" placeholder="CPF*" required pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Insira um CPF válido">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="telefone1" type="tel" class="form-control" id="telefone1" placeholder="Telefone 1*" required pattern="\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-phone"></i></span>
            <input v-model="telefone2" type="tel" class="form-control" id="telefone2" placeholder="Telefone 2" pattern="\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})">
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
            <input v-model="email" type="email" class="form-control" id="email" placeholder="Email*" required>
          </div>
        </div>
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-lock"></i></span>
            <input v-model="senha" type="password" class="form-control" id="senha" placeholder="Senha*" required>
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
      senha: ''
    };
  },
  methods: {
    async cadastrar() {
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
          alert('Erro ao cadastrar produtor. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },

    resetForm() {
      this.nome = '';
      this.cpf = '';
      this.telefone1 = '',
        this.telefone2 = '',
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
  background-image: url('../assets/fundo.jpg');
  background-size: cover;
  background-position: center;
}

.cadastro-form {
  flex: 1;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #c2e0a6;
  border-radius: 5px;
  margin-left: 150px;
  margin-right: 150px;
}

/* .title-cadastro {
  color: #358137;
}

.input-group-text {
  background-color: #358137;
  color: white;
  border: 1px solid #358137;
}

.form-control {
  border: 1px solid #358137;
} */

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
</style>

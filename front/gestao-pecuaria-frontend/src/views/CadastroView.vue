<template>
  <div class="vh-100 vw-100 cadastro-container">
    <div sm="5" class="vh-100 cadastro-image">
      <img src="../assets/cadastro.svg" width="600" height="600">
    </div>
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
    <input v-model="cpf" type="text" class="form-control" id="cpf" placeholder="CPF*" required>
  </div>
</div>
<div class="mb-3">
  <div class="input-group">
    <span class="input-group-text"><i class="fas fa-phone"></i></span>
    <input v-model="telefone1" type="tel" class="form-control" id="telefone1" placeholder="Telefone 1*" required>
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
    <input v-model="email" type="email" class="form-control" id="email" placeholder="Email*" required>
  </div>
</div>
<div class="mb-3">
  <div class="input-group">
    <span class="input-group-text"><i class="fas fa-lock"></i></span>
    <input v-model="senha" type="password" class="form-control" id="senha" placeholder="Senha*" required>
  </div>
</div>


        <b-button type="button" class="btn btn-primary" block @click="cadastrar">
          <i class="fas fa-sign-in-alt"></i> Cadastrar
        </b-button>
        <hr />
        <b-button type="button" class="btn btn-outline-secondary" @click="voltar">
          <i class="fas fa-arrow-left"></i> Voltar
        </b-button>
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
        console.log(response.status)
        if (response.status === 200) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
        } else {
          alert('Erro ao cadastrar produtor. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.log("entrou no catch");
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
}

.cadastro-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f2f2f2;
}

.cadastro-form {
  flex: 1;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-left: 150px;
  margin-right: 150px;
}
</style>

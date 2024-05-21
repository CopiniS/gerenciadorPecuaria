<template>
    <div class="form-container">
      <form id="formProdutor">
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user"></i></span>
              <input type="text" class="form-control" id="nomeProdutor" placeholder="Nome" required>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-id-card"></i></span>
              <input type="text" class="form-control" id="cpfProdutor" placeholder="CPF sem pontos ou traços." maxlength="11" required pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Insira um CPF válido">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-phone"></i></span>
              <input type="text" class="form-control" id="telefone1Produtor" placeholder="Telefone 1" required pattern="\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})">
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-phone"></i></span>
              <input type="text" class="form-control" id="telefone2Produtor" placeholder="Telefone 2" pattern="\(?([0-9]{2})\)?([ .-]?)([0-9]{4,5})?([ .-]?)([0-9]{4})">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-envelope"></i></span>
              <input type="email" class="form-control" id="emailProdutor" aria-describedby="emailHelp" placeholder="Email" required>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-lock"></i></span>
              <input type="password" class="form-control" id="senhaProdutor" placeholder="Senha" required>
            </div>
          </div>
        </div>
        
        <button type="button" class="btn btn-primary" @click="editar">Cadastrar</button>
      </form>
    </div>
  </template>

<script>
// import axios from 'axios';

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
    async editar() {
    //   const dadosProdutor = {
    //     nome: this.nome,
    //     cpf: this.cpf,
    //     telefone1: this.telefone1,
    //     telefone2: this.telefone2,
    //     email: this.email,
    //     password: this.senha
    //   };

    //   try {
    //     colocar a url
    //     if (response.status === 200) {
    //       alert('Cadastro realizado com sucesso!');
    //       this.resetForm();
    //     } else {
    //       alert('Erro ao cadastrar produtor. Tente novamente mais tarde.');
    //     }
    //   } catch (error) {
    //     console.error('Erro ao enviar requisição:', error);
    //     alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
    //   }
    },
}
};
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center; 
  height: 40vh; 
  margin-top: 10px;
  margin-bottom: 10px;
}

#formProdutor {
  width: 100%; 
  max-width: 1600px; 
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
  background-color: white; 
}
</style>
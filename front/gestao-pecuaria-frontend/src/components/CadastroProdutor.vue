<template>
  <div>
    <!-- Formulário de Cadastro -->
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3 d-flex align-items-center">
              <label for="nomeProdutor" class="form-label me-2">Nome:</label>
              <input v-model="nomeProdutor" type="text" class="form-control" id="nomeProdutor" placeholder="Nome" required>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3 d-flex align-items-center">
              <label for="cpfProdutor" class="form-label me-2">CPF:</label>
              <input v-model="cpfProdutor" type="text" class="form-control" id="cpfProdutor" placeholder="CPF sem pontos ou traços." maxlength="11" required>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3 d-flex align-items-center">
              <label for="emailProdutor" class="form-label me-2">Email:</label>
              <input v-model="emailProdutor" type="email" class="form-control" id="emailProdutor" aria-describedby="emailHelp" placeholder="Email" required>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3 d-flex align-items-center">
              <label for="senhaProdutor" class="form-label me-2">Senha:</label>
              <input v-model="senhaProdutor" type="password" class="form-control" id="senhaProdutor" placeholder="Senha" :required="!editandoProdutor">
            </div>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">{{ editandoProdutor ? 'Salvar Alterações' : 'Cadastrar' }}</button>
      </form>
    </div>
    
    <!-- Tabela de Listagem -->
    <div>
      <h2>Lista de Produtores</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">CPF</th>
            <th scope="col">Email</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(produtor, index) in produtores" :key="index">
            <td>{{ produtor.nome }}</td>
            <td>{{ produtor.cpf }}</td>
            <td>{{ produtor.email }}</td>
            <td>
              <button @click="editarProdutor(produtor)" class="btn btn-primary btn-sm"><i class="fas fa-edit"></i></button>
              <button @click="apagarProdutor(produtor.id)" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CadastroListagemProdutor',
  data() {
    return {
      editandoProdutor: false,
      produtorEditadoId: null,
      nomeProdutor: '',
      cpfProdutor: '',
      emailProdutor: '',
      senhaProdutor: '',
      produtores: []
    };
  },
  mounted() {
    this.buscarProdutoresDaApi();
  },
  methods: {
    async buscarProdutoresDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/produtores/');
        this.produtores = response.data; 
      } catch (error) {
        console.error('Erro ao buscar produtores da API:', error);
      }
    },
    async submitForm() {
      if (this.editandoProdutor) {
        await this.editarForm();
      } else {
        await this.cadastrarForm();
      }
    },
    async cadastrarForm() {
      const dadosProdutor = {
        nome: this.nomeProdutor,
        cpf: this.cpfProdutor,
        email: this.emailProdutor,
        senha: this.senhaProdutor
      };

      try {
        const response = await axios.post('http://127.0.0.1:8000/produtores/', dadosProdutor);

        if (response.status === 201) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
          this.buscarProdutoresDaApi();
        } else {
          alert('Erro ao cadastrar produtor. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async editarForm() {
      const dadosProdutor = {
        nome: this.nomeProdutor,
        cpf: this.cpfProdutor,
        email: this.emailProdutor,
        senha: this.senhaProdutor
      };

      try {
        const response = await axios.put(`http://127.0.0.1:8000/produtores/${this.produtorEditadoId}/`, dadosProdutor);

        if (response.status === 200) {
          alert('Alterações salvas com sucesso!');
          this.resetForm();
          this.buscarProdutoresDaApi();
        } else {
          alert('Erro ao salvar alterações. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    resetForm() {
      this.editandoProdutor = false;
      this.produtorEditadoId = null;
      this.nomeProdutor = '';
      this.cpfProdutor = '';
      this.emailProdutor = '';
      this.senhaProdutor = '';
    },
    editarProdutor(produtor) {
      this.editandoProdutor = true;
      this.produtorEditadoId = produtor.id;
      this.nomeProdutor = produtor.nome;
      this.cpfProdutor = produtor.cpf;
      this.emailProdutor = produtor.email;
      this.senhaProdutor = ''; // Não exibe a senha no formulário de edição
    },
    async apagarProdutor(id) {
      if (confirm("Tem certeza que deseja apagar este produtor?")) {
        try {
          const response = await axios.delete(`http://127.0.0.1:8000/produtores/${id}`);
          console.log(id);

          if (response.status === 204) {
            alert('Produtor apagado com sucesso!');
            this.buscarProdutoresDaApi();
          } else {
            alert('Erro ao apagar produtor. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    }
  }
};
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center; 
  height: 30vh; 
  margin-top: 0px;
  margin-bottom: 10px;
}

#formProdutor {
  width: 100%; 
  max-width: 1500px; 
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
  background-color: white; 
}
</style>

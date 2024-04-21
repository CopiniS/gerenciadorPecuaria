<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar</button>
    </div>
    <h2>Lista de Raças</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(raca, index) in racas" :key="index">
            <td>{{ raca.nome }}</td>
            <td>
              <button @click="editarRaca(raca)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro-->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Raça</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="nome" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nome">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Raça</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitFormEdicao">
              <div class="mb-3">
                <label for="nomeEditar" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitFormEdicao">Salvar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir esta raça?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarRaca(raca)">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ListarRaca',
  data() {
    return {
      racas: [],
      formData: {
        id: null,
        nome: ''
      }
    }
  },
  mounted() {
    this.buscarRacasDaApi();
  },
  methods: {
    async buscarRacasDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/racas/');
        this.racas = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },
    editarRaca(raca) {
      this.formData = {
        id: raca.id,
        nome: raca.nome
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: ''
      };
    },
    async apagarRaca(raca) {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/racas/${raca.id}/`);
        if (response.status === 204) {
          alert('Raça apagada com sucesso!');
          this.buscarRacasDaApi();
        } else {
          alert('Erro ao apagar raça. Tente novamente mais tarde.');
        }

      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },

    async submitFormEdicao() {
      try {
        const response = await axios.put(`http://127.0.0.1:8000/racas/${this.formData.id}/`, this.formData);

        if (response.status === 200) {
          alert('Alterações salvas com sucesso!');
          this.buscarRacasDaApi();
        } else {
          alert('Erro ao salvar alterações. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async submitForm() {
      try {
        const response = await axios.post(`http://127.0.0.1:8000/racas/`, this.formData);

        if (response.status === 201) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
          this.buscarRacasDaApi();
        } else {
          alert('Erro ao cadastrar raça. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    }
  }
};
</script>

<style>
.table-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>

<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar</button>
    </div>
    <h2>Lista de Cidades</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Estado</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cidade, index) in cidades" :key="index">
            <td>{{ cidade.nome }}</td>
            <td>{{ cidade.estado }}</td>
            <td>
              <button @click="editarCidade(cidade)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
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
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Cidade</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="nome" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nome">
              </div>
              <div class="mb-3">
                <label for="estado" class="col-form-label">Estado:</label>
                <select class="form-select" id="estado" required>
                  <option value="" disabled selected>Selecione o estado</option>
                  <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
                </select>
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
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Cidade</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitFormEdicao">
              <div class="mb-3">
                <label for="nomeEditar" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar">
              </div>
              <div class="mb-3">
                <label for="estadoEditar" class="col-form-label">Estado:</label>
                <select v-model="formData.estado" class="form-select" id="estadoEditar" required>
                  <option selected>{{ formData.estado }}</option>
                  <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
                </select>
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
            Tem certeza de que deseja excluir esta cidade?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarCidade(cidade)">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'ListarCidade',
  data() {
    return {
      cidades: [],
      estados: [
        { "id": 1, "nome": "Acre" },
        { "id": 2, "nome": "Alagoas" },
        { "id": 3, "nome": "Amapá" },
        { "id": 4, "nome": "Amazonas" },
        { "id": 5, "nome": "Bahia" },
        { "id": 6, "nome": "Ceará" },
        { "id": 7, "nome": "Distrito Federal" },
        { "id": 8, "nome": "Espírito Santo" },
        { "id": 9, "nome": "Goiás" },
        { "id": 10, "nome": "Maranhão" },
        { "id": 11, "nome": "Mato Grosso" },
        { "id": 12, "nome": "Mato Grosso do Sul" },
        { "id": 13, "nome": "Minas Gerais" },
        { "id": 14, "nome": "Pará" },
        { "id": 15, "nome": "Paraíba" },
        { "id": 16, "nome": "Paraná" },
        { "id": 17, "nome": "Pernambuco" },
        { "id": 18, "nome": "Piauí" },
        { "id": 19, "nome": "Rio de Janeiro" },
        { "id": 20, "nome": "Rio Grande do Norte" },
        { "id": 21, "nome": "Rio Grande do Sul" },
        { "id": 22, "nome": "Rondônia" },
        { "id": 23, "nome": "Roraima" },
        { "id": 24, "nome": "Santa Catarina" },
        { "id": 25, "nome": "São Paulo" },
        { "id": 26, "nome": "Sergipe" },
        { "id": 27, "nome": "Tocantins" }
      ],
      formData: {
        id: null,
        nome: '',
        estado: ''
      }
    }
  },
  mounted() {
    this.buscarCidadesDaApi();
  },
  methods: {
    async buscarCidadesDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/cidades/');
        this.cidades = response.data;
      } catch (error) {
        console.error('Erro ao buscar cidades da API:', error);
      }
    },
    editarCidade(cidade) {
      this.formData = {
        id: cidade.id,
        nome: cidade.nome,
        estado: cidade.estado
      };
    },
    resetForm() {
      this.formData = {
        id: '',
        nome: '',
        estado: ''
      };
    },
    async apagarCidade(cidade) {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/cidades/${cidade.id}/`);
        if (response.status === 204) {
          alert('Cidade apagada com sucesso!');
          this.buscarCidadesDaApi();
        } else {
          alert('Erro ao apagar cidade. Tente novamente mais tarde.');
        }

      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },

    async submitFormEdicao() {
      try {
        const response = await axios.put(`http://127.0.0.1:8000/cidades/${this.formData.id}/`, this.formData);

        if (response.status === 200) {
          alert('Alterações salvas com sucesso!');
          this.buscarCidadesDaApi();
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
        const response = await axios.post(`http://127.0.0.1:8000/cidades/`, this.formData);

        if (response.status === 201) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
          this.buscarCidadesDaApi();
        } else {
          alert('Erro ao cadastrar cidade. Tente novamente mais tarde.');
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

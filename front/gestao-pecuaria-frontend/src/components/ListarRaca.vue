<template>
  <div class="background">
    <h2>Raças</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Nome</label>
          <input type="text" class="form-control" id="nome" v-model="filtro.nome">
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button class="btn btn-success" @click="aplicarFiltro">Filtrar</button>
        </div>
      </form>
    </div>

    <div>
      <div class="table-container">
        <div class="button-container">
          <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal"
            data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Raca</button>
        </div>
        <table class="table table-bordered">
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
                <button @click="editarRaca(raca)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                <button @click="editarRaca(raca)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
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
              <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastrar Raça</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tag"></i></span>
                  <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
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
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tag"></i></span>
                  <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome" required>
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
      <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
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
              <button type="button" class="btn btn-danger" @click="apagarRaca()">Excluir</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  name: 'ListarRaca',
  data() {
    return {
      racas: [],
      formData: {
        id: null,
        nome: ''
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
      }
    }
  },
  mounted() {
    this.buscarRacasDaApi();
  },
  methods: {
    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/');
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
    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },
    async apagarRaca() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/racas/${this.formData.id}/`);
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
      this.fecharModal("confirmacaoExclusaoModal");
    },
    async submitFormEdicao() {
      try {
        const response = await api.patch(`http://127.0.0.1:8000/racas/${this.formData.id}/`, this.formData);
        if (response.status === 200) {
          alert('Alterações salvas com sucesso!');
          this.buscarRacasDaApi();
          this.fecharModal("edicaoModal");
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
        const response = await api.post(`http://127.0.0.1:8000/racas/`, this.formData);
        if (response.status === 201) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
          this.buscarRacasDaApi();
          this.fecharModal("cadastroModal");
        } else {
          alert('Erro ao cadastrar raça. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    aplicarFiltro() {
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
      this.filtro = {
        nome: '',
      };
    },
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color:  #ededef; /* Um tom mais escuro que o branco */
  min-height: 100vh; /* Garante que o fundo cubra toda a altura da tela */
  padding: 20px;
}

.table-container {
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.button-container {
  text-align: left;
  margin-bottom: 20px;
}

.table-container table tbody tr td {
  background-color: #ededef !important; /* Cor de fundo das células da tabela */
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  background-color: #f0f0f0;
  /* Adiciona uma borda verde na parte inferior */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 5px
}

.btn-acoes i {
  color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px; 
}
</style>

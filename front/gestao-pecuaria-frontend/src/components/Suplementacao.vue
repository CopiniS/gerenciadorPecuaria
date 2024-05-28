<template>
<div>
    <h2>Suplementações</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <!-- Outros filtros existentes -->
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Produto</label>
          <input type="text" class="form-control" id="produto" v-model="filtro.produto">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="piquete" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control" id="piquete" v-model="filtro.piquete">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="quantidade" class="form-label me-2">Quantidade</label>
          <input type="number" class="form-control" id="quantidade" v-model="filtro.quantidade">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataInicial" class="form-label me-2">Data Inicial</label>
          <input type="date" class="form-control" id="dataInicial" v-model="filtro.dataInicial">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataFinal" class="form-label me-2">Data Final</label>
          <input type="date" class="form-control" id="dataFinal" v-model="filtro.dataFinal">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="status" class="form-label me-2">Status</label>
          <select class="form-select" id="status" v-model="filtro.status">
            <option value="">Todos</option>
            <option value="Em andamento">Em andamento</option>
            <option value="Finalizado">Finalizado</option>
          </select>
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
          data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Adicionar Suplemento</button>
      </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Produto</th>
            <th scope="col">Piquete</th>
            <th scope="col">Quantidade</th>
            <th scope="col">Data Inicial</th>
            <th scope="col">Data Final</th>
            <th scope="col">Status</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(suplemento, index) in suplementos" :key="index">
            <td>{{ suplemento.produto }}</td>
            <td>{{ suplemento.piquete }}</td>
            <td>{{ suplemento.quantidade }}</td>
            <td>{{ suplemento.dataInicial }}</td>
            <td>{{ suplemento.dataFinal || '-' }}</td>
            <td :class="{ 'status-andamento': !suplemento.dataFinal, 'status-finalizada': suplemento.dataFinal }">{{
          suplemento.dataFinal ? 'Finalizada' : 'Em Andamento' }}</td>
            <td>
              <button v-if="!suplemento.dataFinal" @click="finalizarSuplemento(suplemento)" class="btn-acoes btn-sm"
                data-bs-toggle="modal" data-bs-target="#finalizarModal" data-bs-whatever="@mdo">
                <i class="fas fa-check"></i>
              </button>
              <button @click="editarSuplemento(suplemento)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(suplemento)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Suplemento -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Suplemento</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                <input v-model="formData.quantidade" type="number" class="form-control" id="quantidade"
                  placeholder="Quantidade" required>
              </div>
              <div class="mb-3 input-group">
                <input v-model="nomeProduto" @input="filtrarProdutos" type="text" class="form-control"
                  placeholder="Digite o nome do produto...">
              </div>
              <div class="list-group" v-if="nomeProduto && filteredProdutos.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="produto in filteredProdutos"
                  :key="produto.id" @click="selecionarProduto(produto)">
                  {{ produto.nome }}
                </button>
              </div>

              <div class="mb-3 input-group">
                <input v-model="piquete" @input="filtrarPiquetes" type="text" class="form-control"
                  placeholder="Digite o número do piquete...">
              </div>
              <div class="list-group" v-if="piquete && filteredPiquetes.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetes"
                  :key="piquete.id" @click="selecionarPiquete(piquete)">
                  {{ piquete.nome }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <label for="dataInicial" class="input-group-text"><i class="fas fa-calendar-alt"></i> Data
                  Inicial</label>
                <input v-model="formData.dataInicial" type="date" class="form-control" id="dataInicial" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button @click="submitForm" class="btn btn-primary">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição de Suplemento -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Suplemento</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                <input v-model="formData.quantidade" type="number" class="form-control" id="quantidadeEditar"
                  placeholder="Quantidade" required>
              </div>
              <div class="mb-3 input-group">
                <input v-model="nomeProduto" @input="filtrarProdutos" type="text" class="form-control"
                  placeholder="Digite o nome do produto...">
              </div>
              <div class="list-group" v-if="nomeProduto && filteredProdutos.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="produto in filteredProdutos"
                  :key="produto.id" @click="selecionarProduto(produto)">
                  {{ produto.nome }}
                </button>
              </div>

              <div class="mb-3 input-group">
                <input v-model="piquete" @input="filtrarPiquetes" type="text" class="form-control"
                  placeholder="Digite o número do piquete...">
              </div>
              <div class="list-group" v-if="piquete && filteredPiquetes.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetes"
                  :key="piquete.id" @click="selecionarPiquete(piquete)">
                  {{ piquete.nome }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.dataInicial" type="date" class="form-control" id="dataInicialEditar" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Salvar</button>
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
            Tem certeza de que deseja excluir este suplemento?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarSuplemento()">Excluir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Finalização de Suplemento -->
    <div class="modal fade" id="finalizarModal" tabindex="-1" aria-labelledby="finalizarModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="finalizarModalLabel">Finalizar Suplemento</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="finalizarSuplementoSubmit">
              <div class="mb-3 input-group">
                <label for="dataFinal" class="input-group-text"><i class="fas fa-calendar-alt"></i> Data Final</label>
                <input v-model="formData.dataFinal" type="date" class="form-control" id="dataFinal" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary" @click="finalizarSuplementoSubmit()">Finalizar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaSuplementos',
  data() {
    return {
      suplementos: [],
      produtos: [],
      piquetes: [],
      filteredProdutos: [],
      filteredPiquetes: [],
      nomeProduto: '',
      piquete: '',
      formData: {
        id: null,
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
      },
      mostrarFormulario: false,
      filtro: {
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
        status: ''
      },
      modalTitle: 'Cadastro de Suplemento',
    }
  },
  mounted() {
    this.buscarSuplementosDaApi();
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
  },
  methods: {
    async buscarSuplementosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/suplementacoes/');
        this.suplementos = response.data;
      } catch (error) {
        console.error('Erro ao buscar suplementos da API:', error);
      }
    },
    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },
    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },
    filtrarProdutos(entrada) {
      if (!entrada) {
        this.filteredProdutos = this.produtos;
        return;
      }
      this.filteredProdutos = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },
    filtrarPiquetes(entrada) {
      if (!entrada) {
        this.filteredPiquetes = this.piquetes;
        return;
      }
      this.filteredPiquetes = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piquete));
    },
    selecionarProduto(produto) {
      this.formData.produto = produto.id;
      this.nomeProduto = produto.nome;
      this.filteredProdutos = [];
    },

    selecionarPiquete(piquete) {
      this.formData.piquete = piquete.id;
      this.piquete = piquete.nome;
      this.filteredPiquetes = [];
    },

    editarSuplemento(suplemento) {
      this.modalTitle = 'Editar Suplemento';
      this.formData = {
        id: suplemento.id,
        quantidade: suplemento.quantidade,
        dataInicial: suplemento.dataInicial,
        dataFinal: suplemento.dataFinal,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
      };
      this.modalTitle = 'Cadastro de Suplemento';
    },
    confirmarExclusao(suplemento) {
      this.formData = {
        id: suplemento.id,
        quantidade: suplemento.quantidade,
        dataInicial: suplemento.dataInicial,
        dataFinal: suplemento.dataFinal,
      };
    },
    async apagarSuplemento() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Suplemento apagado com sucesso!');
          this.buscarSuplementosDaApi();
        } else {
          alert('Erro ao apagar suplemento. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("edicaoModal");
    },
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Suplemento') {
        try {
          const response = await api.post('http://127.0.0.1:8000/suplementacoes/', this.formData);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarSuplementosDaApi();
          } else {
            alert('Erro ao cadastrar suplemento. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("cadastroModal");
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`, this.formData);

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarSuplementosDaApi();
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("edicaoModal");
      }
    },
    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    finalizarSuplemento(suplemento) {
      this.formData = {
        id: suplemento.id,
        quantidade: suplemento.quantidade,
        produto: suplemento.produto,
        piquete: suplemento.piquete,
        dataInicial: suplemento.dataInicial,
        dataFinal: suplemento.dataFinal,
      };
    },

    async finalizarSuplementoSubmit(){
        try {
          const response = await api.patch(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`, this.formData);

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarSuplementosDaApi();
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("edicaoModal");      
    },

    aplicarFiltro() {
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
      this.filtro = {
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
        status: ''
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

.table-container table thead tr th {
  border-bottom: 2px solid #4CAF50;
  /* Adiciona uma borda verde na parte inferior */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  margin: 5px
}

.btn-acoes i {
  color: #4CAF50;
}

.button-group {
  display: flex;
  gap: 10px;
}

.status-andamento {
  color: #ff9800;
  /* Laranja */
}

.status-finalizada {
  color: #4caf50;
  /* Verde */
}
</style>

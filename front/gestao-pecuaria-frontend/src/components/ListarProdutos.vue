<template>
  <div class="background">
    <h2>Produtos</h2>
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
          <div class="col-auto d-flex align-items-center">
              <label for="tipo" class="form-label me-2">Tipo</label>
              <select class="form-select" id="tipo" v-model="filtro.tipo">
                  <option value="">Selecione o tipo</option>
                  <option value="alimenticio">Alimentício</option>
                  <option value="sanitario">Sanitário</option>
              </select>
          </div>
          <div class="col-auto d-flex align-items-center">
              <label for="categoria" class="form-label me-2">Categoria</label>
              <input type="text" class="form-control" id="categoria" v-model="filtro.categoria">
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
          data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Produto</button>
      </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Nome</th>
              <th scope="col">Tipo</th>
              <th scope="col">Categoria</th>
              <th scope="col">Estoque</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(produto, index) in produtos" :key="index">
              <td>{{ produto.nome }}</td>
              <td>{{ produto.tipo }}</td>
              <td>{{ produto.categoria }}</td>
              <td>{{ achaEstoque(produto.id) }}</td>
              <td>
                <button @click="editarProduto(produto)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                <button @click="confirmarExclusao(produto)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                    class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal de Cadastro de Produto -->
      <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Produto</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                    placeholder="Selecione o tipo" required>
                    <option disabled value="">Tipo</option>
                    <option value="sanitario">Sanitário</option>
                    <option value="alimenticio">Alimentício</option>
                </select>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                  <input v-model="formData.categoria" type="text" class="form-control" id="categoria" placeholder="Categoria" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                  <textarea v-model="formData.descricao" class="form-control" id="descricao"
                    placeholder="Descrição"></textarea>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                  <input type="text" class="form-control" id="estoque" placeholder="Estoque" required>
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

      <!-- Modal de Edição de Produto -->
      <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Produto</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.tipo" class="form-select" id="tipoEditar" aria-label="Tipo"
                    placeholder="Selecione o tipo" required>
                    <option value="sanitario">Sanitário</option>
                    <option value="alimenticio">Alimentício</option>
                </select>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                  <input v-model="formData.categoria" type="text" class="form-control" id="categoriaEditar" placeholder="Categoria" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                  <textarea v-model="formData.descricao" class="form-control" id="descricaoEditar"
                    placeholder="Descrição"></textarea>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                  <input type="text" class="form-control" id="estoqueEditar" placeholder="Estoque" required>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-primary" @click="submitForm">Salvar</button>
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
            Tem certeza de que deseja excluir este produto?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarProduto()">Excluir</button>
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
  name: 'TelaProdutos',
  data() {
    return {
      produtos: [],
      estoque: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
        tipo: '',
        categoria: ''
      },
      modalTitle: 'Cadastro de Produto',
    }
  },
  mounted() {
    this.buscarProdutosDaApi();
    this.buscarEstoqueDaApi();
  },
  methods: {
    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/' , {
          // Parâmetros da requisição (se houver)
        });
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    async buscarEstoqueDaApi(){
      try {
        const response = await api.get('http://127.0.0.1:8000/estoque/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.estoque = response.data;
      } catch (error) {
        console.error('Erro ao buscar estoque da API:', error);
      }
    },

    editarProduto(produto) {
      this.modalTitle = 'Editar Produto';
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        categoria: produto.categoria,
        descricao:produto.descricao,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
      };
      this.modalTitle = 'Cadastro de Produto';
    },
    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    achaEstoque(produtoId){
      let quantidade;
      this.estoque.forEach(e => {
        if(e.produto === produtoId){
          quantidade = e.quantidade;
        }
      });
      if(!quantidade){
        quantidade = 0;
      }
      return quantidade;
    },

    confirmarExclusao(produto) {
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        categoria: produto.categoria,
        descricao:produto.descricao,
      };
    },
    async apagarProduto() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/produtos/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Produto apagado com sucesso!');
          this.buscarProdutosDaApi();
        } else {
          alert('Erro ao apagar produto. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    async submitForm() {
      if (this.modalTitle === 'Cadastro de Produto') {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarProdutosDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarProdutosDaApi();
            this.fecharModal("edicaoModal");
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },
    aplicarFiltro() {
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
      this.filtro.nome = '';
      this.filtro.tipo = '';
      this.filtro.categoria = '';
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
  background-color: #ededef; /* Um tom mais escuro que o branco */
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
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px; 
}

</style>

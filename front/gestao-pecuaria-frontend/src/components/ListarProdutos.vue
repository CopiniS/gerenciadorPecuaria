<template>
  <div>
    <h2>Lista de Produtos</h2>
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="(produto, index) in produtos" :key="index">
            <td>{{ produto.nome }}</td>
            <td>{{ produto.tipo }}</td>
            <td>{{ produto.categoria }}</td>
            <td>{{ produto.estoque }}</td>
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
                <input v-model="formData.estoque" type="text" class="form-control" id="estoque" placeholder="Estoque" required>
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
                <input v-model="formData.estoque" type="text" class="form-control" id="estoqueEditar" placeholder="Estoque" required>
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
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaProdutos',
  data() {
    return {
      produtos: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: '',
        estoque: '',
      },
      modalTitle: 'Cadastro de Produto',
    }
  },
  mounted() {
    this.buscarProdutosDaApi();
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
    editarProduto(produto) {
      this.modalTitle = 'Editar Produto';
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        categoria: produto.categoria,
        descricao:produto.descricao,
        estoque: produto.estoque,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: '',
        estoque: '',
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
    confirmarExclusao(produto) {
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        categoria: produto.categoria,
        descricao:produto.descricao,
        estoque: produto.estoque,
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

    async verificaEstoqueVazio(){
      if(this.formData.estoque === ''){
        this.formData.estoque = 0;
      }
    },
    
    async submitForm() {
      this.verificaEstoqueVazio();
      if (this.modalTitle === 'Cadastro de Produto') {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarProdutosDaApi();
          } else {
            alert('Erro ao cadastrar produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("cadastroModal");
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarProdutosDaApi();
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("edicaoModal");
      }
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.table-container {
  margin-left: 20px;
  margin-right: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.button-container {
  text-align: left; 
  margin-bottom: 20px; 
}

.table-container table thead tr th {
  border-bottom: 2px solid #4CAF50; /* Adiciona uma borda verde na parte inferior */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #4CAF50;
}

.button-group {
  display: flex;
  gap: 10px; 
}

</style>

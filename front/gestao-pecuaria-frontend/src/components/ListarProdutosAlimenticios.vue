<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Produto Alimentício</button>
    </div>
    <h2>Lista de Produtos Alimentícios</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(produto, index) in produtos" :key="index">
            <td>{{ produto.nome }}</td>
            <td>{{ produto.tipo }}</td>
            <td>
              <button @click="editarProduto(produto)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(produto)" class="btn btn-danger btn-sm" data-bs-toggle="modal"
                data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Produto Alimentício -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Produto Alimentício</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <input v-model="formData.tipo" type="text" class="form-control" id="tipo" placeholder="Tipo" required>
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

    <!-- Modal de Edição de Produto Alimentício -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Produto Alimentício</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome"
                  required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <input v-model="formData.tipo" type="text" class="form-control" id="tipoEditar" placeholder="Tipo"
                  required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar</button>
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
            Tem certeza de que deseja excluir este produto Alimentício?
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
  name: 'TelaProdutosAlimenticios',
  data() {
    return {
      produtos: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
      },
      modalTitle: 'Cadastro de Produto Alimenticio',
    }
  },
  mounted() {
    this.buscarProdutosAlimenticiosDaApi();
  },
  methods: {
    async buscarProdutosAlimenticiosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos-alimenticios/');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos Alimentícios da API:', error);
      }
    },
    editarProduto(produto) {
      this.modalTitle = 'Editar Produto Alimenticio';
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipo: '',
      };
      this.modalTitle = 'Cadastro de Produto Alimenticio';
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
      };
    },
    async apagarProduto() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/produtos-alimenticios/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Produto Alimenticio apagado com sucesso!');
          this.buscarProdutosAlimenticiosDaApi();
        } else {
          alert('Erro ao apagar produto Alimenticio. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("cadastroModal");
    },
    

    async submitForm() {
      if (this.modalTitle === 'Cadastro de Produto Alimenticio') {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos-alimenticios/', this.formData);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarProdutosAlimenticiosDaApi();
          } else {
            alert('Erro ao cadastrar produto sanitário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("cadastroModal");
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/produtos-alimenticios/${this.formData.id}/`, this.formData);

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarProdutosAlimenticiosDaApi();
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
}
</style>

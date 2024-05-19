<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Produto Sanitário</button>
    </div>
    <h2>Lista de Produtos Sanitários</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col">Vencimento</th>
            <th scope="col">Lote</th>
            
          </tr>
        </thead>
        <tbody>
          <tr v-for="(produto, index) in produtos" :key="index">
            <td>{{ produto.nome }}</td>
            <td>{{ produto.tipo }}</td>
            <td>{{ produto.vencimento }}</td>
            <td>{{ produto.lote }}</td>
            <td>
              <button @click="editarProduto(produto)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(produto)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Produto Sanitário -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Produto Sanitário</h1>
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
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.vencimento" type="date" class="form-control" id="vencimento" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-layer-group"></i></span>
                <input v-model="formData.lote" type="text" class="form-control" id="lote" placeholder="Lote" required>
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

    <!-- Modal de Edição de Produto Sanitário -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Produto Sanitário</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <input v-model="formData.tipo" type="text" class="form-control" id="tipoEditar" placeholder="Tipo" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.vencimento" type="date" class="form-control" id="vencimentoEditar" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-layer-group"></i></span>
                <input v-model="formData.lote" type="text" class="form-control" id="loteEditar" placeholder="Lote" required>
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
            Tem certeza de que deseja excluir este produto sanitário?
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
  name: 'TelaProdutosSanitarios',
  data() {
    return {
      produtos: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
        vencimento: '',
        lote: '',
      },
      modalTitle: 'Cadastro de Produto Sanitário',
    }
  },
  mounted() {
    this.buscarProdutosSanitariosDaApi();
  },
  methods: {
    async buscarProdutosSanitariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos-sanitarios/' , {
          // Parâmetros da requisição (se houver)
        });
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos sanitários da API:', error);
      }
    },
    editarProduto(produto) {
      this.modalTitle = 'Editar Produto Sanitário';
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        vencimento: produto.vencimento,
        lote: produto.lote,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipo: '',
        vencimento: '',
        lote: '',
      };
      this.modalTitle = 'Cadastro de Produto Sanitário';
    },
    confirmarExclusao(produto) {
      this.formData = {
        id: produto.id,
        nome: produto.nome,
        tipo: produto.tipo,
        vencimento: produto.vencimento,
        lote: produto.lote,
      };
    },
    async apagarProduto() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/produtos-sanitarios/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Produto sanitário apagado com sucesso!');
          this.buscarProdutosSanitariosDaApi();
        } else {
          alert('Erro ao apagar produto sanitário. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
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
    
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Produto Sanitário') {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos-sanitarios/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarProdutosSanitariosDaApi();
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
          const response = await api.patch(`http://127.0.0.1:8000/produtos-sanitarios/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarProdutosSanitariosDaApi();
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

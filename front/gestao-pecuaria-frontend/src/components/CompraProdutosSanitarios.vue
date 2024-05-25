<template>
  <div>
    <h2>Compra de Produtos Sanitários</h2>
    <div class="table-container">
    <div class="button-container">
      <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Compra Produto Sanitário</button>
    </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Valor Unitário</th>
            <th scope="col">Quantidade Comprada</th>
            <th scope="col">Validade</th>
            <th scope="col">Lote</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(compra, index) in compras" :key="index">
            <td>{{ compra.valorUnitario }}</td>
            <td>{{ compra.quantidadeComprada }}</td>
            <td>{{ compra.validade }}</td>
            <td>{{ compra.lote }}</td>
            <td>
              <button @click="editarCompra(compra)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(compra)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Compra de Produto Sanitário -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Compra de Produto Sanitário</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                <input v-model="formData.valorUnitario" type="number" class="form-control" id="valorUnitario" placeholder="Valor Unitário" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-boxes"></i></span>
                <input v-model="formData.quantidadeComprada" type="number" class="form-control" id="quantidadeComprada" placeholder="Quantidade Comprada" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.validade" type="date" class="form-control" id="validade" required>
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

    <!-- Modal de Edição de Compra de Produto Sanitário -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Compra de Produto Sanitário</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                <input v-model="formData.valorUnitario" type="number" class="form-control" id="valorUnitarioEditar" placeholder="Valor Unitário" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-boxes"></i></span>
                <input v-model="formData.quantidadeComprada" type="number" class="form-control" id="quantidadeCompradaEditar" placeholder="Quantidade Comprada" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.validade" type="date" class="form-control" id="validadeEditar" required>
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
            Tem certeza de que deseja excluir esta compra de produto sanitário?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarCompra()">Excluir</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaComprasSanitarios',
  data() {
    return {
      compras: [],
      formData: {
        id: null,
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
      },
      modalTitle: 'Cadastro de Compra de Produto Sanitário',
    }
  },
  mounted() {
    this.buscarComprasSanitariosDaApi();
  },
  methods: {
    async buscarComprasSanitariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/compras-sanitarios/');
        this.compras = response.data;
      } catch (error) {
        console.error('Erro ao buscar compras de produtos sanitários da API:', error);
      }
    },
    editarCompra(compra) {
      this.modalTitle = 'Editar Compra de Produto Sanitário';
      this.formData = {
        id: compra.id,
        valorUnitario: compra.valorUnitario,
        quantidadeComprada: compra.quantidadeComprada,
        validade: compra.validade,
        lote: compra.lote,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
      };
      this.modalTitle = 'Cadastro de Compra de Produto Sanitário';
    },
    confirmarExclusao(compra) {
      this.formData = {
        id: compra.id,
        valorUnitario: compra.valorUnitario,
        quantidadeComprada: compra.quantidadeComprada,
        validade: compra.validade,
        lote: compra.lote,
      };
    },
    async apagarCompra() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/compras-sanitarios/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Compra de produto sanitário apagada com sucesso!');
          this.buscarComprasSanitariosDaApi();
        } else {
          alert('Erro ao apagar compra de produto sanitário. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("edicaoModal");
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
      if (this.modalTitle === 'Cadastro de Compra de Produto Sanitário') {
        try {
          const response = await api.post('http://127.0.0.1:8000/compras-sanitarios/', this.formData);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarComprasSanitariosDaApi();
          } else {
            alert('Erro ao cadastrar compra de produto sanitário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/compras-sanitarios/${this.formData.id}/`, this.formData);

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarComprasSanitariosDaApi();
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
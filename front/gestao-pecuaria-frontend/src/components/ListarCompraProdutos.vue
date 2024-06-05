<template>
    <div>
    <h2>Compras</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataCompra" class="form-label me-2">Data da Compra</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da compra" 
          class="form-control" id="dataCompra" v-model="filtro.dataCompra">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Produto</label>
          <input type="text" class="form-control" id="produto" v-model="filtro.produto">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="valorUnitario" class="form-label me-2">Valor Unitário</label>
          <input type="number" class="form-control" id="valorUnitario" v-model="filtro.valorUnitario">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="quantidadeComprada" class="form-label me-2">Quantidade Comprada</label>
          <input type="number" class="form-control" id="quantidadeComprada" v-model="filtro.quantidadeComprada">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="validade" class="form-label me-2">Validade</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da compra" 
          class="form-control" id="validade" v-model="filtro.validade">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="lote" class="form-label me-2">Lote</label>
          <input type="text" class="form-control" id="lote" v-model="filtro.lote">
        </div>
        <div class="col-auto">
            <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
            <button class="btn btn-success" @click="aplicarFiltro">Filtrar</button>
        </div>
      </form>
    </div>

    <h2>Histórico de Compras de Produtos</h2>
    <div class="table-container">
    <div class="button-container">
      <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Compra Produto</button>
    </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Data da compra</th>
            <th scope="col">Produto</th>
            <th scope="col">Valor Unitário</th>
            <th scope="col">Quantidade Comprada</th>
            <th scope="col">Validade</th>
            <th scope="col">Lote</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(compra, index) in compras" :key="index">
            <td>{{ compra.dataCompra }}</td>
            <td>{{ compra.produto.nome }}</td>
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

    <!-- Modal de Cadastro de Compra de Produto -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Compras de Produtos</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da compra" 
                class="form-control" id="dataCompraCadastro" v-model="formData.dataCompra" required>
              </div>
              <div class="mb-3 input-group">
                <input v-model="nomeDigitado" @input="filterProdutos" type="text" class="form-control" placeholder="Digite o produto...">
              </div>
              <div class="list-group" v-if="nomeDigitado && produtosFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                  {{ produto.nome }}
                </button>
              </div>
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
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Validade" 
                class="form-control" id="validadeCadastro" v-model="formData.validade" required>
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

    <!-- Modal de Edição de Compra de Produto -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Compra de Produto </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da compra" 
                class="form-control" id="dataCompraEdicao" v-model="formData.dataCompra" required>
              </div>
              <div class="mb-3 input-group">
                <input v-model="nomeDigitado" @input="filterProdutos" type="text" class="form-control" placeholder="Digite o produto...">
              </div>
              <div class="list-group" v-if="nomeDigitado && produtosFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                  {{ produto.nome }}
                </button>
              </div>
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
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Validade" 
                class="form-control" id="validade" v-model="formData.validade" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-layer-group"></i></span>
                <input v-model="formData.lote" type="text" class="form-control" id="lote" placeholder="Lote" required>
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
            Tem certeza de que deseja excluir esta compra de produto?
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
  name: 'TelaComprasProdutos',
  data() {
    return {
      compras: [],
      produtos: [],
      produtosFiltrados: [],
      nomeDigitado: '',
      formData: {
        id: null,
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
      },
      mostrarFormulario: false,
      filtro: {
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: ''
      },
      modalTitle: 'Cadastro de Compra de Produto',
    }
  },
  mounted() {
    this.buscarComprasDaApi();
    this.buscarProdutos();
  },
  methods: {
    async buscarComprasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/compras-produtos/');
        this.compras = response.data;
      } catch (error) {
        console.error('Erro ao buscar compras de produtos da API:', error);
      }
    },

    async buscarProdutos(){
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeDigitado));
    },
    selectProduto(produto) {
      this.nomeDigitado = produto.nome;
      this.formData.produto = produto.id;
      this.produtosFiltrados = [];
    },

    editarCompra(compra) {
      this.modalTitle = 'Editar Compra de Produto';
      this.formData = {
        id: compra.id,
        dataCompra: compra.dataCompra,
        produto: compra.produto.id,
        valorUnitario: compra.valorUnitario,
        quantidadeComprada: compra.quantidadeComprada,
        validade: compra.validade,
        lote: compra.lote,
      };
      this.nomeDigitado = compra.produto.nome;
    },
    resetForm() {
      this.formData = {
        id: null,
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
      };
      this.nomeDigitado = '',
      this.modalTitle = 'Cadastro de Compra de Produto';
    },
    confirmarExclusao(compra) {
      this.formData = {
        id: compra.id,
        dataCompra: compra.dataCompra,
        produto: compra.produto.id,
        valorUnitario: compra.valorUnitario,
        quantidadeComprada: compra.quantidadeComprada,
        validade: compra.validade,
        lote: compra.lote,
      };
    },
    async apagarCompra() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/compras-produtos/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Compra de produto apagada com sucesso!');
          this.buscarComprasDaApi();
        } else {
          alert('Erro ao apagar compra de produto. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
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
      if (this.modalTitle === 'Cadastro de Compra de Produto') {
        try {
          const response = await api.post('http://127.0.0.1:8000/compras-produtos/', this.formData);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarComprasDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar compra de produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          console.log('formdata: ', this.formData)
          const response = await api.patch(`http://127.0.0.1:8000/compras-produtos/${this.formData.id}/`, this.formData);

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarComprasDaApi();
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
      this.filtro.dataCompra ='';
      this.filtro.produto ='';
      this.filtro.valorUnitario ='';
      this.filtro.quantidadeComprada ='';
      this.filtro.validade ='';
      this.filtro.lote ='';
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
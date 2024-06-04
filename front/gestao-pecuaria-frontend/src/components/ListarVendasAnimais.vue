<template>
  <div>
    <h2>Vendas de animais</h2>
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
          data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Venda</button>
      </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data da venda</th>
              <th scope="col">Preco KG</th>
              <th scope="col">Finalidade</th>
              <th scope="col">Animal</th>
              <th scope="col">Peso</th>
              <th scope="col">Valor Total</th>
              <th scope="col">Observação</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(venda, index) in vendas" :key="index">
              <td>{{ venda.dataVenda }}</td>
              <td>{{ venda.animal.brinco }}</td>
              <td>{{ venda.peso }}</td>
              <td>{{ venda.precoKg }}</td>
              <td>{{ venda.valorTotal }}</td>
              <td>{{ venda.finalidade }}</td>
              <td>{{ venda.observacao }}</td>
              <td>
                <button @click="editarVenda(venda)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                <button @click="confirmarExclusao(venda)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                    class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal de Cadastro de Venda -->
      <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Venda</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                    <input v-model="formData.dataVenda" type="date" class="form-control" id="dataVenda"
                    placeholder="Data da Venda" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.precoKg" type="text" class="form-control" id="precoKg" placeholder="Preço por Kg" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.finalidade" class="form-select" id="finalidade" aria-label="Finalidade"
                    placeholder="Selecione o tipo" required>
                    <option disabled value="">Finalidade</option>
                    <option value="Cria">Cria</option>
                    <option value="Recria">Recria</option>
                    <option value="Engorda">Engorda</option>
                    <option value="Abate">Abate</option>
                </select>
                </div>
                <div class="mb-3 input-group">
                    <input v-model="brinco" @input="filterAnimais" type="text" class="form-control" placeholder="Digite o brinco...">
                </div>
                <div class="list-group" v-if="brinco && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                    {{ animal.brinco }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.peso" type="text" class="form-control" id="peso" placeholder="Peso" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.valorTotal" type="text" class="form-control" id="valorTotal" placeholder="Valor Total" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                  <textarea v-model="formData.observacao" class="form-control" id="observacao"
                    placeholder="Observação"></textarea>
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
              <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Venda</h1>
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
  </div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaProdutos',
  data() {
    return {
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      vendas: [],
      camposHabilitados: false,
      formData: {
        id: null,
        animal: '',
        dataVenda: '',
        peso: '',
        precoKg: '',
        valorTotal: '',
        finalidade: '',
        observacao: null,
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
        tipo: '',
        categoria: ''
      },
      modalTitle: 'Cadastro de Venda',
    }
  },
  mounted() {
    this.buscarVendasDaApi();
    this.buscarAnimaisDaApi();
  },
  methods: {
    async buscarVendasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/vendas-animais/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.vendas = response.data;
      } catch (error) {
        console.error('Erro ao buscar vendas da API:', error);
      }
    },

    async buscarAnimaisDaApi() {
        try {
            const response = await api.get('http://127.0.0.1:8000/animais/vivos' , {
            params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
            });
            this.animais = response.data;
        } catch (error) {
            console.error('Erro ao buscar animais da API:', error);
        }
    },

    filterAnimais() {
        this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectAnimal(animal) {
        this.brinco = animal.brinco;
        this.formData.animal = animal.id;
        this.camposHabilitados = true;
        this.animaisFiltrados = [];
    },

    editarVenda(venda) {
      this.modalTitle = 'Editar Venda';
      this.formData = {
        id: venda.id,
        animal: venda.animal,
        dataVenda: venda.dataVenda,
        peso: venda.peso,
        precoKg: venda.precoKg,
        valorTotal: venda.valorTotal,
        finalidade: venda.finalidade,
        observacao: venda.observacao,
      };
    },
    resetForm() {
      const { dataVenda, precoKg, finalidade } = this.formData;
      this.formData = {
        id: null,
        animal: '',
        dataVenda: dataVenda,
        peso: '',
        precoKg: precoKg,
        valorTotal: '',
        finalidade: finalidade,
        observacao: null,
      };
      this.brinco = '',
      this.modalTitle = 'Cadastro de Venda';
    },
    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },
    confirmarExclusao(venda) {
      this.formData = {
        id: venda.id,
        animal: venda.animal,
        dataVenda: venda.dataVenda,
        peso: venda.peso,
        precoKg: venda.precoKg,
        valorTotal: venda.valorTotal,
        finalidade: venda.finalidade,
        observacao: venda.observacao,
      };
    },
    async apagarProduto() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/vendas-animais/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Venda apagada com sucesso!');
          this.buscarVendasDaApi();
          this.buscarAnimaisDaApi();
        } else {
          alert('Erro ao apagar venda. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    async submitForm() {
      if (this.modalTitle === 'Cadastro de Venda') {
        try {
          const response = await api.post('http://127.0.0.1:8000/vendas-animais/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarVendasDaApi();
            this.buscarAnimaisDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar Venda. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/vendas-animais/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.buscarVendasDaApi();
            this.buscarAnimaisDaApi();
            this.resetForm();
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

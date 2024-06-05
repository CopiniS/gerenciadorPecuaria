<template>
<div>
  <h2>Aplicações de Produtos</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Animal</label>
          <input type="text" class="form-control" id="animal" v-model="filtro.animal">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Produto</label>
          <input type="text" class="form-control" id="produto" v-model="filtro.produto">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataCompra" class="form-label me-2">Data</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação" 
          class="form-control" id="dataAplicacao" v-model="filtro.dataAplicacao" required>
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
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Aplicação</button>
    </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Data da aplicação</th>
            <th scope="col">Animal</th>
            <th scope="col">Produto</th>
            <th scope="col">Dosagem</th>
            <th scope="col">Observação</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(aplicacao, index) in aplicacoes" :key="index">
            <td>{{ aplicacao.dataAplicacao }}</td>
            <td>{{ aplicacao.animal.brinco }}</td>
            <td>{{ aplicacao.produto.nome }}</td>
            <td>{{ aplicacao.dosagem }}</td>
            <td>{{ aplicacao.observacao }}</td>
            <td>
              <button @click="editarAplicacao(aplicacao)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="editarAplicacao(aplicacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
        <!-- Modal de Cadastro de Aplicação -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Aplicação</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação" 
                    class="form-control" id="dataAplicacaoCadastro" v-model="formData.dataAplicacao" required>
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
                    <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control" placeholder="Digite o produto...">
                </div>
                <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                    {{ produto.nome }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.dosagem" type="text" class="form-control" id="dosagem" 
                    :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Dosagem" required>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.observacao" type="text" class="form-control" id="observacao" 
                    :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Observação" required>
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

    <!-- Modal de Edição de Aplicação -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Aplicação de Produto</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação" 
                    class="form-control" id="dataAplicacaoEdicao" v-model="formData.dataAplicacao" required>
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
                    <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control" placeholder="Digite o produto...">
                </div>
                <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados" :key="produto.id" @click="selectProduto(produto)">
                    {{ produto.nome }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.dosagem" type="text" class="form-control" id="dosagem" 
                    :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Dosagem" required>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.observacao" type="text" class="form-control" id="observacao" 
                    :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Observação" required>
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
            Tem certeza de que deseja excluir esta aplicação?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarAplicacao()">Excluir</button>
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
  name: 'TelaAplicacoesProdutos',
  data() {
    return {
        animais: [],
        animaisFiltrados: [],
        brinco: '',
        aplicacoes: [],
        produtos: [],
        produtosFiltrados: [],
        nomeProduto: '',  
        camposHabilitadosAnimal: false,
        camposHabilitadosProduto: false,
        formData: {
            id: null,
            produto: '',
            animal: '',
            dosagem: '',
            dataAplicacao: '',
            observacao: null,
      },
      mostrarFormulario: false,
      filtro: {
        produto: '',
        animal: '',
        dataAplicacao: '',
      },
      modalTitle: 'Cadastro de Aplicacao',
    }

  },
  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();
    this.buscarAplicacoesDaApi();
  },
  methods: {
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
        this.camposHabilitadosAnimal = true;
        this.animaisFiltrados = [];
    },
    
    async buscarProdutosDaApi(){
        try {
            const response = await api.get('http://127.0.0.1:8000/produtos/sanitarios' , {});
            this.produtos = response.data;
        } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
        }
    },

    filterProdutos() {
        this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },

    selectProduto(produto) {
        this.nomeProduto = produto.nome;
        this.formData.produto = produto.id;
        this.camposHabilitadosProduto = true;
        this.produtosFiltrados = [];
    },

    async buscarAplicacoesDaApi(){
        try {
            const response = await api.get('http://127.0.0.1:8000/aplicacoes-produtos/' , {
            params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
            });
            this.aplicacoes = response.data;
        } catch (error) {
        console.error('Erro ao buscar aplicações de produtos da API:', error);
        }
    },

    editarAplicacao(aplicacao) {
      this.modalTitle = 'Editar Aplicacao';
      this.formData = {
        id: aplicacao.id,
        animal: aplicacao.animal.id,
        produto: aplicacao.produto.id,
        dataAplicacao: aplicacao.dataAplicacao,
        dosagem: aplicacao.dosagem,
        observacao: aplicacao.observacao,
      };
      this.brinco = aplicacao.animal.brinco;
      this.nomeProduto = aplicacao.produto.nome;
      this.camposHabilitadosAnimal = true;
      this.camposHabilitadosProduto = true;
    },
    resetForm() {
      this.formData = {
        id: null,
        animal: '',
        produto: '',
        dataAplicacao: '',
        dosagem: '',
        observacao: null,
      };
      this.brinco = '';
      this.nomeProduto = '';
      this.modalTitle = 'Cadastro de Aplicacao';
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async apagarAplicacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/aplicacoes-produtos/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Aplicação de produto apagada com sucesso!');
          this.buscarAplicacoesDaApi();
        } else {
          alert('Erro ao apagar aplicação de produto. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },
    
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Aplicacao') {
        try {
          const response = await api.post('http://127.0.0.1:8000/aplicacoes-produtos/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarAplicacoesDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar aplicação de produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          console.log('formDAta: ', this.formData)
          const response = await api.patch(`http://127.0.0.1:8000/aplicacoes-produtos/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarAplicacoesDaApi();
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
      this.filtro = {
        produto: '',
        animal: '',
        dataAplicacao: '',
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
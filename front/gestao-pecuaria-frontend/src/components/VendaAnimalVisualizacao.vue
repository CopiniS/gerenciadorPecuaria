<template>
<div class="background">
  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Visualização</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Vizualização</h2>
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
        <p><strong>Data da Venda:</strong> {{ formatarData(this.dataSelecionada) }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Animal</th>
                  <th scope="col">Peso</th>
                  <th scope="col">Finalidade</th>
                  <th scope="col">Preço do Kg</th>
                  <th scope="col">Valor total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="venda in this.vendasSelecionadas" :key="venda.id">
                  <td>{{ venda.animal.brinco}}</td>
                  <td>{{ venda.peso}}</td>
                  <td>{{ venda.finalidade}}</td>
                  <td>{{ venda.precoKg}}</td>
                  <td>{{ venda.valorTotal}}</td>
                  <td>
                    <button @click="editarVenda(venda)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                    <button @click="confirmarExclusaoVenda(venda)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
                  </td>
                </tr>
              </tbody>
            </table>
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
            Tem certeza de que deseja excluir esta Venda?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarVenda()">Excluir</button>
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
  data() {
    return {
      vendas: [],
      datasVendas: [],
      vendaParaExcluir: null,
      vendasSelecionadas: [],
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
    }
  },
  mounted() {
    const vendasSelecionadasJSON = this.$route.params.vendasSelecionadas;
        if (vendasSelecionadasJSON) {
            this.fetchVendas(vendasSelecionadasJSON);
        }
  },
  methods: {

    async fetchVendas(vendasSelecionadasJSON) {
      try {
        this.vendasSelecionadas = JSON.parse(decodeURIComponent(vendasSelecionadasJSON));
      } catch (error) {
        console.error('Erro ao carregar dados da venda:', error);
      }
    },

    acessarCadastro(){
        this.$router.push({
        name: 'VendaAnimalCadastro', 
      })
    },

    
    formatarData(data) {
        const date = new Date(data);
        const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
        return utcDate.toLocaleDateString('pt-BR', options);
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    confirmarExclusaoVenda(venda) {
      this.vendaParaExcluir = venda;
    },
    
    async apagarVenda() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/vendas-animais/${this.vendaParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Venda excluído com sucesso!');
          this.detalhesVendas = this.detalhesVendas.filter(animal => animal.id !== this.vendaParaExcluir.id);
          this.vendaParaExcluir = null;
          this.buscarVendasDaApi();
        } else {
          alert('Erro ao excluir a venda. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoAnimalModal');
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
  background-color:  #ededef; /* Um tom mais escuro que o branco */
  min-height: 100vh; /* Garante que o fundo cubra toda a altura da tela */
  padding: 20px;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
  /* Cor um pouco mais escura quando a aba está ativa */
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
  border-bottom: 2px solid #176d1a; /* Adiciona uma borda verde na parte inferior */
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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px; 
}

</style>

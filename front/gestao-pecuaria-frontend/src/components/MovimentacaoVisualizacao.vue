<template>
<div class="background">
  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link" :class="{ active: activeTab === 'movimentacoes' }" id="nav-vet-tab" @click="selectTab('movimentacoes')" 
    type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Movimentações</button>
    <button class="nav-link active" :class="{ active: activeTab === 'visualizacao' }" id="nav-vet-tab" data-bs-toggle="tab" 
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
        <p><strong>Data da Movimentação:</strong> {{ formatarData(this.dataSelecionada) }}</p>
        <p><strong>Piquete de Origem:</strong> {{ this.piqueteOrigem }}</p>
        <p><strong>Piquete de Destino:</strong> {{ this.piqueteDestino }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Animal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="movimentacao in this.movimentacoesSelecionadas" :key="movimentacao.id">
                  <td>{{ movimentacao.animal.brinco}}</td>
                  <td>
                    <button @click="acessarEdicao(movimentacao)" class="btn-acoes btn-sm"><i class="fas fa-edit"></i></button>
                    <button @click="confirmarExclusaoMovimentacao(movimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
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
            Tem certeza de que deseja excluir esta Movimentacao?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarMovimentacao()">Excluir</button>
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
      activeTab: 'visualizacao',
      movimentacoes: [],
      datasMovimentacoes: [],
      dataSelecionada: null,
      piqueteOrigem: null,
      piqueteDestino: null,
      movimentacaoParaExcluir: null,
      movimentacoesSelecionadas: [],
      mostrarFormulario: false,
      filtro: {
        nome: '',
        tipo: '',
        categoria: ''
      },
    }
  },
  mounted() {
    const dataSelecionada = this.$route.params.data;
    const piqueteOrigem = this.$route.params.piqueteOrigem;
    const piqueteDestino = this.$route.params.piqueteDestino;

        if (dataSelecionada && piqueteOrigem && piqueteDestino) {
            this.dataSelecionada = dataSelecionada;
            this.piqueteOrigem = piqueteOrigem;
            this.piqueteDestino = piqueteDestino;
            this.fetchMovimentacoes();
        }
  },
  methods: {

    async fetchMovimentacoes() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/movimentacoes/por-detalhe/`, {
          params: {
                dataSelecionada: this.dataSelecionada,
                piqueteOrigem: this.piqueteOrigem,
                piqueteDestino: this.piqueteDestino
            },
        });
        this.movimentacoesSelecionadas = response.data;
        
        if(this.movimentacoesSelecionadas.length === 0){
        this.$router.push('/movimentacoes');
        }
      } catch (error) {
        console.error('Erro ao carregar dados da movimentacao:', error);
      }
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

    acessarEdicao(movimentacao) {
      this.$router.push({
        name: 'MovimentacaoEdicao', 
        params: { movimentacaoId: movimentacao.id } 
      })
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'movimentacoes') {
        this.$router.push('/movimentacoes');
      }
    },

    confirmarExclusaoMovimentacao(movimentacao) {
      this.movimentacaoParaExcluir = movimentacao;
    },
    
    async apagarMovimentacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/movimentacoes/${this.movimentacaoParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Movimentacao excluído com sucesso!');
          this.fetchMovimentacoes();
          this.movimentacaoParaExcluir = null;
        } else {
          alert('Erro ao excluir a movimentacao. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoModal');
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

<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Movimentacões</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Movimentações</h2>
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
          <label for="dataCompra" class="form-label me-2">Data</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação" 
          class="form-control" id="dataMovimentacao" v-model="filtro.dataMovimentacao" required>
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
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Movimentação</button>
        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data Movimentação</th>
              <th scope="col">Piquete de Origem</th>
              <th scope="col">Piquete de Destino</th>
              <th scope="col">Tipo</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(detalhesMovimentacao, index) in listaDetalhes" :key="index">
              <td>{{ formatarData(detalhesMovimentacao.dataMovimentacao) }}</td>
              <td>{{ detalhesMovimentacao.piqueteOrigem.nome }} - {{ detalhesMovimentacao.piqueteOrigem.propriedade.nome }}</td>
              <td>{{ detalhesMovimentacao.piqueteDestino.nome }} - {{ detalhesMovimentacao.piqueteDestino.propriedade.nome }}</td>
              <td>{{ achaTipo(detalhesMovimentacao)}}</td>
              <td>
                <button @click="acessarVisualizacao(detalhesMovimentacao)" class="btn-acoes btn-sm"><i class="fas fa-eye"></i></button>
                <button @click="confirmarExclusao(detalhesMovimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
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
            Tem certeza de que deseja excluir esta Movimentação?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarMovimentacaoPorDetalhe()">Excluir</button>
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
      movimentacoes: [],
      dataParaExclusao: null,
      listaDetalhes: [],
      formData: {
            animal: [],
            dataMovimentacao: null,
            piqueteOrigem: null,
            piqueteDestino: null,
            motivo: null,
      },
      mostrarFormulario: false,
      filtro: {
        animal: [],
        dataMovimentacao: '',
      },
    }
  },
  mounted() {
    this.buscarMovimentacoesDaApi();
  },
  methods: {
    async buscarMovimentacoesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/movimentacoes/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.movimentacoes = response.data;
        this.preencherDetalhesMovimentacoes();

      } catch (error) {
        console.error('Erro ao buscar movimentacoes da API:', error);
      }
    },

    async preencherDetalhesMovimentacoes(){
      let detalhesMovimentacao = null;
      this.movimentacoes.forEach(movimentacao => {
        detalhesMovimentacao = {
            dataMovimentacao: movimentacao.dataMovimentacao,
            piqueteOrigem: movimentacao.piqueteOrigem,
            piqueteDestino: movimentacao.piqueteDestino,
        }
      this.listaDetalhes.push(detalhesMovimentacao)
      });
    },

    achaTipo(movimentacao){ 
      if(movimentacao.piqueteOrigem.propriedade.id == localStorage.getItem('propriedadeSelecionada')
      && movimentacao.piqueteDestino.propriedade.id == localStorage.getItem('propriedadeSelecionada')){
        return 'Interna'
      }
      else if(movimentacao.piqueteOrigem.propriedade.id == localStorage.getItem('propriedadeSelecionada')){
        return 'Saída'
      }
      else{
        return 'Entrada'
      }
    },
    
    acessarVisualizacao(movimentacao) {
        this.$router.push({
            name: 'MovimentacaoVisualizacao', 
            params: { 
              data: movimentacao.dataMovimentacao, 
              piqueteOrigem: movimentacao.piqueteOrigem.id,
              piqueteDestino: movimentacao.piqueteDestino.id
             } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'MovimentacaoCadastro', 
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
    confirmarExclusao(data) {
      this.dataParaExclusao = data;
    },
    async apagarMovimentacaoPorDetalhe() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/movimentacoes-animais/datas/${this.dataParaExclusao}/`, {
        });

        if (response.status === 204) {
          alert('Movimentacoes excluídas com sucesso!');
          this.dataParaExclusao = null;
        } else {
          alert('Erro ao excluir movimentacoes. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.buscarMovimentacoesDaApi();
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

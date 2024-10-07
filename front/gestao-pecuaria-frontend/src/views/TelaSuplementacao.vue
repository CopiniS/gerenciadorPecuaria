<template>
  <div class="background">

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" data-bs-target="#nav-vet" type="button"
          role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Suplementações</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0">
      </div>
    </div>

    <h2>Lista de Suplementações</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" @keyup.enter="aplicarFiltro" class="row g-3 align-items-center"
        v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Produto</label>
          <input type="text" class="form-control input-consistente" id="produto" v-model="filtro.produto">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="piquete" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control input-consistente" id="piquete" v-model="filtro.piquete">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataInicial" class="form-label me-2">Data Inicial</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataInicialInicio"
            :endDate="filtro.dataInicialFim" @update:startDate="val => filtro.dataInicialInicio = val"
            @update:endDate="val => filtro.dataInicialFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataInicial" class="form-label me-2">Data Final</label>
          <DateRangePicker class="input-consistente" :startDate="filtro.dataFinalInicio" :endDate="filtro.dataFinalFim"
            @update:startDate="val => filtro.dataFinalInicio = val"
            @update:endDate="val => filtro.dataFinalFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="status" class="form-label me-2">Status</label>
          <select class="form-select select-consistente" id="status" v-model="filtro.status">
            <option value="andamento">Em andamento</option>
            <option value="finalizado">Finalizado</option>
          </select>
        </div>
        <div class="col-12 d-flex justify-content-start mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

    <div>
      <div class="table-container">
        <div class="button-container">
          <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Suplementação</button>
          <RelatorioPdf titulo="Relatório de Suplementação"
            :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtual]"
            :colunas="['Piquete', 'Produto', 'Quantidade', 'Data Inicial', 'Data Final']"
            :dados="suplementacoes.map(suplementacao => [suplementacao.piquete.nome, suplementacao.produto.nome, suplementacao.quantidade, formatarData(suplementacao.dataInicial), formatarData(suplementacao.dataFinal) || '-'])" />
        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Produto</th>
              <th scope="col">Piquete</th>
              <th scope="col">Quantidade</th>
              <th scope="col">Data Inicial</th>
              <th scope="col">Data Final</th>
              <th scope="col">Status</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(suplementacao, index) in suplementacoes" :key="index">
              <td>{{ suplementacao.produto.nome }}</td>
              <td>{{ suplementacao.piquete.nome }}</td>
              <td>{{ replacePontoVirgula(suplementacao.quantidade) }}</td>
              <td>{{ formatarData(suplementacao.dataInicial) }}</td>
              <td>{{ formatarData(suplementacao.dataFinal) || '-' }}</td>
              <td
                :class="{ 'status-andamento': !suplementacao.dataFinal, 'status-finalizada': suplementacao.dataFinal }">
                {{
                  suplementacao.dataFinal ? 'Finalizada' : 'Em Andamento' }}</td>
              <td>
                <button v-if="!suplementacao.dataFinal" @click="acessarFinalizacao(suplementacao)"
                  class="btn-acoes btn-sm" title="Finalizar Suplementação">
                  <i class="fas fa-check"></i>
                </button>
                <button @click="acessarEdicao(suplementacao)" class="btn-acoes btn-sm" title="Editar Suplementação">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="confirmarExclusao(suplementacao)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal" title="Excluir Suplementação">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>


      </div>

      <!-- Modal de Confirmação de Exclusão -->
      <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
        aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir este Suplementação?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarSuplementacao()">Excluir</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios'
import DateRangePicker from '../components/DateRangePicker.vue';
import RelatorioPdf from '../components/RelatorioPdf.vue';

export default {
  components: {
    DateRangePicker,
    RelatorioPdf
  },
  data() {
    return {
      propriedadeAtual: localStorage.getItem('propriedadeSelecionadaNome'),
      nomeProdutor: localStorage.getItem('produtorNome'),
      suplementacoes: [],
      suplementacoesDaApi: [],
      estaFinalizado: false,
      formData: {
        id: null,
        produto: '',
        piquete: '',
        quantidade: '',
        dataInicial: '',
        dataFinal: null,
      },
      mostrarFormulario: false,
      filtro: {
        produto: '',
        piquete: '',
        dataInicialInicio: '',
        dataInicialFim: '',
        dataFinalInicio: '',
        dataFinalFim: '',
        status: ''
      },
    }
  },
  mounted() {
    this.buscarSuplementacoesDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarSuplementacoesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/suplementacoes/', {
        });
        this.suplementacoesDaApi = response.data;
        this.suplementacoes = this.suplementacoesDaApi;
      } catch (error) {
        console.error('Erro ao buscar suplementacoes da API:', error);
      }
    },

    async apagarSuplementacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/suplementacoes/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Exclusão realizada com sucesso!');
          this.buscarSuplementacoesDaApi();
        } else {
          alert('Erro ao apagar suplementacao. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },


    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.suplementacoes = this.suplementacoesDaApi.filter(suplementacao => {
        return (new Date(suplementacao.dataInicial) >= new Date(this.filtro.dataInicialInicio || '1970-01-01')) &&
          (new Date(suplementacao.dataInicial) <= new Date(this.filtro.dataInicialFim || '9999-12-31')) &&
          (new Date(suplementacao.dataFinal) >= new Date(this.filtro.dataFinalInicio || '1970-01-01')) &&
          (new Date(suplementacao.dataFinal) <= new Date(this.filtro.dataFinalFim || '9999-12-31')) &&
          suplementacao.produto.nome.includes(this.filtro.produto) &&
          suplementacao.piquete.nome.includes(this.filtro.piquete) &&
          (
            ((this.filtro.status == 'andamento' && suplementacao.dataFinal == null) || this.filtro.status == '') ||
            ((this.filtro.status == 'finalizado' && suplementacao.dataFinal != null) || this.filtro.status == '')
          );
      });
    },

    limparFiltro() {
      this.filtro.produto = '';
      this.filtro.piquete = '';
      this.filtro.dataInicialInicio = '';
      this.filtro.dataInicialFim = '';
      this.filtro.dataFinalInicio = '';
      this.filtro.dataFinalFim = '';
      this.filtro.status = '';

      this.suplementacoes = this.suplementacoesDaApi;

      // Resetando as datas no DateRangePicker
      this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaFinalizado(suplementacao) {
      if (suplementacao.dataFinal != null) {
        this.estaFinalizado = true;
      }
      else {
        this.estaFinalizado = false;
      }
    },

    acessarEdicao(suplementacao) {
      this.$router.push({
        name: 'SuplementacaoEdicao',
        params: { suplementacaoId: suplementacao.id }
      })
    },

    acessarCadastro() {
      this.$router.push({
        name: 'SuplementacaoCadastro',
      })
    },

    acessarFinalizacao(suplementacao) {
      this.$router.push({
        name: 'SuplementacaoFinalizacao',
        params: { suplementacaoId: suplementacao.id }
      })
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    confirmarExclusao(suplementacao) {
      this.formData = {
        id: suplementacao.id,
      };
    },

    formatarData(data) {
      if (data) {
        const date = new Date(data);
        const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
        return utcDate.toLocaleDateString('pt-BR', options);
      }
    },

    replacePontoVirgula(valorString) {
      valorString = valorString.replace(".", ",");

      return valorString;
    },
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  z-index: 0; /* Garante que a imagem de fundo fique na camada mais baixa */
}

.background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../assets/logo-sem-fundo.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}

nav, .tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
}

.table-container, .button-container {
  position: relative;
  z-index: 1; /* Garante que as tabelas e botões estejam acima da imagem de fundo */
}

.table-container table tbody tr td {
  background-color: transparent !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  /* Adiciona uma borda verde na parte inferior */
  background-color: transparent !important;
}

.button-container {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
  margin-bottom: 20px;
  white-space: nowrap;
}

.btn-success {
  margin-right: 10px;
  margin-bottom: 10px;
  z-index: 2; /* Garante que o botão esteja acima da imagem */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  z-index: 2; /* Garante que o botão de ação esteja acima da imagem */
}

.btn-acoes i {
  color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.status-andamento {
  color: #ff9800;
  /* Laranja */
}

.status-finalizada {
  color: #4caf50;
  /* Verde */
}

.input-consistente,
.select-consistente {
  width: 200px;
}
</style>
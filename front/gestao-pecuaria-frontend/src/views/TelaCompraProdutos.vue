<template>
  <div class="background">

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'produtos' }" id="nav-produtos-tab"
          @click="selectTab('produtos')" type="button" role="tab" aria-controls="nav-produtos"
          aria-selected="true">Lista de Produtos</button>

        <button class="nav-link" :class="{ active: activeTab === 'compras' }" id="nav-compras-tab"
          @click="selectTab('compras')" type="button" role="tab" aria-controls="nav-compras"
          aria-selected="false">Histórico de Compras</button>

      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'produtos' }" id="nav-produtos" role="tabpanel"
        aria-labelledby="nav-produtos-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'compras' }" id="nav-compras" role="tabpanel"
        aria-labelledby="nav-compras-tab">

      </div>
    </div>

    <h2>Histórico de Compras</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" @keyup.enter="aplicarFiltro" class="row g-3 align-items-center"
        v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataCompra" class="form-label me-2">Data da Compra</label>
          <DateRangePicker ref="dateRangePicker" :startDate="filtro.dataCompraInicio" :endDate="filtro.dataCompraFim"
            @update:startDate="val => filtro.dataCompraInicio = val"
            @update:endDate="val => filtro.dataCompraFim = val" />

        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Produto</label>
          <input type="text" class="form-control input-consistente" id="produto" v-model="filtro.produto">
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
          <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Compra</button>
          <RelatorioPdf
  titulo="Relatório de Compra de Produto"
  :cabecalho="['Produtor: ' + nomeProdutor, 'Propriedade: ' +propriedadeAtualNome]"
  :colunas="['Nome do Produto', 'Data', 'Validade', 'Quantidade Comprada', 'Valor Unitário', 'Valor Total']"
  :dados="compras.map(compra => [compra.produto.nome, formatarData(compra.dataCompra), formatarData(compra.validade), compra.quantidadeComprada, formatarValor(compra.valorUnitario), formatarValor((compra.valorUnitario*compra.quantidadeComprada).toFixed(2))])"
  :mostrarSoma="false"
/>

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
              <td>{{ formatarData(compra.dataCompra) }}</td>
              <td>{{ compra.produto.nome }}</td>
              <td>{{ formatarValor(compra.valorUnitario) }}</td>
              <td>{{ compra.quantidadeComprada }}</td>
              <td>{{ formatarData(compra.validade) }}</td>
              <td>{{ compra.lote }}</td>
              <td>
                <button @click="acessarEdicao(compra)" class="btn-acoes btn-sm" title="Editar Compra">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="confirmarExclusao(compra)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal" title="Excluir Compra">
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
              Tem certeza de que deseja excluir esta Compra?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarCompra()">Excluir</button>
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
    RelatorioPdf,
    DateRangePicker
  },
  data() {
    return {
      activeTab: 'compras',
      compras: [],
      comprasDaApi: [],
      propriedadeAtualNome: localStorage.getItem('propriedadeSelecionadaNome'),
      nomeProdutor: localStorage.getItem('produtorNome'),
      formData: {
        id: null,
        dataCompra: '',
        produto: '',
        valorUnitario: '',
        quantidadeComprada: '',
        validade: '',
        lote: '',
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      mostrarFormulario: false,
      filtro: {
        dataCompraInicio: '',
        dataCompraFim: '',
        produto: '',
      },
    }
  },
  mounted() {
    this.buscarComprasDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarComprasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/compras-produtos/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.comprasDaApi = response.data;
        this.compras = this.comprasDaApi;
      } catch (error) {
        console.error('Erro ao buscar compras de produtos da API:', error);
      }
    },

    async apagarCompra() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/compras-produtos/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Exclusão realizada com sucesso!');
          this.buscarComprasDaApi();
        } else {
          alert('Erro ao apagar compra. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },


    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.compras = this.comprasDaApi.filter(compra => {
        return (new Date(compra.dataCompra) >= new Date(this.filtro.dataCompraInicio || '1970-01-01')) &&
          (new Date(compra.dataCompra) <= new Date(this.filtro.dataCompraFim || '9999-12-31')) &&
          compra.produto.nome.includes(this.filtro.produto);
      });
    },

    limparFiltro() {
      this.filtro.dataCompraInicio = null; // ou ''
      this.filtro.dataCompraFim = null; // ou ''
      this.filtro.produto = '';
      this.compras = this.comprasDaApi;

      // Resetando as datas no DateRangePicker
      this.$refs.dateRangePicker.resetDates();
    },


    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    acessarEdicao(compra) {
      this.$router.push({
        name: 'CompraProdutoEdicao',
        params: { compraId: compra.id }
      })
    },

    acessarCadastro() {
      this.$router.push({
        name: 'CompraProdutoCadastro',
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

    confirmarExclusao(compra) {
      this.formData = {
        id: compra.id,
      };
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'produtos') {
        this.$router.push('/produtos');
      }
    },

    formatarValor(valor) {
    if (typeof valor !== 'number') {
      valor = parseFloat(valor);
    }
    return valor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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

.input-consistente,
.select-consistente {
  width: 200px;
}

.button-container {
  display: flex;
  flex-wrap: nowrap; /* Garante que os botões não vão para a linha seguinte */
  gap: 10px; /* Espaço entre os botões */
  margin-bottom: 20px; 
  white-space: nowrap; /* Evita quebras de linha nos botões */
}
</style>

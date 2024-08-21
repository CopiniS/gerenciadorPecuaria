<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Gastos</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Gastos</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataGasto" class="form-label me-2">Data do Gasto</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataGastoInicio" :endDate="filtro.dataGastoFim"
      @update:startDate="val => filtro.dataGastoInicio = val"
      @update:endDate="val => filtro.dataGastoFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Descrição</label>
          <input type="text" class="form-control input-consistente" id="descricao" v-model="filtro.descricao">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Categoria</label>
          <input type="text" class="form-control input-consistente" id="categoria" v-model="filtro.categoria">
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
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Gasto</button>
        </div>
        <table class="table table-bordered">
            <thead>
                <tr>
                <th scope="col">Data</th>
                <th scope="col">Tipo</th>
                <th scope="col">Valor</th>
                <th scope="col">Descricao</th>
                <th scope="col">Categoria</th>
                <th scope="col">Ações</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(gasto, index) in gastos" :key="index">
                <td>{{ formatarData(gasto.dataGasto) }}</td>
                <td>{{ gasto.tipo }}</td>
                <td>{{ replacePontoVirgula(gasto.valor) }}</td>
                <td>{{ gasto.descricao }}</td>
                <td>{{ retornaCategoria(gasto.categoria) }}</td>
                <td>
                    <button @click="acessarEdicao(gasto)" class="btn-acoes btn-sm" title="Editar Gasto">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmarExclusao(gasto)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#confirmacaoExclusaoModal" title="Excluir Gasto">
                      <i class="fas fa-trash-alt"></i>
                    </button>
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
            Tem certeza de que deseja excluir este gasto?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarGasto()">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from '/src/interceptadorAxios'
import DateRangePicker from './DateRangePicker.vue';

export default {
  name: 'TelaProdutos',
  components: {
    DateRangePicker
  },
  data() {
    return {
      gastos: [],
      gastosDaApi: [],
      formData: {
        id: null,
        dataGasto: '',
        valor: '',
        descricao: null,
        categoria: null,
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      mostrarFormulario: false,
      filtro: {
        dataGastoInicio: '',
        dataGastoFim: '',
        descricao: '',
        categoria: '',
      },
      modalTitle: 'Cadastro de Gasto',
    }
  },
  mounted() {
    this.buscarGastosDaApi();
  },
  methods: {
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarGastosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/gastos/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.gastosDaApi = response.data;
        this.gastos = this.gastosDaApi;
      } catch (error) {
        console.error('Erro ao buscar gastos da API:', error);
      }
    },

    async apagarGasto() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/gastos/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Gasto apagada com sucesso!');
          this.buscarGastosDaApi();
        } else {
          alert('Erro ao apagar gasto. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },


//FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.gastos = this.gastosDaApi.filter(gasto => {
        if(gasto.descricao == null){
          gasto.descricao = '';
        }
        if(gasto.categoria == null){
          gasto.categoria = '';
        }
        return  (new Date(gasto.dataGasto) >= new Date(this.filtro.dataGastoInicio || '1970-01-01')) &&
                (new Date(gasto.dataGasto) <= new Date(this.filtro.dataGastoFim || '9999-12-31')) &&
                gasto.descricao.includes(this.filtro.descricao) &&
                gasto.categoria.includes(this.filtro.categoria);
      });
    },

    limparFiltro() {
      this.filtro.dataGastoInicio = null;
      this.filtro.dataGastoFim = null;
      this.filtro.descricao = '';
      this.filtro.categoria = '';

      this.gastos = this.gastosDaApi;

       // Resetando as datas no DateRangePicker
  this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


//FUNÇÕES AUXILIARES---------------------------------------------------------------------------------------------------------------------
    acessarEdicao(gasto) {
      this.$router.push({
        name: 'EdicaoGasto', 
        params: { gastoId: gasto.id } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'CadastroGasto', 
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

    confirmarExclusao(gasto) {
      this.formData = {
        id: gasto.id,
      };
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

    replacePontoVirgula(valorString){
      valorString = valorString.replace(".", ",");

      return valorString;
    },

    retornaCategoria(string){
      switch (string) {
        case 'mao_de_obra':
          return 'Mão de Obra';
        case 'manutencao_maquinas':
          return 'Manutenção de Máquinas';
        case 'manutencao_benfeitorias':
          return 'Manutenção de Benfeitorias';
        case 'medicamentos':
          return 'Medicamentos';
        case 'combustiveis':
          return 'Combustíveis';
        case 'despesa_administrativa':
          return 'Despesa Administrativa';
        case 'sementes':
          return 'Sementes';
        case 'adubos':
          return 'Adubos';
        case 'outros':
          return 'Outros';
        case 'compra_maquinas':
          return 'Compra de Máquinas';
        case 'construcao_benfeitorias':
          return 'Construção de Benfeitorias';
        case 'implantacao_lavouras':
          return 'Implantação de Lavouras';
        case 'aquisicao_terra':
          return 'Aquisição de Terra';
      }
    }
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
  overflow-x: auto;
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

.button-group {
  display: flex;
  gap: 10px; 
}

.input-consistente, .select-consistente {
    width: 200px; 
}

</style>

<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Despesas</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Despesas</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataDespesa" class="form-label me-2">Data da Despesa</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataDespesaInicio" :endDate="filtro.dataDespesaFim"
      @update:startDate="val => filtro.dataDespesaInicio = val"
      @update:endDate="val => filtro.dataDespesaFim = val" />
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
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Despesa</button>
        </div>
        <table class="table table-bordered">
            <thead>
                <tr>
                <th scope="col">Data</th>
                <th scope="col">Valor</th>
                <th scope="col">Descricao</th>
                <th scope="col">Categoria</th>
                <th scope="col">Ações</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(despesa, index) in despesas" :key="index">
                <td>{{ formatarData(despesa.dataDespesa) }}</td>
                <td>{{ replacePontoVirgula(despesa.valor) }}</td>
                <td>{{ despesa.descricao }}</td>
                <td>{{ despesa.categoria }}</td>
                <td>
                    <button @click="acessarEdicao(despesa)" class="btn-acoes btn-sm" title="Editar Despesa">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmarExclusao(despesa)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#confirmacaoExclusaoModal" title="Excluir Despesa">
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
            Tem certeza de que deseja excluir esta despesa?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarDespesa()">Excluir</button>
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
      despesas: [],
      despesasDaApi: [],
      formData: {
        id: null,
        dataDespesa: '',
        valor: '',
        descricao: null,
        categoria: null,
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      mostrarFormulario: false,
      filtro: {
        dataDespesaInicio: '',
        dataDespesaFim: '',
        descricao: '',
        categoria: '',
      },
      modalTitle: 'Cadastro de Despesa',
    }
  },
  mounted() {
    this.buscarDespesasDaApi();
  },
  methods: {
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarDespesasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/outras-despesas/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.despesasDaApi = response.data;
        this.despesas = this.despesasDaApi;
      } catch (error) {
        console.error('Erro ao buscar outras despesas da API:', error);
      }
    },

    async apagarDespesa() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/outras-despesas/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Despesa apagada com sucesso!');
          this.buscarDespesasDaApi();
        } else {
          alert('Erro ao apagar despesa. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },


//FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.despesas = this.despesasDaApi.filter(despesa => {
        if(despesa.descricao == null){
          despesa.descricao = '';
        }
        if(despesa.categoria == null){
          despesa.categoria = '';
        }
        return  (new Date(despesa.dataDespesa) >= new Date(this.filtro.dataDespesaInicio || '1970-01-01')) &&
                (new Date(despesa.dataDespesa) <= new Date(this.filtro.dataDespesaFim || '9999-12-31')) &&
                despesa.descricao.includes(this.filtro.descricao) &&
                despesa.categoria.includes(this.filtro.categoria);
      });
    },

    limparFiltro() {
      this.filtro.dataDespesaInicio = null;
      this.filtro.dataDespesaFim = null;
      this.filtro.descricao = '';
      this.filtro.categoria = '';

      this.despesas = this.despesasDaApi;

       // Resetando as datas no DateRangePicker
  this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


//FUNÇÕES AUXILIARES---------------------------------------------------------------------------------------------------------------------
    acessarEdicao(despesa) {
      this.$router.push({
        name: 'EdicaoDespesa', 
        params: { despesaId: despesa.id } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'CadastroDespesa', 
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

    confirmarExclusao(despesa) {
      this.formData = {
        id: despesa.id,
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

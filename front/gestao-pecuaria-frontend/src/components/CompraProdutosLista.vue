<template>
<div class="background">

  <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'produtos' }" id="nav-produtos-tab" @click="selectTab('produtos')" 
        type="button" role="tab" aria-controls="nav-produtos" aria-selected="true">Lista de Produtos</button>
        
        <button class="nav-link" :class="{ active: activeTab === 'compras' }" id="nav-compras-tab" @click="selectTab('compras')" 
        type="button" role="tab" aria-controls="nav-compras" aria-selected="false">Histórico de Compras</button>
        
      </div>
    </nav>
    
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'produtos' }" id="nav-produtos" role="tabpanel" aria-labelledby="nav-produtos-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'compras' }" id="nav-compras" role="tabpanel" aria-labelledby="nav-compras-tab">
        
      </div>
    </div>

<h2>Histórico de Compras</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataCompra" class="form-label me-2">Data da Compra</label>
          <DateRangePicker ref="dateRangePicker" 
  :startDate="filtro.dataCompraInicio" 
  :endDate="filtro.dataCompraFim"
  @update:startDate="val => filtro.dataCompraInicio = val"
  @update:endDate="val => filtro.dataCompraFim = val"
/>

        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Produto</label>
          <input type="text" class="form-control input-consistente" id="produto" v-model="filtro.produto">
        </div>
        <div class="col-12 d-flex justify-content-center mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

  <div>
    <div class="table-container">
        <div class="button-container">
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Compra</button>
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
            <td>{{ replacePontoVirgula(compra.valorUnitario) }}</td>
            <td>{{ compra.quantidadeComprada }}</td>
            <td>{{ formatarData(compra.validade) }}</td>
            <td>{{ compra.lote }}</td>
            <td>
                <button @click="acessarEdicao(compra)" class="btn-acoes btn-sm"><i class="fas fa-edit"></i></button>
                <button @click="confirmarExclusao(compra)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
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
import DateRangePicker from './DateRangePicker.vue';

export default {
  components: {
    DateRangePicker
  },
  data() {
    return {
      activeTab: 'compras',
      compras: [],
      comprasDaApi: [],
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
        const response = await api.delete(`http://127.0.0.1:8000/compras-produtos/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Compra apagado com sucesso!');
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
        return  (new Date(compra.dataCompra) >= new Date(this.filtro.dataCompraInicio || '1970-01-01')) &&
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

    acessarCadastro(){
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

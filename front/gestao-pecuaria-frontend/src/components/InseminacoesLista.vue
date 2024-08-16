<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Inseminações</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Inseminações</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataInseminacao" class="form-label me-2">Data da Inseminação</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataInseminacaoInicio" :endDate="filtro.dataInseminacaoFim"
      @update:startDate="val => filtro.dataInseminacaoInicio = val"
      @update:endDate="val => filtro.dataInseminacaoFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Animal</label>
          <input type="text" @input="aplicarBrincoMask" class="form-control input-consistente" id="animal" v-model="filtro.animal">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Veterinário</label>
          <input type="text" class="form-control input-consistente" id="veterinario" v-model="filtro.veterinario">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Touro</label>
          <input type="text" class="form-control input-consistente" id="identificadorTouro" v-model="filtro.identificadorTouro">
        </div>
        <div class="col-12 d-flex justify-content-start mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro()">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

  <div>
    <div class="table-container">
        <div class="button-container">
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Inseminação</button>
        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data Inseminação</th>
              <th scope="col">Animal</th>
              <th scope="col">Veterinario</th>
              <th scope="col">Touro</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(inseminacao, index) in inseminacoes" :key="index">
              <td>{{ formatarData(inseminacao.dataInseminacao) }}</td>
              <td>{{ inseminacao.animal.brinco }}</td>
              <td>{{ inseminacao.veterinario.nome }}</td>
              <td>{{ inseminacao.identificadorTouro }}</td>
              <td>
                <button @click="acessarEdicao(inseminacao)" class="btn-acoes btn-sm" title="Editar Inseminação">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="confirmarExclusaoInseminacao(inseminacao)" class="btn-acoes btn-sm" 
                data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal" title="Excluir Inseminação">
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
            Tem certeza de que deseja excluir esta Inseminação?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarInseminacao()">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from '/src/interceptadorAxios'
import { masksMixin } from '../mixins/maks';
import DateRangePicker from './DateRangePicker.vue';

export default {
  mixins: [masksMixin],
  components: {
    DateRangePicker
  },
  data() {
    return {
      inseminacoes: [],
      inseminacoesDaApi: [],
      formData: {
        id: null,
        dataInseminacao: '',
        veterinario: '',
        animal: '',
        identificadorTouro: '',
      },
      mostrarFormulario: false,
      filtro: {
        dataInseminacaoInicio: '',
        dataInseminacaoFim: '',
        animal: '',
        veterinario: '',
        identificadorTouro: '',
      },
    }
  },
  mounted() {
    this.buscarInseminacoesDaApi();
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(event){
      const value = event.target.value;
      this.filtro.animal =  this.brincoFiltroMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarInseminacoesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/inseminacoes/' , {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.inseminacoesDaApi = response.data;
        this.inseminacoes = this.inseminacoesDaApi;

      } catch (error) {
        console.error('Erro ao buscar inseminacoes da API:', error);
      }
    },
    
    async apagarInseminacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/inseminacoes/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Inseminação excluída com sucesso!');
          this.buscarInseminacoesDaApi();
        } else {
          alert('Erro ao excluir inseminacoes. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoModal');
    },
    

//FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.inseminacoes = this.inseminacoesDaApi.filter(inseminacao => {
        return  (new Date(inseminacao.dataInseminacao) >= new Date(this.filtro.dataInseminacaoInicio || '1970-01-01')) &&
                (new Date(inseminacao.dataInseminacao) <= new Date(this.filtro.dataInseminacaoFim || '9999-12-31')) &&
                inseminacao.animal.brinco.includes(this.filtro.animal) &&
                inseminacao.veterinario.nome.includes(this.filtro.veterinario) &&
                inseminacao.identificadorTouro.includes(this.filtro.identificadorTouro);
                
      });
    },

    limparFiltro() {
      this.filtro.dataInseminacaoInicio = '';
      this.filtro.dataInseminacaoFim = '';
      this.filtro.animal = '';
      this.filtro.veterinario = '';
      this.filtro.identificadorTouro = '';
      this.inseminacoes = this.inseminacoesDaApi;

       // Resetando as datas no DateRangePicker
  this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


//FUNÇÕES AUXILIARES---------------------------------------------------------------------------------------------------------------------
    acessarEdicao(inseminacao) {
      this.$router.push({
        name: 'InseminacaoEdicao', 
        params: { inseminacaoId: inseminacao.id } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'InseminacaoCadastro', 
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

    confirmarExclusaoInseminacao(inseminacao) {
      this.formData.id = inseminacao.id;
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

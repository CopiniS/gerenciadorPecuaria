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
        <form @submit.prevent="aplicarFiltro"  @keyup.enter="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
          <div class="col-auto d-flex align-items-center">
            <label for="dataMovimentacao" class="form-label me-2">Data</label>
            <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataMovimentacaoInicio" :endDate="filtro.dataMovimentacaoFim"
        @update:startDate="val => filtro.dataMovimentacaoInicio = val"
        @update:endDate="val => filtro.dataMovimentacaoFim = val" />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Piquete de Origem</label>
            <input type="text" class="form-control input-consistente" id="piqueteOrigem" v-model="filtro.piqueteOrigem">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Piquete de Destino</label>
            <input type="text" class="form-control input-consistente" id="piqueteDestino" v-model="filtro.piqueteDestino">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="tipoCultivo" class="form-label me-2">Tipo</label>
            <select class="form-select select-consistente" id="tipo" v-model="filtro.tipo">
              <option value="">Selecione o tipo</option>
              <option value="Entrada">Entrada</option>
              <option value="Saida">Saída</option>
              <option value="Interna">Interna</option>
            </select>
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Animal</label>
            <input type="text" @input="aplicarBrincoMask" class="form-control input-consistente" id="animal" v-model="filtro.animal">
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
              <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Movimentação</button>
              <RelatorioPdf
  titulo="Relatório de Movimentação"
  :cabecalho="['Nome do produtor: ' + nomeProdutor]"
  :colunas="['Propriedade de origem', 'Piquete de origem', 'Propriedade de destino', 'Piquete de destino', 'Brinco', 'Data da movimentação']"
  :dados="movimentacoes.map(movimentacao => [movimentacao.piqueteOrigem.propriedade.nome, movimentacao.piqueteOrigem.nome, movimentacao.piqueteDestino.propriedade.nome, movimentacao.piqueteDestino.nome, movimentacao.animal.brinco, formatarData(movimentacao.dataMovimentacao)])"
/>

          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Data</th>
                <th scope="col">Animal</th>
                <th scope="col">Piquete de Origem</th>
                <th scope="col">Piquete de Destino</th>
                <th scope="col">Tipo</th>
                <!-- <th scope="col">Ações</th> -->
              </tr>
            </thead>
            <tbody>
              <tr v-for="(movimentacao, index) in movimentacoes" :key="index">
                <td>{{ formatarData(movimentacao.dataMovimentacao) }}</td>
                <td>{{ movimentacao.animal.brinco}}</td>
                <td>{{ movimentacao.piqueteOrigem.nome }} - {{ movimentacao.piqueteOrigem.propriedade.nome }}</td>
                <td>{{ movimentacao.piqueteDestino.nome }} - {{ movimentacao.piqueteDestino.propriedade.nome }}</td>
                <td>{{ achaTipo(movimentacao)}}</td>
                <!-- <td>
                  <button @click="confirmarExclusaoMovimentacao(movimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                  data-bs-target="#confirmacaoExclusaoModal" title="Excluir Movimentação">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td> -->
              </tr>
            </tbody>
          </table>
      </div>
  
      <!-- Modal de Confirmação de Exclusão -->
      <!-- <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
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
              <button type="button" class="btn btn-danger" @click="apagarMovimentacao()">Excluir</button>
            </div>
          </div>
        </div>
      </div> -->
    </div>
  </div>
  </template>
  
  <script>
  import api from '/src/interceptadorAxios';
  import { masksMixin } from '../mixins/maks';
  import DateRangePicker from '../components/DateRangePicker.vue';
  import RelatorioPdf from '../components/RelatorioPdf.vue';
  
  export default {
    mixins: [masksMixin],
    components: {
      DateRangePicker,
      RelatorioPdf
    },
    data() {
      return {
      propriedadeAtualNome: localStorage.getItem('propriedadeSelecionadaNome'),
      nomeProdutor: localStorage.getItem('produtorNome'),
        movimentacoes: [],
        movimentacoesDaApi: [],
        formData: {
              animal: [],
              dataMovimentacao: null,
              piqueteOrigem: null,
              piqueteDestino: null,
              motivo: null,
        },
        mostrarFormulario: false,
        filtro: {
          dataMovimentacaoInicio: '',
          dataMovimentacaoFim: '',
          animal: '',
          piqueteOrigem: '',
          piqueteDestino: '',
          tipo: '',
        },
      }
    },
    mounted() {
      this.buscarMovimentacoesDaApi();
    },
    methods: {
  //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarBrincoMask(event){
        const value = event.target.value;
        this.filtro.animal =  this.brincoFiltroMask(value);
      },
  
  
  //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
      async buscarMovimentacoesDaApi() {
        try {
          const response = await api.get('http://127.0.0.1:8000/movimentacoes/' , {
            params: {
                  propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
              },
          });
          this.movimentacoesDaApi = response.data;
          this.movimentacoes = this.movimentacoesDaApi;
  
        } catch (error) {
          console.error('Erro ao buscar movimentacoes da API:', error);
        }
      },
  
      async apagarMovimentacao() {
        try {
          const response = await api.delete(`http://127.0.0.1:8000/movimentacoes/${this.formData.id}/`, {
          });
  
          if (response.status === 204) {
            alert('Exclusão realizada com sucesso!');
            this.buscarMovimentacoesDaApi();
          } else {
            alert('Erro ao excluir movimentacoes. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal('confirmacaoExclusaoModal');
      },
  
  
  //FILTROS----------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarFiltro() {
        const propriedadeAtualNome = localStorage.getItem('propriedadeSelecionada');
        this.movimentacoes = this.movimentacoesDaApi.filter(movimentacao => {
          return  (new Date(movimentacao.dataMovimentacao) >= new Date(this.filtro.dataMovimentacaoInicio || '1970-01-01')) &&
                  (new Date(movimentacao.dataMovimentacao) <= new Date(this.filtro.dataMovimentacaoFim || '9999-12-31')) &&
                  movimentacao.animal.brinco.includes(this.filtro.animal) &&
                  movimentacao.piqueteOrigem.nome.includes(this.filtro.piqueteOrigem) &&
                  movimentacao.piqueteDestino.nome.includes(this.filtro.piqueteDestino) &&
                  (
                    (this.filtro.tipo == 'entrada' && movimentacao.piqueteOrigem.propriedade.id != propriedadeAtualNome && 
                    movimentacao.piqueteDestino.propriedade.id == propriedadeAtualNome) || 
                    (this.filtro.tipo == 'saida' && movimentacao.piqueteOrigem.propriedade.id == propriedadeAtualNome && 
                    movimentacao.piqueteDestino.propriedade.id != propriedadeAtualNome) || 
                    (this.filtro.tipo == 'interna' && movimentacao.piqueteOrigem.propriedade.id == propriedadeAtualNome && 
                    movimentacao.piqueteDestino.propriedade.id == propriedadeAtualNome ||
                    this.filtro.tipo == '')
                  );
        });
      },
  
      limparFiltro() {
          this.filtro.dataMovimentacaoInicio = '';
          this.filtro.dataMovimentacaoFim = '',
          this.filtro.animal = '',
          this.filtro.piqueteOrigem = '',
          this.filtro.piqueteDestino = '',
          this.filtro.tipo = '',
  
          this.movimentacoes = this.movimentacoesDaApi;
           // Resetando as datas no DateRangePicker
    this.$refs.dateRangePicker.resetDates();
      },
      
      toggleFormulario() {
        this.mostrarFormulario = !this.mostrarFormulario;
      },
  
  
  //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------
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
  
      confirmarExclusaoMovimentacao(movimentacao) {
        this.formData.id = movimentacao.id;
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
  
  .input-consistente, .select-consistente {
      width: 200px; 
  }
  
  </style>
  
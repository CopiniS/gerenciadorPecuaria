<template>
  <div class="background">
    <nav>
    <div class="nav nav-tabs" id="nav-tab" role="tablist">
      <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
      data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Aplicações</button>
    </div>
  </nav>
  <div class="tab-content" id="nav-tabContent">
    <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
   </div>
  
    <h2>Lista de Aplicações</h2>


    <!-- Exibe o skeleton enquanto carrega os dados -->
    <SkeletonListagem v-if="loading" />

    <div v-else>
      <div class="d-flex align-items-start table-container flex-column">
        <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
        </div>
        <form @submit.prevent="aplicarFiltro"  @keyup.enter="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
          <div class="col-auto d-flex align-items-center">
            <label for="dataAplicacao" class="form-label me-2">Data</label>
            <DateRangePicker ref="dateRangePicker" class="input-consistente" 
        :startDate="filtro.dataAplicacaoInicio" 
        :endDate="filtro.dataAplicacaoFim"
        @update:startDate="val => filtro.dataAplicacaoInicio = val"
        @update:endDate="val => filtro.dataAplicacaoFim = val" />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Produto</label>
            <input type="text" class="form-control input-consistente" id="produto" v-model="filtro.produto">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Animal</label>
            <input type="text" @input="aplicarBrincoMask" class="form-control input-consistente" id="animal" v-model="filtro.animal">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Piquete</label>
            <input type="text" class="form-control input-consistente" id="piquete" v-model="filtro.piquete">
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
        <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Aplicação</button>
        <RelatorioPdf
    titulo="Relatório de Aplicação de Produtos"
    :cabecalho="['Produtor: ' + nomeProdutor]"
    :colunas="['Nome do Produto', 'Data da Aplicação', 'Brinco', 'Piquete', 'Dosagem']"
    :dados="aplicacoes.map(aplicacao => [aplicacao.produto.nome, formatarData(aplicacao.dataAplicacao), aplicacao.animal.brinco, aplicacao.animal.piquete.nome, replacePontoVirgula(aplicacao.dosagem)])"
    :mostrarSoma="false"
  />
  
      </div>
        <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Data</th>
                <th scope="col">Animal</th>
                <th scope="col">Piquete</th>
                <th scope="col">Produto</th>
                <th scope="col">Dosagem</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(aplicacao, index) in aplicacoes" :key="index">
                <td>{{ formatarData(aplicacao.dataAplicacao) }}</td>
                <td>{{ aplicacao.animal.brinco}}</td>
                <td>{{ aplicacao.animal.piquete.nome}}</td>
                <td>{{ aplicacao.produto.nome}}</td>
                <td>{{ replacePontoVirgula(aplicacao.dosagem)}}</td>
                <td>
                  <button @click="acessarEdicao(aplicacao)" class="btn-acoes btn-sm" title="Editar Aplicação">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="confirmarExclusaoAplicacao(aplicacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                  data-bs-target="#confirmacaoExclusaoAnimalModal" title="Excluir Aplicação">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
      </div>
  
        <!-- Modal de Confirmação de Exclusão do animal da Inseminacao -->
        <div class="modal fade" id="confirmacaoExclusaoAnimalModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoAnimalModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="confirmacaoExclusaoAnimalModalLabel">Confirmação de Exclusão de Animal</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir esta aplicação?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarAplicacao">Excluir</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
  </template>
  
  <script>
  import api from '/src/interceptadorAxios';
  import { masksMixin } from '../mixins/maks';
  import DateRangePicker from '../components/DateRangePicker.vue';
  import RelatorioPdf from '../components/RelatorioPdf.vue';
  import SkeletonListagem from "../components/SkeletonListagem.vue";
  
  export default {
    mixins: [masksMixin],
    components: {
      RelatorioPdf,
      DateRangePicker,
      SkeletonListagem,
    },
    data() {
      return {
        activeTab: 'aplicacoes',
          aplicacoes: [],
          aplicacoesDaApi: [],
        nomeProdutor: localStorage.getItem('produtorNome'),
          formData: {
              id: null,
              produto: '',
              animal: [],
              dosagem: '',
              dataAplicacao: '',
              observacao: null,
        },
        mostrarFormulario: false,
        filtro: {
          dataAplicacaoInicio: '',
          dataAplicacaoFim: '',
          animal: '',
          piquete: '',
          produto: ''
        },
        loading: true,
        modalTitle: 'Cadastro de Aplicacao',
      }
  
    },
    mounted() {
      this.buscarAplicacoesDaApi();
    },
    methods: {
  //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarBrincoMask(event){
        const value = event.target.value;
        this.filtro.animal =  this.brincoFiltroMask(value);
      },
  
  
  //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
      async buscarAplicacoesDaApi(){
          try {
              const response = await api.get('http://127.0.0.1:8000/aplicacoes-produtos/' , {
              params: {
                  propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
              },
              });
              this.aplicacoesDaApi = response.data;
              this.aplicacoes = this.aplicacoesDaApi;
              this.loading = false;
          } catch (error) {
          console.error('Erro ao buscar aplicações de produtos da API:', error);
          }
      },
  
      async apagarAplicacao() {
        try {
          const response = await api.delete(`http://127.0.0.1:8000/aplicacoes-produtos/${this.formData.id}/`);
  
          if (response.status === 204) {
            alert('Exclusão realizada com sucesso!');
            this.buscarAplicacoesDaApi();
          } else {
            alert('Erro ao excluir a aplicação. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal('confirmacaoExclusaoAnimalModal');
      },
  
  
  //FILTROS-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarFiltro() {
        this.aplicacoes = this.aplicacoesDaApi.filter(aplicacao => {
          return  (new Date(aplicacao.dataAplicacao) >= new Date(this.filtro.dataAplicacaoInicio || '1970-01-01')) &&
                  (new Date(aplicacao.dataAplicacao) <= new Date(this.filtro.dataAplicacaoFim || '9999-12-31')) &&
                  aplicacao.animal.brinco.includes(this.filtro.animal) &&
                  aplicacao.animal.piquete.nome.includes(this.filtro.piquete) &&
                  aplicacao.produto.nome.includes(this.filtro.produto);
        });
      },
      
      limparFiltro() {
    this.filtro.dataAplicacaoInicio = '';
    this.filtro.dataAplicacaoFim = '';
    this.filtro.animal = '';
    this.filtro.piquete = '';
    this.filtro.produto = '';
  
    // Resetando as datas no DateRangePicker
    this.$refs.dateRangePicker.resetDates();
  
    // Restaura a lista de aplicações
    this.aplicacoes = this.aplicacoesDaApi;
  },
  
  
      toggleFormulario() {
        this.mostrarFormulario = !this.mostrarFormulario;
      },
  
  
  //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
      fecharModal(modalId) {
        var closeButton = document.getElementById(modalId).querySelector('.btn-close');
        if (closeButton) {
          closeButton.click();
        } else {
          console.error('Botão de fechar não encontrado no modal:', modalId);
        }
      },
  
      acessarEdicao(aplicacao) {
        this.$router.push({
          name: 'AplicacaoProdutoEdicao', 
          params: { aplicacaoId: aplicacao.id } 
        })  
      },
  
      acessarCadastro(){
          this.$router.push({
          name: 'AplicacaoProdutoCadastro', 
        })
      },
  
      confirmarExclusaoAplicacao(aplicacao) {
        this.formData.id = aplicacao.id;
      },
  
      formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
      },
  
      replacePontoVirgula(valorString) {
        if (typeof valorString === 'string') {
          valorString = valorString.replace(".", ",");
        } else {
          valorString = '-';
        }
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
  .nav-link.active {
    background-color: #d0d0d0 !important;
    /* Cor um pouco mais escura quando a aba está ativa */
  }
  .input-consistente, .select-consistente {
      width: 200px; 
  }
  
  </style>
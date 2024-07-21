<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'movimentacoes' }" id="nav-vet-tab"
          @click="selectTab('movimentacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Movimentação</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Movimentação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'movimentacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Movimentação</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group" >
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :placeholder="dataPlaceholder" class="form-control" id="dataMovimentacaoEdicao"
                v-model="formData.dataMovimentacao" :class="{ 'is-invalid': !isDataValida }">
            </div>
            <div class="mb-3 input-group" >
              <input v-model="brinco" @input="inputBrinco" type="text" class="form-control" :placeholder="brincoPlaceholder"
                id="brincoInput" :class="{ 'is-invalid': !isBrincoValido }">
            </div>
            <div class="list-group" v-if="brinco && animaisFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group" >
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="piqueteOrigemNome" type="text" class="form-control" :placeholder="piqueteOrigemPlaceholder" :disabled="true">
            </div>

            <div class="mb-3 input-group" >
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="piqueteDestinoNome" @input="filtrarPiquetesDestino()" type="text" class="form-control"
                :placeholder="piqueteDestinoPlaceholder" :class="{ 'is-invalid': !isPiqueteDestinoValido }">
            </div>
            <div class="list-group" v-if="piqueteDestinoNome && filteredPiquetesDestino.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="piquete in filteredPiquetesDestino" :key="piquete.id" @click="selecionarPiqueteDestino(piquete)">
                {{ piquete.nome }} - {{ piquete.propriedade.nome }}
              </button>
            </div>

            <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.motivo" type="text" @input="aplicarMotivoMask" class="form-control" id="motivo" 
                    placeholder="Motivo">
                    <div>({{ contadorMotivo }} / 255)</div>
                </div>

            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('movimentacoes')">Cancelar</button>
              <button type="submit" class="btn btn-success">Enviar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';
import { masksMixin } from '../mixins/maks';

export default {
  mixins: [masksMixin],

    data() {
        return {
            activeTab: 'edicao', // Começa na aba de edição
            animais: [],
      animaisFiltrados: [],
      brinco: '',
      piquetes: [],
      piquetesDaPropriedade: [],
      piqueteOrigemNome: '',
      piqueteDestinoNome: '',
      propriedadeAtual: null,
      piqueteId: null,
      filteredPiquetesOrigem: [],
      filteredPiquetesDestino: [],
      dataSelecionada: null,
      piqueteOrigemSelecionado: null,
      piqueteDestinoSelecionado: null,
      contadorMotivo: null,
      formData: {
          id: null,
          animal: null,
          dataMovimentacao: null,
          piqueteOrigem: null,
          piqueteDestino: null,
          motivo: null,
      },
      isBrincoValido: true,
      isDataValida: true,
      isPiqueteValido: true,
      isPiqueteOrigemValido: true,
      isPiqueteDestinoValido: true,
      isMotivoKgValido: true,
      brincoPlaceholder: 'Brinco do animal*',
      dataPlaceholder: 'Data da aplicacao*',
      piquetePlaceholder: 'Piquete*',
      piqueteOrigemPlaceholder: 'Piquete de Origem*',
      piqueteDestinoPlaceholder: 'Piquete de Destino*'
        };
    },
 
    mounted() {
        const movimentacaoId = this.$route.params.movimentacaoId;
        if (movimentacaoId) {
            this.fetchMovimentacao(movimentacaoId);
        }
        this.buscarAnimaisDaApi();
        this.buscarPiquetesDaApi();
    },
    methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
      aplicarMotivoMask(event){
        const value = event.target.value;
        this.formData.motivo = this.observacoesMask(value);
        this.contadorMotivo = this.formData.motivo.length;
      },

      aplicarBrincoMask(value){
        this.brinco =  this.brincoMask(value);
      },

      inputBrinco(event){
        const value = event.target.value;
        this.aplicarBrincoMask(value);
        this.filterAnimais();
      },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
      async fetchMovimentacao(id) {
        try {
          const response = await api.get(`http://127.0.0.1:8000/movimentacoes/movimentacao/${id}`);
          const movimentacao = response.data;
          this.formData.id = movimentacao[0].id;
          this.formData.animal = movimentacao[0].animal.id;
          this.formData.dataMovimentacao = movimentacao[0].dataMovimentacao;
          this.formData.piqueteOrigem = movimentacao[0].piqueteOrigem.id;
          this.formData.piqueteDestino = movimentacao[0].piqueteDestino.id;
          this.formData.motivo = movimentacao[0].motivo;

          this.brinco = movimentacao[0].animal.brinco;
          this.piqueteOrigemNome = movimentacao[0].piqueteOrigem.nome
          this.piqueteDestinoNome = movimentacao[0].piqueteDestino.nome
          this.dataSelecionada = movimentacao[0].dataMovimentacao
          this.piqueteOrigemSelecionado = movimentacao[0].piqueteOrigem.id
          this.piqueteDestinoSelecionado = movimentacao[0].piqueteDestino.id
          this.contadorMotivo = this.formData.motivo.length;
          
        } catch (error) {
          console.error('Erro ao carregar dados da movimentacao:', error);
        }
      },

      async buscarAnimaisDaApi() {
          try {
              const response = await api.get('http://127.0.0.1:8000/animais/vivos-piquetes' , {
              params: {
                  propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
              },
              });
              this.animais = response.data;
          } catch (error) {
              console.error('Erro ao buscar animais da API:', error);
          }
      },

      async buscarPiquetesDaApi() {
        try {
          const response = await api.get('http://127.0.0.1:8000/piquetes/piquetes-propriedades');
          this.piquetes = response.data;
        } catch (error) {
          console.error('Erro ao buscar piquetes da API:', error);
        }
      },

      async submitForm() {
        if (this.verificaVazio()) {
        try {
            const response = await api.patch(`http://127.0.0.1:8000/movimentacoes/${this.formData.id}/`, this.formData , {
          });

            if (response.status === 200) {
              alert('Alterações salvas com sucesso!');
              this.selectTab('movimentacoes');
            } else {
              alert('Erro ao salvar alterações. Tente novamente mais tarde.');
            }
          } catch (error) {
            console.error('Erro ao enviar requisição:', error);
            alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
          }
        }
      },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
      filtrarPiquetesDestino() {
        this.filteredPiquetesDestino = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteDestinoNome));
      },

      selecionarPiqueteDestino(piquete) {
        this.piqueteDestinoNome = piquete.nome + " - " + piquete.propriedade.nome;
        this.formData.piqueteDestino = piquete.id;
        this.filteredPiquetesDestino = [];
      },
      
      filterAnimais() {
          this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
      },

      selectAnimal(animal) {
          this.brinco = animal.brinco;
          this.formData.piqueteOrigem = animal.piquete.id;
          this.piqueteOrigemNome = animal.piquete.nome
          this.formData.animal = animal.id;
          this.animaisFiltrados = [];
      },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
      verificaVazio(){
        //DATA DA MOVIMENTAÇÃO
        if(this.formData.dataMovimentacao != null){
          if(this.formData.dataMovimentacao.trim() != ''){
            this.isDataValida = true;
            this.dataPlaceholder = 'Data da Movimentação';
          }
          else{
            this.isDataValida = false;
            this.dataPlaceholder = 'Data da Movimentação é um Campo Obrigatório';
          }
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Movimentação é um Campo Obrigatório';
        }
        
        //BRINCO OU TODOS DO PIQUETE
        if(this.radioEscolha == 'brinco'){
          //BRINCO 
          if(this.brinco != null){
            if(this.brinco.trim() != ''){
              this.isBrincoValido = true;
              this.brincoPlaceholder = 'Brinco do Animal'
            }
            else{
            this.isBrincoValido = false;
            this.brincoPlaceholder = 'Brinco do Animal é um Campo Obrigatório';
            }
          }
          else{
            this.isBrincoValido = false;
            this.brincoPlaceholder = 'Brinco do Animal é um Campo Obrigatório';
          }
        }
        else{
          //PIQUETE ORIGEM
          if(this.piqueteOrigemNome != null){
            if(this.piqueteOrigemNome.trim() != ''){
              this.isPiqueteOrigemValido = true;
              this.piqueteOrigemPlaceholder = 'Piquete de Origem';
            }
            else{
              this.isPiqueteOrigemValido = false;
              this.piqueteOrigemPlaceholder = 'Piquete de Origem é um Campo Obrigatório'
            }
          }
          else{
            this.isPiqueteOrigemValido = false;
            this.piqueteOrigemPlaceholder = 'Piquete de Origem é um Campo Obrigatório'
          }
        }

        //PIQUETE DE DESTINO
        if(this.piqueteDestinoNome != null){
            if(this.piqueteDestinoNome.trim() != ''){
              this.isPiqueteDestinoValido = true;
              this.piqueteDestinoPlaceholder = 'Piquete de Destino';
            }
            else{
              this.isPiqueteDestinoValido = false;
              this.piqueteDestinoPlaceholder = 'Piquete de Destino é um Campo Obrigatório'
            }
        }
        else{
          this.isPiqueteDestinoValido = false;
          this.piqueteDestinoPlaceholder = 'Piquete de Destino é um Campo Obrigatório'
        }

        //MOTIVO
        if(this.formData.motivo != null && this.formData.motivo.trim() == ''){
          this.formData.motivo = null;
        }

        return (
          this.isDataValida &&
          this.isBrincoValido &&
          this.isPiqueteOrigemValido &&
          this.isPiqueteDestinoValido
        );
      },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
      selectTab(tab) {
        this.activeTab = tab;
        if (tab === 'movimentacoes') {
          this.$router.push('/movimentacoes');
        }
      },

      cancelarEdicao() {
        this.$router.push('/movimentacoes');
      },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
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
  background-color: #ededef !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
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

.is-invalid {
  border-color: #dc3545;
}
</style>

<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'movimentacoes' }" id="nav-vet-tab"
          @click="selectTab('movimentacoes')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Movimentação</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Movimentação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'movimentacoes' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Movimentação</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group" >
              <span class="input-group-text" title="Data da Movimentação"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :placeholder="dataPlaceholder" class="form-control" id="dataMovimentacaoCadastro"
                v-model="formData.dataMovimentacao" :class="{ 'is-invalid': !isDataValida }" title="Data da Movimentação">
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

            <div class="mb-3 input-group position-relative">
                    <span class="input-group-text" title="Motivo da Movimentação"><i class="fas fa-comment"></i></span>
                    <input v-model="formData.motivo" type="text" @input="aplicarMotivoMask" class="form-control" id="motivo" 
                    placeholder="Motivo" title="Motivo da Movimentação">
                </div>
            <div class="mb-3 input-group" >
              <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
              <input v-model="piqueteOrigemNome" @input="filtrarPiquetesOrigem()" type="text" class="form-control"
                :placeholder="piqueteOrigemPlaceholder" :class="{ 'is-invalid': !isPiqueteOrigemValido }">
            </div>
            <div class="list-group" v-if="piqueteOrigemNome && filteredPiquetesOrigem.length">
              <button type="button" class="list-group-item list-group-item-action"
                v-for="piquete in filteredPiquetesOrigem" :key="piquete.id" @click="selecionarPiqueteOrigem(piquete)">
                {{ piquete.nome }} - {{ piquete.propriedade.nome }}
              </button>
            </div>
            <div class="mb-3 input-group" v-if="animaisFiltrados.length != 0">
              <div class="checkbox-container">
                <label v-if="animaisFiltrados.length != 0">
                <input type="checkbox" v-model="selecionaTodos" @change="ativaSelecaoTodos"> Selecionar todos
              </label>
              <hr>
                <label @change="desativaSelecaoTodos" v-for="animal in animaisOrdenados" :key="animal.id">
                  <input type="checkbox" :value="animal.id" v-model="formData.animal"> {{ animal.brinco }} 
                </label>
              </div>
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
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      piquetes: [],
      piquetesDaPropriedade: [],
      piqueteOrigemNome: '',
      piqueteDestinoNome: '',
      piqueteId: null,
      filteredPiquetesOrigem: [],
      filteredPiquetesDestino: [],
      radioEscolha: 'brinco',
      contadorMotivo: 0,
      selecionaTodos: false,
      formData: {
        animal: [],
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
      brincoPlaceholder: 'Brinco do Animal*',
      dataPlaceholder: 'Data da Movimentação*',
      piquetePlaceholder: 'Piquete*',
      piqueteOrigemPlaceholder: 'Piquete de Origem*',
      piqueteDestinoPlaceholder: 'Piquete de Destino*'
    };
  },
  computed: {
    animaisOrdenados() {
        return this.animaisFiltrados.slice().sort((a, b) => a.brinco.localeCompare(b.brinco));
    }
},
  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarPiquetesParaDestino();
    this.buscarPiquetesParaOrigem();
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
    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/vivos-piquetes', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    async buscarPiquetesParaDestino() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/piquetes-propriedades');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarPiquetesParaOrigem() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/com-animais-propriedade', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetesDaPropriedade = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/movimentacoes/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/movimentacoes');
          } else {
            alert('Erro ao cadastrar movimentacao. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filtrarPiquetesOrigem() {
      this.filteredPiquetesOrigem = this.piquetesDaPropriedade.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteOrigemNome));
    },

    async selecionarPiqueteOrigem(piquete) {
      this.piqueteId = piquete.id;
      this.formData.piqueteOrigem = piquete.id;
      this.piqueteOrigemNome = piquete.nome + " - " + piquete.propriedade.nome;
      this.filteredPiquetesOrigem = [];
      this.preencheCheckBox();
      await this.buscarPiquetesParaDestino();
      this.atualizaDestino();
    },

    filtrarPiquetesDestino() {
      this.filteredPiquetesDestino = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteDestinoNome));
    },

    async selecionarPiqueteDestino(piquete) {
      this.piqueteDestinoNome = piquete.nome + " - " + piquete.propriedade.nome;
      this.formData.piqueteDestino = piquete.id;
      this.filteredPiquetesDestino = [];
      await this.buscarPiquetesParaOrigem();
      this.atualizaOrigem();
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
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
preencheCheckBox(){
      this.animaisFiltrados = this.animais.filter(animal => animal.piquete.id === this.piqueteId);
      console.log('animais filtrados: ', this.animaisFiltrados);
      
    },

    ativaSelecaoTodos(){
      this.formData.animal = [];
      if(this.selecionaTodos){
        this.animais.forEach(animal => {
          this.formData.animal.push(animal.id);
        });
      }
    },

    desativaSelecaoTodos(){
      this.selecionaTodos = false;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'movimentacoes') {
        this.$router.push('/movimentacoes');
      }
    },

    atualizaOrigem(){
      let indice = null;
      for (let index = 0; index < this.piquetesDaPropriedade.length; index++) {
        const piquete = this.piquetesDaPropriedade[index];
        if(piquete.id === this.formData.piqueteDestino){
          indice = index;
          break;
        }
      }
      console.log('indice: ', indice);
      if(indice != null){
        this.piquetesDaPropriedade.splice(indice, 1)
      }
    },

    atualizaDestino(){
      let indice = null;
      for (let index = 0; index < this.piquetes.length; index++) {
        const piquete = this.piquetes[index];
        if(piquete.id === this.formData.piqueteOrigem){
          indice = index;
          break;
        }
      }
      console.log('indice: ', indice);
      if(indice != null){
        this.piquetes.splice(indice, 1)
      }
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

#legenda {
    font-size: 16px;
}

.checkbox-container {
    gap: 10px;
    border: 1px solid #6c757d;
    border-radius: 5px;
    padding: 20px;
    width: 40%; /* Largura do contêiner */
    height: 150px; /* Altura do contêiner */
    overflow-y: auto; /* Adiciona uma barra de rolagem se necessário */
}

.checkbox-container label {
    display: flex;
    align-items: center;
}
</style>

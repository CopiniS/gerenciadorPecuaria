<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista
          de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Animais</button>
      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'animais' }" id="nav-animais" role="tabpanel"
        aria-labelledby="nav-animais-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Animais</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tag"></i>*</span>
              <select v-model="formData.piquete" :class="{ 'is-invalid': !isPiqueteValido }" class="form-select"
                id="piquete" aria-label="Piquete" :placeholder="piquetePlaceholder">
                <option disabled :value="null">Selecione o piquete</option>
                <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{ piquete.nome }}</option>
              </select>
            </div>
            <hr>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user-tag"></i>*</span>
              <input v-model="formData.brinco" :class="{ 'is-invalid': !isBrincoValido }" type="text" class="form-control"
                @input="aplicarBrincoMask" id="brinco" :placeholder="brincoPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i>*</span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataNascimentoValido }" :placeholder="dataNascimentoPlaceholder"
                class="form-control" id="dataNascimentoCadastro" v-model="formData.dataNascimento" >
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-venus-mars"></i>*</span>
              <select v-model="formData.sexo" :class="{ 'is-invalid': !isSexoValido }" class="form-select" id="sexo"
                aria-label="Sexo" :placeholder="sexoPlaceholder" >
                <option disabled :value="null">Selecione o sexo</option>
                <option value="macho">Macho</option>
                <option value="femea">Fêmea</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-horse"></i></span>
              <select v-model="formData.racaPredominante" :class="{ 'is-invalid': !isRacaPredominanteValido }"
                class="form-select" id="racaPredominante" aria-label="Raça Predominante">
                <option disabled :value="null">Selecione a raça predominante</option>
                <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}</option>
              </select>
              <button @click="acessarCadastroRaca()"><i class="fas fa-plus"></i></button>

            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
              <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacao"
                placeholder="Observações sobre a Raça"></textarea>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-mars"></i></span>
              <input v-model="formData.brincoPai" @input="inputBrincoPai" type="text" class="form-control"
                id="brincoPai" placeholder="Digite o brinco do Pai..." pattern="\d*">
            </div>
            <div class="list-group" v-if="formData.brincoPai && machosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in machosFiltrados"
                :key="animal.id" @click="selectPai(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-venus"></i></span>
              <input v-model="formData.brincoMae" @input="inputBrincoMae" type="text" class="form-control"
               id="brincoMae" placeholder="Digite o brinco da Mãe..." pattern="\d*">
            </div>
            <div class="list-group" v-if="formData.brincoMae && femeasFiltradas.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                :key="animal.id" @click="selectMae(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
              <input v-model="formData.rfid" :class="{ 'is-invalid': !isRfidValido }" type="text" class="form-control"
                id="rfid" :placeholder="rfidPlaceholder" pattern="\d*">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
              <input v-model="formData.observacoes" type="text" class="form-control" id="observacoes"
                @input="aplicarObservacaoMask" placeholder="Observações">
              <div>({{ contadorObservacoes }} / 255)</div>
            </div>
            <div class="mb-3 input-group">
              <input v-model="comprado" type="checkbox" id="check-comprado"> Animal Comprado
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i>*</span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataCompraValido }" :placeholder="dataCompraPlaceholder" class="form-control"
                id="dataDaCompra" v-model="formData.dataCompra" >
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-weight"></i>*</span>
              <input v-model="formData.valorCompra" :class="{ 'is-invalid': !isValorCompraValido }" type="text"
                @input="aplicarValorCompraMask" class="form-control" id="valorCompra" :placeholder="valorCompraPlaceholder">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('animais')">Cancelar</button>
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

  name: 'TelaAnimais',
  data() {
    return {
      activeTab: 'cadastro',
      animaisDaApi: [],
      racas: [],
      piquetes: [],
      listaMachos: [],
      listaFemeas: [],
      femeasFiltradas: [],
      machosFiltrados: [],
      comprado: false,
      contadorObservacoes: 0,
      formData: {
        id: null,
        brinco: null,
        dataNascimento: null,
        sexo: null,
        racaPredominante: null,
        racaObservacao: null,
        piquete: null,
        brincoPai: null,
        brincoMae: null,
        status: 'Vivo',
        rfid: null,
        observacoes: null,
        dataBaixa: null,
        dataCompra: null,
        valorCompra: null,
      },
      isPiqueteValido: true,
      isBrincoValido: true,
      isDataNascimentoValido: true,
      isSexoValido: true,
      isRacaPredominanteValido: true,
      isRfidValido: true,
      isDataCompraValido: true,
      isValorCompraValido: true,
      piquetePlaceholder: 'Selecione o piquete*',
      brincoPlaceholder: 'Digite o brinco*',
      dataNascimentoPlaceholder: 'Selecione a data de nascimento*',
      sexoPlaceholder: 'Selecione o sexo*',
      racaPredominantePlaceholder: 'Selecione a raça predominante*',
      rfidPlaceholder: 'Digite o RFID',
      dataCompraPlaceholder: 'Selecione a data de compra*',
      valorCompraPlaceholder: 'Digite o valor da compra*',
    }
  },
  async mounted() {
    const animalJSON = this.$route.params.animalJSON;
    if(animalJSON != 'animaisLista'){
      this.preencheForm(animalJSON);
    }
    this.buscarAnimaisDaApi();
    this.buscarRacasDaApi();
    this.buscarPiquetesDaApi();
    this.preencheListas();
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(event){
      const value = event.target.value;
      this.formData.brinco =  this.brincoMask(value);
    },

    aplicarObservacaoMask(event){
      const value = event.target.value;
      this.formData.observacoes = this.observacoesMask(value);
      this.contadorObservacoes = this.formData.observacoes.length;
    },

    aplicarValorCompraMask(event) {
      const value = event.target.value;
      this.formData.valorCompra =  this.valorMask(value);
    },

    aplicarBrincoPaiMask(value){
      this.formData.brincoPai =  this.brincoMask(value);
    },

    inputBrincoPai(event){
      const value = event.target.value;
      this.aplicarBrincoPaiMask(value);
      this.filterMachos();
    },

    aplicarBrincoMaeMask(value){
      this.formData.brincoMae =  this.brincoMask(value);
    },

    inputBrincoMae(event){
      const value = event.target.value;
      this.aplicarBrincoMaeMask(value);
      this.filterFemeas();
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animaisDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },
    
    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/', {
        });
        this.racas = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          console.log('formdata: ', this.formData)
          //FORMATA VALOR DA COMPRA
          if(this.formData.valorCompra){
            this.formData.valorCompra = this.replaceVirgulaPonto(this.formData.valorCompra);
          }

          const response = await api.post(`http://127.0.0.1:8000/animais/`, this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/animais');
            this.preencherListaFemeas();
            this.preencherListaMachos();
          } else {
            alert('Erro ao cadastrar animal. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filterFemeas() {
      this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoMae));
    },

    selectMae(animal) {
      this.formData.brincoMae = animal.brinco;
      this.femeasFiltradas = [];
    },

    filterMachos() {
      this.machosFiltrados = this.listaMachos.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoPai));
    },

    selectPai(animal) {
      this.formData.brincoPai = animal.brinco;
      this.machosFiltrados = [];
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario(){
      let valido = true;
      this.isBrincoValido = true;
      this.brincoPlaceholder = 'Brinco do Animal';

      for (let animal of this.animaisDaApi) {
        if (animal.brinco === this.formData.brinco) {
          this.isBrincoValido = false;
          this.brincoPlaceholder = 'Este Brinco já foi cadastrado';
          this.formData.brinco = null;
          valido = false;
          break;
        }
      }
      return valido;
    },

    verificaVazio(){
      //PIQUETE
      if(this.formData.piquete == null){
        this.isPiqueteValido = false
      }
      else{
        this.isPiqueteValido = true 
      }

      //BRINCO
      if(this.formData.brinco != null){
        if(this.formData.brinco.trim == ''){
          this.isBrincoValido = false
          this.brincoPlaceholder = 'Brinco é um Campo Obrigatório' 
        } 
        else{
          this.isBrincoValido = true
          this.brincoPlaceholder = 'Digite o Brinco' 
        }
      }
      else{
        this.isBrincoValido = false
        this.brincoPlaceholder = 'Brinco é um Campo Obrigatório' 
      }

      //DATA DE NASCIMENTO
      if(this.formData.dataNascimento != null){
        if(this.formData.dataNascimento.trim == ''){
          this.isDataNascimentoValido = false
          this.dataNascimentoPlaceholder = 'Data de Nascimento é um Campo Obrigatório' 
        } 
        else{
          this.isDataNascimentoValido = true
          this.dataNascimentoPlaceholder = 'Digite Data de Nascimento' 
        }
      }
      else{
        this.isDataNascimentoValido = false
        this.dataNascimentoPlaceholder = 'Data de Nascimento é um Campo Obrigatório'  
      }
      
      //SEXO
      if(this.formData.sexo == null){
        this.isSexoValido = false
        this.sexoPlaceholder = 'Sexo é um Campo Obrigatório' 
      }
      else{
        this.isSexoValido = true
        this.sexoPlaceholder = 'Digite o Sexo' 
      }

      //COMPRADO
      if(this.comprado){
        //DATA DA COMPRA
        if(this.formData.dataCompra != null){
          if(this.formData.dataCompra.trim == ''){
            this.isDataCompraValido = false;
            this.dataCompraPlaceholder = 'Data da Compra é um Campo Obrigatório'
          }
          else{
            this.isDataCompraValido = true;
            this.dataCompraPlaceholder = 'Digite a Data da Compra'
          }
        }
        else{
          this.isDataCompraValido = false;
          this.dataCompraPlaceholder = 'Data da Compra é um Campo Obrigatório'
        }
        
        //VALOR DA COMPRA
        if(this.formData.valorCompra != null){
          if(this.formData.valorCompra.trim == ''){
            this.isValorCompraValido = false;
            this.valorCompraPlaceholder = 'Valor da Compra é um Campo Obrigatório'
          }
          else{
            this.isValorCompraValido = true;
            this.dataCompraPlaceholder = 'Digite o Valor da Compra'
          }
        }
        else{
          this.isValorCompraValido = false;
          this.valorCompraPlaceholder = 'Valor da Compra é um Campo Obrigatório'
        }
      }
      else{
        this.formData.dataCompra = null;
        this.formData.valorCompra = null;
        this.isDataCompraValido = true;
        this.dataCompraPlaceholder = 'Data da Compra';
        this.isValorCompraValido = true;
        this.valorCompraPlaceholder = 'Valor da Compra';
      }

      //OS QUE PODEM ESTAR NULOS NO BANCO
      //RAÇA PREDOMINANTE
      if(this.formData.racaPredominante != null && this.formData.racaPredominante === ''){
        this.formData.racaPredominante = null;
      }
      //RAÇA OBSERVAÇÃO
      if(this.formData.racaObservacao != null && this.formData.racaObservacao === ''){
        this.formData.racaObservacao = null;
      }

      //BRINCO PAI
      if(this.formData.brincoPai != null && this.formData.brincoPai === ''){
        this.formData.brincoPai = null;
      }
      
      //BRINCO MÃE  
      if(this.formData.brincoMae != null && this.formData.brincoMae === ''){
        this.formData.brincoMae = null;
      }

      //RFID
      if(this.formData.rfid != null && this.formData.rfid === ''){
        this.formData.rfid = null;
      }

      //OBSERVAÇÕES
      if(this.formData.observacoes != null && this.formData.observacoes === ''){
        this.formData.observacoes = null;
      }


      return (
        this.isPiqueteValido &&
        this.isBrincoValido &&
        this.isDataNascimentoValido &&
        this.isSexoValido &&
        this.isDataCompraValido &&
        this.isValorCompraValido
      );
    },



//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    preencheForm(animalJSON){
      this.formData = JSON.parse(animalJSON);
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
    },

    acessarCadastroRaca(){
      let jsonAnimal = JSON.stringify(this.formData);
      this.$router.push({
        name: 'RacaCadastro',
        params: {animalJSON: jsonAnimal}
      })
    },

    async preencheListas() {
      this.preencherListaMachos();
      this.preencherListaFemeas();
    },

    async preencherListaFemeas() {
      const response = await api.get(`http://127.0.0.1:8000/animais/femeas`, {
        params: {
          propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
        },
      });
      this.listaFemeas = response.data;
    },

    async preencherListaMachos() {
      const response = await api.get(`http://127.0.0.1:8000/animais/machos`, {
        params: {
          propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
        },
      });
      this.listaMachos = response.data;
    },

    replaceVirgulaPonto(valorString){
      valorString = valorString.replace(",", ".");

      return valorString;
    },

  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color: #ededef;
  /* Um tom mais escuro que o branco */
  min-height: 100vh;
  /* Garante que o fundo cubra toda a altura da tela */
  padding: 20px;
}

.table-container {
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #176d1a;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
  /* Cor um pouco mais escura quando a aba está ativa */
}

.button-group {
  display: flex;
  gap: 10px;
}


.is-invalid {
  border-color: #dc3545;
}
</style>
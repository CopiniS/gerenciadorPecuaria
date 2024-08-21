<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista
          de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-visualizacao-tab"
          @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-visualizacao" 
          aria-selected="true">Visualização de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Animais</button>
      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'animais' }" id="nav-animais" role="tabpanel"
        aria-labelledby="nav-animais-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Animais</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Piquete Atual do Animal"><i class="fas fa-hashtag"></i></span>
              <select disabled v-model="formData.piquete" :class="{ 'is-invalid': !isPiqueteValido }" class="form-select"
                id="piquete" aria-label="Piquete" :placeholder="piquetePlaceholder" title="Piquete Atual do Animal">
                <option disabled value="">Selecione o piquete</option>
                <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{ piquete.nome }}</option>
              </select>
            </div>
            <hr>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Brinco do Animal"><i class="fas fa-user-tag"></i></span>
              <input v-model="formData.brinco" :class="{ 'is-invalid': !isBrincoValido }" type="text" class="form-control"
                @input="aplicarBrincoMask" id="brinco" :placeholder="brincoPlaceholder" title="Brinco do Animal">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data de Nascimento"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataNascimentoValido }" :placeholder="dataNascimentoPlaceholder"
                class="form-control" id="dataNascimentoEdicao" v-model="formData.dataNascimento" title="Data de nascimento">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Sexo do Animal"><i class="fas fa-venus-mars"></i></span>
              <select v-model="formData.sexo" :class="{ 'is-invalid': !isSexoValido }" class="form-select" id="sexo"
                aria-label="Sexo" :placeholder="sexoPlaceholder" title="Sexo do Animal">
                <option disabled value="">Selecione o sexo</option>
                <option value="macho">Macho</option>
                <option value="femea">Fêmea</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Raça Predominante do Animal"><i class="fas fa-horse"></i></span>
              <select v-model="formData.racaPredominante" :class="{ 'is-invalid': !isRacaPredominanteValido }"
                class="form-select" id="racaPredominante" aria-label="Raça Predominante"
                :placeholder="racaPredominantePlaceholder" title="Raça Predominante do Animal">
                <option disabled :value="null">Selecione a raça predominante</option>
                <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}</option>
              </select>
              <button @click="() => { this.$router.push('/raca-edicao'); }" type="button" class="btn btn-acoes"><i
                  class="fas fa-plus"></i></button>

            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Raça de Observação do Animal"><i class="fas fa-sticky-note"></i></span>
              <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacao"
                placeholder="Observações sobre a Raça" title="Raça de Observação do Animal"></textarea>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Brinco do Pai do Animal"><i class="fas fa-mars"></i></span>
              <input v-model="formData.brincoPai" @input="inputBrincoPai" type="text" class="form-control"
                id="brincoPai" placeholder="Digite o brinco do Pai..." title="Brinco do Pai do Animal">
            </div>
            <div class="list-group" v-if="formData.brincoPai && machosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in machosFiltrados"
                :key="animal.id" @click="selectPai(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Brinco da Mãe do Animal"><i class="fas fa-venus"></i></span>
              <input v-model="formData.brincoMae" @input="inputBrincoMae" type="text" class="form-control"
                id="brincoMae" placeholder="Digite o brinco da Mãe..." title="Brinco da Mãe do Animal">
            </div>
            <div class="list-group" v-if="formData.brincoMae && femeasFiltradas.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                :key="animal.id" @click="selectMae(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="RFID do Animal"><i class="fas fa-barcode"></i></span>
              <input v-model="formData.rfid" :class="{ 'is-invalid': !isRfidValido }" type="text" class="form-control"
                id="rfid" :placeholder="rfidPlaceholder" title="RFID do Animal">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Observações do Animal"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacoes" type="text" class="form-control" id="observacoes"
                @input="aplicarObservacaoMask" placeholder="Observações" title="Observações do Animal">
              <div class="character-counter">({{ contadorObservacoes }} / 255)</div>
            </div>
            <div class="mb-3 input-group">
              <input v-model="comprado" type="checkbox" id="check-comprado"> Animal Comprado
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text" title="Data da Compra do Animal"><i class="fas fa-calendar-alt"></i>*</span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataCompraValido }" :placeholder="dataCompraPlaceholder" class="form-control"
                id="dataDaCompra" v-model="formData.dataCompra" title="Data da Compra do Animal">
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text" title="Valor da Compra do Animal"><i class="fas fa-weight"></i>*</span>
              <input v-model="formData.valorCompra" :class="{ 'is-invalid': !isValorCompraValido }" type="text"
                @input="aplicarValorCompraMask" class="form-control" id="valorCompra" :placeholder="valorCompraPlaceholder"
                title="Valor da Compra do Animal">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('animais')">Cancelar</button>
              <button type="submit" class="btn btn-success">Salvar</button>
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
      activeTab: 'edicao',
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
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: null,
        racaObservacao: null,
        piquete: '',
        brincoPai: '',
        brincoMae: '',
        status: 'Vivo',
        rfid: '',
        observacoes: '',
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
      piquetePlaceholder: 'Selecione o piquete',
      brincoPlaceholder: 'Digite o brinco',
      dataNascimentoPlaceholder: 'Selecione a data de nascimento',
      sexoPlaceholder: 'Selecione o sexo',
      racaPredominantePlaceholder: 'Selecione a raça predominante',
      rfidPlaceholder: 'Digite o RFID',
      dataCompraPlaceholder: 'Selecione a data de compra',
      valorCompraPlaceholder: 'Digite o valor da compra',
    }
  },
  async mounted() {
    const animalId = this.$route.params.animalId;
    if (animalId) {
      this.fetchAnimal(animalId);
    }
    this.buscarRacasDaApi();
    this.buscarPiquetesDaApi();
    this.buscarAnimaisDaApi();
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
    async fetchAnimal(animalId) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/animais/animal/${animalId}/`);
        const animais = response.data;
        this.formData.id = animais[0].id;
        this.formData.brinco = animais[0].brinco;
        this.formData.piquete = animais[0].piquete.id;
        this.formData.dataNascimento = animais[0].dataNascimento;
        this.formData.sexo = animais[0].sexo;
        if(this.formData.racaPredominante != null){
          this.formData.racaPredominante = animais[0].racaPredominante.id;
        }
        this.formData.racaObservacao = animais[0].racaObservacao;
        this.formData.brincoPai = animais[0].brincoPai;
        this.formData.brincoMae = animais[0].brincoMae;
        this.formData.rfid = animais[0].rfid;
        this.formData.observacoes = animais[0].observacoes;
        this.formData.dataCompra = animais[0].dataCompra;
        this.formData.valorCompra = this.replacePontoVirgula(animais[0].valorCompra);

        if(this.formData.dataCompra){
          this.comprado = true;
        }

        if(this.formData.observacoes){
          this.contadorObservacoes = this.formData.observacoes;
        }

      } catch (error) {
        console.error('Erro ao buscar animal da API:', error);
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

    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/produtor/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animaisDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          //FORMATA VALOR COMPRA
          this.formData.valorCompra = this.replaceVirgulaPonto(this.formData.valorCompra);

          const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData, {
          });
          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.selectTab('visualizacao');
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
    validarFormulario() {
      let valido = true;
      this.isBrincoValido = true;
      this.brincoPlaceholder = 'Brinco do Animal';
      
      // Cria uma nova lista sem o item com o id atual
      let brincosComExclusao = this.animaisDaApi.filter(animal => animal.id !== this.formData.id);

      // Verifica se o nome do produto já existe na lista
      for (let i = 0; i < brincosComExclusao.length; i++) {
        if (brincosComExclusao[i].brinco === this.formData.brinco) {
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
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
      else if (tab === 'visualizacao') {
        this.$router.push({
            name: 'VizualizarAnimal', 
            params: { animalId: this.formData.id } 
        })
      }
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

    replacePontoVirgula(valorString){
      if(valorString){
        valorString = valorString.replace(".", ",");
      }
      return valorString;
    },

    replaceVirgulaPonto(valorString){
      if(valorString){
        valorString = valorString.replace(",", ".");
      }
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

.position-relative {
  position: relative;
}

.character-counter {
  position: absolute;
  top: 35px;
  right: 10px;
  font-size: 12px;
  color: #6c757d;
}

#legenda {
    font-size: 16px;
}
</style>
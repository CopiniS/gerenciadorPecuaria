<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista
          de Animais</button>
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
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tag"></i>*</span>
              <select v-model="formData.piquete" :class="{ 'is-invalid': !isPiqueteValido }" class="form-select"
                id="piquete" aria-label="Piquete" :placeholder="piquetePlaceholder" required>
                <option disabled value="">Selecione o piquete</option>
                <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{ piquete.nome }}</option>
              </select>
            </div>
            <hr>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-user-tag"></i>*</span>
              <input v-model="formData.brinco" :class="{ 'is-invalid': !isBrincoValido }" type="text" class="form-control"
                id="brinco" :placeholder="brincoPlaceholder" required pattern="\d+">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i>*</span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataNascimentoValido }" :placeholder="dataNascimentoPlaceholder"
                class="form-control" id="dataNascimentoEdicao" v-model="formData.dataNascimento" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-venus-mars"></i>*</span>
              <select v-model="formData.sexo" :class="{ 'is-invalid': !isSexoValido }" class="form-select" id="sexo"
                aria-label="Sexo" :placeholder="sexoPlaceholder" required>
                <option disabled value="">Selecione o sexo</option>
                <option value="macho">Macho</option>
                <option value="femea">Fêmea</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-horse"></i></span>
              <select v-model="formData.racaPredominante" :class="{ 'is-invalid': !isRacaPredominanteValido }"
                class="form-select" id="racaPredominante" aria-label="Raça Predominante"
                :placeholder="racaPredominantePlaceholder">
                <option disabled value="">Selecione a raça predominante</option>
                <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}</option>
              </select>
              <button @click="() => { this.$router.push('/raca-edicao'); }" type="button" class="btn btn-acoes"><i
                  class="fas fa-plus"></i></button>

            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
              <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacao"
                placeholder="Observações sobre a Raça"></textarea>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-mars"></i></span>
              <input v-model="formData.brincoPai" @input="filterMachos()" type="text" class="form-control"
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
              <input v-model="formData.brincoMae" @input="filterFemeas()" type="text" class="form-control"
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
                placeholder="Observações">
            </div>
            <div class="mb-3 input-group">
              <input v-model="comprado" type="checkbox" id="check-comprado"> Animal Comprado
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i>*</span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataCompraValido }" :placeholder="dataCompraPlaceholder" class="form-control"
                id="dataDaCompra" v-model="formData.dataCompra" required>
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-weight"></i>*</span>
              <input v-model="formData.valorCompra" :class="{ 'is-invalid': !isValorCompraValido }" type="text"
                class="form-control" id="valorCompra" :placeholder="valorCompraPlaceholder" required
                pattern="^\d+(\.\d{1,2})?$">
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
import $ from 'jquery';
import 'jquery-mask-plugin/dist/jquery.mask.min';

export default {
  name: 'TelaAnimais',
  data() {
    return {
      activeTab: 'edicao',
      animais: [],
      racas: [],
      piquetes: [],
      listaMachos: [],
      listaFemeas: [],
      femeasFiltradas: [],
      machosFiltrados: [],
      comprado: false,
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
    const animalId = localStorage.getItem('animalSelecionado');
    if (animalId) {
      this.animalId = animalId;
      await this.buscarAnimalDaApi(animalId);
    }
    this.buscarRacasDaApi();
    this.buscarPiquetesDaApi();


    $(document).ready(() => {
      $('#brinco').mask('00000000000000000000', { reverse: true });
      $('#brincoPai').mask('00000000000000000000', { reverse: true });
      $('#brincoMae').mask('00000000000000000000', { reverse: true });
    });
  },

  methods: {
    validarFormulario() {
      this.isPiqueteValido = !!this.formData.piquete;
      if (this.formData.brinco) {
        this.isBrincoValido = /^\d+$/.test(this.formData.brinco.trim());
      }
      this.isDataNascimentoValido = !!this.formData.dataNascimento;
      this.isSexoValido = !!this.formData.sexo;
      this.isRacaPredominanteValido = !!this.formData.racaPredominante;

      if (this.formData.rfid !== null) {
        this.isRfidValido = /^\d*$/.test(this.formData.rfid.trim());
      }

      if (this.formData.racaObservacao === '') {
        this.formData.racaObservacao = null;
      }

      if (this.formData.observacao === '') {
        this.formData.observacao = null;
      }

      if (this.comprado) {
        this.isDataCompraValido = !!this.formData.dataCompra;
        this.isValorCompraValido = /^\d+(\.\d{1,2})?$/.test(this.formData.valorCompra);
      } else {
        this.isDataCompraValido = true;
        this.isValorCompraValido = true;
      }

      this.piquetePlaceholder = this.isPiqueteValido ? 'Selecione o piquete' : 'Selecione um piquete válido';
      this.brincoPlaceholder = this.isBrincoValido ? 'Digite o brinco' : 'Campo Brinco é obrigatório (somente números)';
      this.dataNascimentoPlaceholder = this.isDataNascimentoValido ? 'Selecione a data de nascimento' : 'Campo Data de Nascimento é obrigatório';
      this.sexoPlaceholder = this.isSexoValido ? 'Selecione o sexo' : 'Selecione o sexo';
      this.racaPredominantePlaceholder = this.isRacaPredominanteValido ? 'Selecione a raça predominante' : 'Selecione a raça predominante';
      this.rfidPlaceholder = this.isRfidValido ? 'Digite o RFID' : 'Campo RFID é obrigatório (somente números)';
      this.dataCompraPlaceholder = this.isDataCompraValido ? 'Selecione a data de compra' : 'Campo Data de Compra é obrigatório';
      this.valorCompraPlaceholder = this.isValorCompraValido ? 'Digite o valor da compra' : 'Campo Valor da Compra é obrigatório';

      return (
        this.isPiqueteValido &&
        this.isBrincoValido &&
        this.isDataNascimentoValido &&
        this.isSexoValido &&
        this.isRacaPredominanteValido &&
        this.isRfidValido &&
        this.isDataCompraValido &&
        this.isValorCompraValido
      );
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

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
      if (tab === 'viewAnimal') {
        this.$router.push('/vizualizarAnimal');
      }
    },

    async buscarAnimalDaApi() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/animais/animal/${this.animalId}/`);
        this.animais = response.data;
        this.animal = this.animais[0];
        this.formDataFoto.animal = this.animal.id;
        this.buscarOcorrenciasDoAnimal();

        this.formData = {
          ...this.animal,
          dataNascimento: this.animal.dataNascimento ? this.animal.dataNascimento.split('T')[0] : '',
          dataCompra: this.animal.dataCompra ? this.animal.dataCompra.split('T')[0] : '',
        };
        this.comprado = !!this.animal.dataCompra;

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

    async submitForm() {
      if (this.verificaVazio()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData, {
          });
          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
            this.fecharModal("edicaoModal");
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
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

    filterFemeas() {
      this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoMae));
    },

    filterMachos() {
      this.machosFiltrados = this.listaMachos.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoPai));
    },

    selectPai(animal) {
      this.formData.brincoPai = animal.brinco;
      this.machosFiltrados = [];
    },

    selectMae(animal) {
      this.formData.brincoMae = animal.brinco;
      this.femeasFiltradas = [];
    },

    vizualizarAnimal(animal) {
      localStorage.setItem('animalSelecionado', animal.id);
      this.$router.push('/vizualizarAnimal');
    }

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
</style>
<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicialAnimais || loadingInicialPiquetes || loadingInicialRacas" />
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
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>

            <div ref="dropdownPiquete" class="select mb-3 input-group"
              @keydown.up.prevent="navigateOptionsPiquete('up')" @keydown.down.prevent="navigateOptionsPiquete('down')"
              @keydown.enter.prevent="selectHighlightedPiquete">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownPiquete">
                <span class="input-group-text" title="Piquete"><i class="fas fa-box"></i></span>
                <input v-model="nomePiquete" :class="{ 'is-invalid': !isPiqueteValido }" @input="inputPiquete"
                  @keydown.up.prevent="navigateOptionsPiquete('up')" autocomplete="off"
                  @keydown.down.prevent="navigateOptionsPiquete('down')" type="text" class="form-control"
                  :placeholder="piquetePlaceholder" id="caixa-select" title="Piquete">
              </div>
              <div class="itens" v-show="dropdownPiqueteOpen">
                <ul class="options">
                  <li v-for="(piquete, index) in piquetesFiltrados" :key="piquete.id" :value="piquete.id"
                    @click="selectPiquete(piquete)" :class="{ 'highlighted': index === highlightedIndexPiquete }">{{
                      piquete.nome }}</li>
                </ul>
              </div>
            </div>
            <hr class="custon-hr">
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Brinco do Animal"><i class="fas fa-user-tag"></i></span>
              <input v-model="formData.brinco" :class="{ 'is-invalid': !isBrincoValido }" type="text"
                class="form-control" @input="aplicarBrincoMask" id="brinco" :placeholder="brincoPlaceholder"
                title="Brinco do Animal" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data de Nascimento"><i class="fas fa-calendar-alt"></i></span>
              <DateComponent :class="{ 'is-invalid': !isDataNascimentoValido }" :placeholder="dataNascimentoPlaceholder"
                class="form-control" id="dataNascimentoCadastro" v-model="formData.dataNascimento"
                title="Data de nascimento" autocomplete="off" @update:selectedDate="updateDataNascimento" />
            </div>

            <div class="mb-3 input-group">
              <span class="input-group-text" title="Sexo"><i class="fas fa-venus-mars"></i></span>
              <select v-model="formData.sexo" :class="{ 'is-invalid': !isSexoValido }" class="form-select" id="sexo"
                aria-label="Sexo" :placeholder="sexoPlaceholder" title="Sexo">
                <option disabled :value="null">{{ sexoPlaceholder }}</option>
                <option value="macho">Macho</option>
                <option value="femea">Fêmea</option>
              </select>
            </div>
            <div ref="dropdownRaca" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsRaca('up')"
              @keydown.down.prevent="navigateOptionsRaca('down')" @keydown.enter.prevent="selectHighlightedRaca">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownRaca">
                <span class="input-group-text" title="Raca Predominante"><i class="fas fa-box"></i></span>
                <input v-model="nomeRaca" @input="inputRaca" @keydown.up.prevent="navigateOptionsRaca('up')"
                  autocomplete="off" @keydown.down.prevent="navigateOptionsRaca('down')" type="text"
                  class="form-control" placeholder="Raça Predominante" id="caixa-select" title="Raca Predominante">
              </div>
              <div class="itens" v-show="dropdownRacaOpen">
                <ul class="options">
                  <li v-for="(raca, index) in racasFiltradas" :key="raca.id" :value="raca.id" @click="selectRaca(raca)"
                    :class="{ 'highlighted': index === highlightedIndexRaca }">{{
                      raca.nome }}</li>
                </ul>
              </div>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Observação da Raça"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.racaObservacao" type="text" class="form-control" id="racaObservacao"
                placeholder="Observação da Raça" title="Observação da Raça" autocomplete="off" />
            </div>

            <div ref="dropdownPai" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsPai('up')"
              @keydown.down.prevent="navigateOptionsPai('down')" @keydown.enter.prevent="selectHighlightedPai">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownPai">
                <span class="input-group-text" title="Brinco do Pai"><i class="fas fa-box"></i></span>
                <input v-model="formData.brincoPai" @input="inputPai" @keydown.up.prevent="navigateOptionsPai('up')"
                  autocomplete="off" @keydown.down.prevent="navigateOptionsPai('down')" type="text" class="form-control"
                  placeholder="Brinco do Pai" id="caixa-select" title="Brinco do Pai">
              </div>
              <div class="itens" v-show="dropdownPaiOpen">
                <ul class="options">
                  <li v-for="(macho, index) in machosFiltrados" :key="macho.id" :value="macho.id"
                    @click="selectPai(macho)" :class="{ 'highlighted': index === highlightedIndexPai }">{{
                      macho.brinco }}</li>
                </ul>
              </div>
            </div>

            <div ref="dropdownMae" class="select mb-3 input-group" @keydown.up.prevent="navigateOptionsMae('up')"
              @keydown.down.prevent="navigateOptionsMae('down')" @keydown.enter.prevent="selectHighlightedMae">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdownMae">
                <span class="input-group-text" title="Brinco da Mãe"><i class="fas fa-box"></i></span>
                <input v-model="formData.brincoMae" @input="inputMae" @keydown.up.prevent="navigateOptionsMae('up')"
                  autocomplete="off" @keydown.down.prevent="navigateOptionsMae('down')" type="text" class="form-control"
                  placeholder="Brinco da Mãe" id="caixa-select" title="Brinco da Mãe">
              </div>
              <div class="itens" v-show="dropdownMaeOpen">
                <ul class="options">
                  <li v-for="(femea, index) in femeasFiltradas" :key="femea.id" :value="femea.id"
                    @click="selectMae(femea)" :class="{ 'highlighted': index === highlightedIndexMae }">{{
                      femea.brinco }}</li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group">
              <span class="input-group-text" title="RFID do Animal"><i class="fas fa-barcode"></i></span>
              <input v-model="formData.rfid" type="text" class="form-control" id="rfid" placeholder="RFID do Animal"
                title="RFID do Animal" autocomplete="off">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Observações"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.observacoes" type="text" class="form-control" id="observacoes"
                placeholder="Observações" title="Observações" autocomplete="off">

            </div>
            <div class="mb-3 input-group">
              <input v-model="comprado" type="checkbox" id="check-comprado"> Animal Comprado
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text" title="Data da Compra"><i class="fas fa-calendar-alt"></i></span>
              <DateComponent type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                :class="{ 'is-invalid': !isDataCompraValido }" :placeholder="dataCompraPlaceholder" class="form-control"
                id="dataDaCompra" v-model="formData.dataCompra" title="Data da Compra" autocomplete="off"
                @update:selectedDate="updateDataCompra" />
            </div>
            <div v-if="comprado" class="mb-3 input-group">
              <span class="input-group-text" title="Valor da Compra"><i class="fas fa-weight"></i></span>
              <input v-model="formData.valorCompra" :class="{ 'is-invalid': !isValorCompraValido }" type="text"
                @input="aplicarValorCompraMask" class="form-control" id="valorCompra"
                :placeholder="valorCompraPlaceholder" title="Valor da Compra" autocomplete="off">
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
import LoadSpinner from './LoadSpiner.vue';
import DateComponent from './DateComponent.vue';

export default {
  mixins: [masksMixin],
  components: {
    LoadSpinner,
    DateComponent,
  },

  name: 'TelaAnimais',
  data() {
    return {
      activeTab: 'edicao',
      animaisDaApi: [],
      racas: [],
      racasFiltradas: [],
      nomeRaca: '',
      piquetes: [],
      piquetesFiltrados: [],
      nomePiquete: '',
      machos: [],
      femeas: [],
      femeasFiltradas: [],
      machosFiltrados: [],
      comprado: false,
      highlightedIndexPiquete: -1,
      dropdownPiqueteOpen: false,
      highlightedIndexRaca: -1,
      dropdownRacaOpen: false,
      highlightedIndexPai: -1,
      dropdownPaiOpen: false,
      highlightedIndexMae: -1,
      dropdownMaeOpen: false,
      loadingSubmit: false,
      loadingInicialAnimalId: true,
      loadingInicialAnimais: true,
      loadingInicialPiquetes: true,
      loadingInicialRacas: true,
      formData: {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: null,
        racaObservacao: null,
        piquete: '',
        brincoPai: null,
        brincoMae: null,
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
      isDataCompraValido: true,
      isValorCompraValido: true,
      piquetePlaceholder: 'Piquete*',
      brincoPlaceholder: 'Brinco*',
      dataNascimentoPlaceholder: 'Data de nascimento*',
      sexoPlaceholder: 'Sexo*',
      dataCompraPlaceholder: 'Data de compra*',
      valorCompraPlaceholder: 'Valor da compra*',
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
    this.preencheListas();
    document.addEventListener('click', this.handleClickOutsidePiquete);
    document.addEventListener('click', this.handleClickOutsideRaca);
    document.addEventListener('click', this.handleClickOutsidePai);
    document.addEventListener('click', this.handleClickOutsideMae);
  },

  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(event) {
      const value = event.target.value;
      this.formData.brinco = this.brincoMask(value);
    },

    aplicarValorCompraMask(event) {
      const value = event.target.value;
      this.formData.valorCompra = this.valorMask(value);
    },

    aplicarBrincoPaiMask(value) {
      this.formData.brincoPai = this.brincoMask(value);
    },

    aplicarBrincoMaeMask(value) {
      this.formData.brincoMae = this.brincoMask(value);
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
        if (this.formData.racaPredominante != null) {
          this.formData.racaPredominante = animais[0].racaPredominante.id;
          this.nomeRaca = animais[0].racaPredominante.nome;
        }
        if (animais[0].brincoPai != null) {
          this.formData.brincoPai = animais[0].brincoPai;
        }
        if (animais[0].brincoMae != null) {
          this.formData.brincoMae = animais[0].brincoMae;
        }
        this.nomePiquete = animais[0].piquete.nome;
        this.formData.racaObservacao = animais[0].racaObservacao;
        this.formData.rfid = animais[0].rfid;
        this.formData.observacoes = animais[0].observacoes;
        this.formData.dataCompra = animais[0].dataCompra;
        this.formData.valorCompra = this.replacePontoVirgula(animais[0].valorCompra);

        if (this.formData.dataCompra) {
          this.comprado = true;
        }

        this.loadingInicialAnimalId = false;

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
        this.loadingInicialPiquetes = false;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/', {
        });
        this.racas = response.data;
        this.loadingInicialRacas = false;
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
        this.loadingInicialAnimais = false;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        console.log('formData: ', this.formData);
        this.loadingSubmit = true;
        try {
          //FORMATA VALOR COMPRA
          this.formData.valorCompra = this.replaceVirgulaPonto(this.formData.valorCompra);

          const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData, {
          });
          if (response.status === 200) {
            this.loadingSubmit = false;

            setTimeout(() => {
              alert('Alterações salvas com sucesso!');
              this.selectTab('visualizacao');
            }, 100);
          } else {
            this.loadingSubmit = false;
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          this.loadingSubmit = false;
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


    //LÓGICA DOS SELECT PIQUETE ----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetes() {
      this.piquetesFiltrados = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.nomePiquete.toLowerCase()));
    },

    async selectPiquete(piquete) {
      this.nomePiquete = piquete.nome;
      this.formData.piquete = piquete.id;
      this.piquetesFiltrados = [];
      this.dropdownPiqueteOpen = false;
      this.highlightedIndexPiquete = -1; // Reseta o índice após a seleção
    },

    toggleDropdownPiquete() {
      this.dropdownPiqueteOpen = !this.dropdownPiqueteOpen;
      let nomeCorreto = false;

      if (!this.dropdownPiqueteOpen) {
        this.piquetesFiltrados.forEach(piquete => {
          if (piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()) {
            this.selectPiquete(piquete);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiquete = '';
          this.formData.piquete = null;
        }
      }
      else if (this.dropdownRacaOpen) {
        this.racas.forEach(raca => {
          if (raca.nome.toLowerCase() === this.nomeRaca.toLowerCase()) {
            this.selectRaca(raca);
            nomeCorreto = true;

          }
        });
        if (!nomeCorreto) {
          this.formData.racaPredominante = null;
          this.nomeRaca = ''
        }
        this.dropdownRacaOpen = false;
        this.filterPiquetes();
      }

      else if (this.dropdownPaiOpen) {
        this.dropdownPaiOpen = false;
        this.filterPiquetes();
      }

      else if (this.dropdownMaeOpen) {
        this.dropdownMaeOpen = false;
        this.filterPiquetes();
      }
      else {
        this.filterPiquetes();
      }
    },

    handleClickOutsidePiquete(event) {
      let nomeCorreto = false;
      if (this.dropdownPiqueteOpen && this.$refs.dropdownPiquete && !this.$refs.dropdownPiquete.contains(event.target)) {
        this.piquetes.forEach(piquete => {
          if (piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()) {
            this.selectPiquete(piquete);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiquete = '';
          this.formData.piquete = null;
        }
      }
      this.dropdownPiqueteOpen = false;
    },

    inputPiquete() {
      this.filterPiquetes();
      this.dropdownPiqueteOpen = true;
      this.highlightedIndexPiquete = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsPiquete(direction) {
      if (direction === 'up' && this.highlightedIndexPiquete > 0) {
        this.highlightedIndexPiquete--;
      } else if (direction === 'down' && this.highlightedIndexPiquete < this.piquetesFiltrados.length - 1) {
        this.highlightedIndexPiquete++;
      }
    },

    selectHighlightedPiquete() {
      if (this.highlightedIndexPiquete >= 0 && this.highlightedIndexPiquete < this.piquetesFiltrados.length) {
        this.selectPiquete(this.piquetesFiltrados[this.highlightedIndexPiquete]);
      }
    },


    //LÓGICA DOS SELECT RACA ----------------------------------------------------------------------------------------------------------------------------------------------------
    filterRacas() {
      this.racasFiltradas = this.racas.filter(raca => raca.nome.toLowerCase().includes(this.nomeRaca.toLowerCase()));
    },

    async selectRaca(raca) {
      this.nomeRaca = raca.nome;
      this.formData.racaPredominante = raca.id;
      this.racasFiltradas = [];
      this.dropdownRacaOpen = false;
      this.highlightedIndexRaca = -1; // Reseta o índice após a seleção
    },

    toggleDropdownRaca() {
      this.dropdownRacaOpen = !this.dropdownRacaOpen;
      let nomeCorreto = false;

      if (!this.dropdownRacaOpen) {
        this.racasFiltradas.forEach(raca => {
          if (raca.nome.toLowerCase() === this.nomeRaca.toLowerCase()) {
            this.selectRaca(raca);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomeRaca = '';
          this.formData.racaPredominante = null;
        }
      }
      else if (this.dropdownPiqueteOpen) {
        this.piquetes.forEach(piquete => {
          if (piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()) {
            this.formData.piquete = piquete.id;
            this.piquetesFiltrados = [];
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.piquete = null;
          this.nomePiquete = ''
        }
        this.dropdownPiqueteOpen = false;
        this.filterRacas();
      }

      else if (this.dropdownPaiOpen) {
        this.dropdownPaiOpen = false;
        this.filterRacas();
      }

      else if (this.dropdownMaeOpen) {
        this.dropdownMaeOpen = false;
        this.filterRacas();
      }
      else {
        this.filterRacas();
      }
    },

    handleClickOutsideRaca(event) {
      let nomeCorreto = false;
      if (this.dropdownRacaOpen && this.$refs.dropdownRaca && !this.$refs.dropdownRaca.contains(event.target)) {
        this.racas.forEach(raca => {
          if (raca.nome.toLowerCase() === this.nomeRaca.toLowerCase()) {
            this.selectRaca(raca);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomeRaca = '';
          this.formData.racaPredominante = null;
        }
      }
      this.dropdownRacaOpen = false;
    },

    inputRaca() {
      this.filterRacas();
      this.dropdownRacaOpen = true;
      this.highlightedIndexRaca = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsRaca(direction) {
      if (direction === 'up' && this.highlightedIndexRaca > 0) {
        this.highlightedIndexRaca--;
      } else if (direction === 'down' && this.highlightedIndexRaca < this.racasFiltradas.length - 1) {
        this.highlightedIndexRaca++;
      }
    },

    selectHighlightedRaca() {
      if (this.highlightedIndexRaca >= 0 && this.highlightedIndexRaca < this.racasFiltradas.length) {
        this.selectRaca(this.racasFiltradas[this.highlightedIndexRaca]);
      }
    },


    //LÓGICA DOS SELECT PAI----------------------------------------------------------------------------------------------------------------------------------------------------
    filterMachos() {
      this.machosFiltrados = this.machos.filter(macho => macho.brinco.includes(this.formData.brincoPai));
    },

    selectPai(macho) {
      this.formData.brincoPai = macho.brinco;
      this.machosFiltrados = [];
      this.dropdownPaiOpen = false;
      this.highlightedIndexPai = -1; // Reseta o índice após a seleção
    },

    toggleDropdownPai() {
      this.dropdownPaiOpen = !this.dropdownPaiOpen;
      let nomeCorreto = false;

      if (this.dropdownPiqueteOpen) {
        this.piquetes.forEach(piquete => {
          if (piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()) {
            this.formData.piquete = piquete.id;
            this.piquetesFiltrados = [];
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.piquete = null;
          this.nomePiquete = ''
        }
        this.dropdownPiqueteOpen = false;
        this.filterMachos();
      }

      else if (this.dropdownRacaOpen) {
        this.racas.forEach(raca => {
          if (raca.nome.toLowerCase() === this.nomeRaca.toLowerCase()) {
            this.selectRaca(raca);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.racaPredominante = null;
          this.nomeRaca = ''
        }
        this.dropdownRacaOpen = false;
        this.filterMachos();
      }

      else if (this.dropdownMaeOpen) {
        this.dropdownMaeOpen = false;
        this.filterMachos();
      }

      else {
        this.filterMachos();
      }
    },

    handleClickOutsidePai() {
      this.dropdownPaiOpen = false;
    },

    inputPai(event) {
      const value = event.target.value;
      this.aplicarBrincoPaiMask(value);
      this.filterMachos();
      this.dropdownPaiOpen = true;
      this.highlightedIndexPai = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsPai(direction) {
      if (direction === 'up' && this.highlightedIndexPai > 0) {
        this.highlightedIndexPai--;
      } else if (direction === 'down' && this.highlightedIndexPai < this.machosFiltrados.length - 1) {
        this.highlightedIndexPai++;
      }
    },

    selectHighlightedPai() {
      if (this.highlightedIndexPai >= 0 && this.highlightedIndexPai < this.machosFiltrados.length) {
        this.selectPai(this.machosFiltrados[this.highlightedIndexPai]);
      }
    },



    //LÓGICA DOS SELECT MAE----------------------------------------------------------------------------------------------------------------------------------------------------
    filterFemeas() {
      this.femeasFiltradas = this.femeas.filter(femea => femea.brinco.includes(this.formData.brincoMae));
    },

    selectMae(femea) {
      this.formData.brincoMae = femea.brinco;
      this.femeasFiltradas = [];
      this.dropdownMaeOpen = false;
      this.highlightedIndexMae = -1; // Reseta o índice após a seleção
    },

    toggleDropdownMae() {
      this.dropdownMaeOpen = !this.dropdownMaeOpen;
      let nomeCorreto = false;

      if (this.dropdownPiqueteOpen) {
        this.piquetes.forEach(piquete => {
          if (piquete.nome.toLowerCase() === this.nomePiquete.toLowerCase()) {
            this.formData.piquete = piquete.id;
            this.piquetesFiltrados = [];
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.piquete = null;
          this.nomePiquete = ''
        }
        this.dropdownPiqueteOpen = false;
        this.filterFemeas();
      }

      else if (this.dropdownRacaOpen) {
        this.racas.forEach(raca => {
          if (raca.nome.toLowerCase() === this.nomeRaca.toLowerCase()) {
            this.selectRaca(raca);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.racaPredominante = null;
          this.nomeRaca = ''
        }
        this.dropdownRacaOpen = false;
        this.filterFemeas();
      }

      else if (this.dropdownPaiOpen) {
        this.dropdownPaiOpen = false;
        this.filterFemeas();
      }

      else {
        this.filterFemeas();
      }
    },

    handleClickOutsideMae() {
      this.dropdownMaeOpen = false;
    },

    inputMae(event) {
      const value = event.target.value;
      this.aplicarBrincoMaeMask(value);
      this.filterFemeas();
      this.dropdownMaeOpen = true;
      this.highlightedIndexMae = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsMae(direction) {
      if (direction === 'up' && this.highlightedIndexMae > 0) {
        this.highlightedIndexMae--;
      } else if (direction === 'down' && this.highlightedIndexMae < this.femeasFiltradas.length - 1) {
        this.highlightedIndexMae++;
      }
    },

    selectHighlightedMae() {
      if (this.highlightedIndexMae >= 0 && this.highlightedIndexMae < this.femeasFiltradas.length) {
        this.selectMae(this.femeasFiltradas[this.highlightedIndexMae]);
      }
    },



    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      let valido = true;
      this.isBrincoValido = true;
      this.brincoPlaceholder = 'Brinco do Animal*';

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

    verificaVazio() {
      //PIQUETE
      if (this.formData.piquete == null || this.formData.piquete == '') {
        this.isPiqueteValido = false
        this.piquetePlaceholder = "Piquete é um Campo Obrigatório"
      }
      else {
        this.isPiqueteValido = true
        this.piquetePlaceholder = "Piquete*"
      }

      //BRINCO
      if (this.formData.brinco != null) {
        if (this.formData.brinco == '') {
          this.isBrincoValido = false
          this.brincoPlaceholder = 'Brinco do Animal é um Campo Obrigatório'
        }
        else {
          this.isBrincoValido = true
          this.brincoPlaceholder = 'Brinco do Animal*'
        }
      }
      else {
        this.isBrincoValido = false
        this.brincoPlaceholder = 'Brinco do Animal é um Campo Obrigatório'
      }

      //DATA DE NASCIMENTO
      if (this.formData.dataNascimento != null) {
        if (this.formData.dataNascimento.trim == '') {
          this.isDataNascimentoValido = false
          this.dataNascimentoPlaceholder = 'Data de nascimento é um Campo Obrigatório'
        }
        else {
          this.isDataNascimentoValido = true
          this.dataNascimentoPlaceholder = 'Data de nascimento*'
        }
      }
      else {
        this.isDataNascimentoValido = false
        this.dataNascimentoPlaceholder = 'Data de nascimento é um Campo Obrigatório'
      }

      //SEXO
      if (this.formData.sexo == null) {
        this.isSexoValido = false
        this.sexoPlaceholder = 'Sexo é um Campo Obrigatório'
      }
      else {
        this.isSexoValido = true
        this.sexoPlaceholder = 'Sexo*'
      }

      //COMPRADO
      if (this.comprado) {
        //DATA DA COMPRA
        if (this.formData.dataCompra != null) {
          if (this.formData.dataCompra.trim == '') {
            this.isDataCompraValido = false;
            this.dataCompraPlaceholder = 'Data da compra é um Campo Obrigatório'
          }
          else {
            this.isDataCompraValido = true;
            this.dataCompraPlaceholder = 'Data da Compra*'
          }
        }
        else {
          this.isDataCompraValido = false;
          this.dataCompraPlaceholder = 'Data da compra é um Campo Obrigatório'
        }

        //VALOR DA COMPRA
        if (this.formData.valorCompra != null) {
          if (this.formData.valorCompra.trim == '') {
            this.isValorCompraValido = false;
            this.valorCompraPlaceholder = 'Valor da compra é um Campo Obrigatório'
          }
          else {
            this.isValorCompraValido = true;
            this.dataCompraPlaceholder = 'Valor da compra*'
          }
        }
        else {
          this.isValorCompraValido = false;
          this.valorCompraPlaceholder = 'Valor da compra é um Campo Obrigatório'
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
    updateDataNascimento(data) {
      this.formData.dataNascimento = data;
    },

    updateDataCompra(data) {
      this.formData.dataCompra = data;
    },
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
      this.femeas = response.data;
    },

    async preencherListaMachos() {
      const response = await api.get(`http://127.0.0.1:8000/animais/machos`, {
        params: {
          propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
        },
      });
      this.machos = response.data;
    },

    replacePontoVirgula(valorString) {
      if (valorString) {
        valorString = valorString.replace(".", ",");
      }
      return valorString;
    },

    replaceVirgulaPonto(valorString) {
      if (valorString) {
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

#legenda {
  font-size: 16px;
}

.select-option {
  width: 100%;
  cursor: pointer;
}

.itens {
  position: absolute;
  background-color: #fff;
  color: #000;
  border: 1px solid #ccc;
  border-radius: 7px;
  width: 100%;
  margin-top: 40px;
  z-index: 999;
  padding: 20px;
}

.options {
  max-height: 200px;
  /* Ajuste a altura conforme necessário */
  overflow-y: auto;
  border: 1px solid #ddd;
  margin: 0;
  padding: 0;
  list-style: none;
}

.options li {
  padding: 10px;
  cursor: pointer;
}

.options li:hover {
  background-color: #f0f0f0;
}

.highlighted {
  background-color: #f0f0f0;
}
</style>
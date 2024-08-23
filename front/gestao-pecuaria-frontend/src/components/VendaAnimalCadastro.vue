<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'vendas' }" id="nav-vet-tab" @click="selectTab('vendas')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Venda</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Venda</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'vendas' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Venda</h1>
            <form @submit.prevent="submitForm" @keydown="checkEnter">
              <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text" title="Data da Venda"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder" 
                    class="form-control" id="dataVenda" v-model="formData.dataVenda" 
                    :class="{'is-invalid': !isDataValida}" title="Data da Venda">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text" title="Preço por kg"><i class="fas fa-dollar-sign"></i></span>
                  <input ref="valor" @input="inputPrecoKg" v-model="formData.precoKg" 
                  type="text" class="form-control" id="precoKg" :placeholder="precoKgPlaceholder" title="Preço por kg">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text" title="Finalidade da Venda"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.finalidade" class="form-select" id="finalidade" aria-label="Finalidade"
                    :placeholder="finalidadePlaceholder" :class="{'is-invalid': !isFinalidadeValida}" title="Finalidade da Venda">
                    <option disabled value="">Finalidade</option>
                    <option value="Cria">Cria</option>
                    <option value="Recria">Recria</option>
                    <option value="Engorda">Engorda</option>
                    <option value="Abate">Abate</option>
                </select>
                </div>

                <div ref="dropdown" class="select mb-3 input-group" @keydown.up.prevent="navigateOptions('up')"
              @keydown.down.prevent="navigateOptions('down')" @keydown.enter.prevent="selectHighlightedAnimal">
              <div class="select-option mb-3 input-group" @click.stop="toggleDropdown">
                <span class="input-group-text" title="Brinco do Animal"><i class="fas fa-user-tag"></i></span>
                <input v-model="brinco" :class="{ 'is-invalid': !isBrincoValido }" @input="inputBrinco"
                  @keydown.up.prevent="navigateOptions('up')"
                  @keydown.down.prevent="navigateOptions('down')" type="text" class="form-control"
                  :placeholder="brincoPlaceholder" id="caixa-select" title="Brinco do Animal">
              </div>
              <div class="itens" v-show="dropdownOpen">
                <ul class="options">
                  <li v-for="(animal, index) in animaisFiltrados" :key="animal.id" :value="animal.id"
                    @click="selectAnimal(animal)" :class="{ 'highlighted': index === highlightedIndex }">{{
                    animal.brinco }}</li>
                </ul>
              </div>
            </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text" title="Peso do Animal"><i class="fas fa-weight-hanging"></i></span>
                  <input @input="inputPeso" v-model="formData.peso" type="text" class="form-control" id="peso" 
                  :placeholder="pesoPlaceholder" title="Peso do Animal">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text" title="Valor Total da Venda"><i class="fas fa-dollar-sign"></i></span>
                  <input ref="valor" v-model="formData.valorTotal" type="text" class="form-control"  @input="aplicarValorTotalMask"
                  id="valorTotal" :class="{'is-invalid': !isValorTotalValido}" :placeholder="valorTotalPlaceholder" title="Valor Total da Venda">
                </div>
                <div class="mb-3 input-group position-relative">
                  <span class="input-group-text" title="Observação da Venda"><i class="fas fa-sticky-note"></i></span>
                  <input v-model="formData.observacao" type="text" class="form-control" id="observacao"
                  placeholder="Observação" title="Observação da Venda" />
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('vendas')">Cancelar</button>
                    <button type="button" class="btn btn-success" @click="submitForm">Enviar</button>
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
      brinco: '',
      highlightedIndex: -1,
      dropdownOpen: false,
      formData: {
        id: null,
        animal: '',
        dataVenda: '',
        peso: null,
        precoKg: null,
        valorTotal: null,
        finalidade: '',
        observacao: null,
      },
      isBrincoValido: true,
      isDataValida: true,
      isValorTotalValido: true,
      isFinalidadeValida: true,
      brincoPlaceholder: 'Brinco do animal*',
      dataPlaceholder: 'Data da venda*',
      pesoPlaceholder: 'Peso do animal',
      precoKgPlaceholder: 'Preço por KG',
      valorTotalPlaceholder: 'Valor Total*',
      finalidadePlaceholder: 'Finalidade*',
    };
  },

    mounted() {
    this.buscarAnimaisDaApi();
    document.addEventListener('click', this.handleClickOutside);
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarValorTotalMask(event) {
      const value = event.target.value;
      this.formData.valorTotal =  this.valorMask(value);
    },

    aplicarValorTotalMask2(value){
      this.formData.valorTotal = this.valorMask(value);
    },

    aplicarPesoMask(value) {
      this.formData.peso =  this.valorMask(value);
    },

    aplicarPrecoKgMask(value) {
      this.formData.precoKg =  this.valorMask(value);
    },

    aplicarBrincoMask(value){
      this.brinco =  this.brincoFiltroMask(value);
    },

    inputPeso(event){
      const value = event.target.value;
      this.aplicarPesoMask(value);
      this.atualizaValorTotalPeloPeso();
    },

    inputPrecoKg(event){
      const value = event.target.value;
      this.aplicarPrecoKgMask(value);
      this.atualizaValorTotalPeloPrecoKg();
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarAnimaisDaApi() {
        try {
            const response = await api.get('http://127.0.0.1:8000/animais/vivos' , {
            params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
            });
            this.animais = response.data;
        } catch (error) {
            console.error('Erro ao buscar animais da API:', error);
        }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        try {
          //FORMATA PESO, PRECOKG E VALORTOTAL
          if(this.formData.peso != null){
            this.formData.peso = this.replaceVirgulaPonto(this.formData.peso);
          }
          if(this.formData.precoKg != null){
            this.formData.precoKg = this.replaceVirgulaPonto(this.formData.precoKg);
          }
          this.formData.valorTotal = this.replaceVirgulaPonto(this.formData.valorTotal);

          const response = await api.post('http://127.0.0.1:8000/vendas-animais/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/vendas-animais');
          } else {
            alert('Erro ao cadastrar venda. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
    },


//LÓGICA DOS SELECTS----------------------------------------------------------------------------------------------------------------------------------------------------
    filterAnimais() {
        this.animaisFiltrados = this.animais.filter(animal => animal.brinco.includes(this.brinco));
    },

    selectAnimal(animal) {
        this.brinco = animal.brinco;
        this.formData.animal = animal.id;
        this.animaisFiltrados = [];
        this.dropdownOpen = false;
    },

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
      let nomeCorreto = false;

      if(!this.dropdownOpen){
        this.animaisFiltrados.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.brinco = '';
        }
      }
      else{
        this.filterAnimais();
      }
    },

    handleClickOutside(event) {
      if (this.dropdownOpen && this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.dropdownOpen = false;
      }
      let nomeCorreto = false;
      if(!this.dropdownOpen){
        this.animais.forEach(animal => {
          if(animal.brinco === this.brinco){
            this.brinco = animal.brinco;
            this.formData.animal = animal.id;
            this.animaisFiltrados = [];
            nomeCorreto = true;
          }
        });
        if(!nomeCorreto){
          this.brinco = '';
        }
      }
    },

    inputBrinco(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
      this.dropdownOpen = true;
    },

    navigateOptions(direction) {
      if (direction === 'up' && this.highlightedIndex > 0) {
        this.highlightedIndex--;
      } else if (direction === 'down' && this.highlightedIndex < this.animaisFiltrados.length - 1) {
        this.highlightedIndex++;
      }
    },

    selectHighlightedAnimal() {
      if (this.highlightedIndex >= 0 && this.highlightedIndex < this.animaisFiltrados.length) {
        this.selectAnimal(this.animaisFiltrados[this.highlightedIndex]);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DA VENDA
      if(this.formData.dataVenda != null && this.formData.dataVenda.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Data da Venda*';
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Venda é um Campo Obrigatório';
      }
      
      //PREÇO POR KG
      if(this.formData.precoKg != null && this.formData.precoKg.trim() == ''){
          this.formData.precoKg = null;
      }

      //FINALIDADE
      if(this.formData.finalidade != null && this.formData.finalidade.trim() != ''){
          this.isFinalidadeValida = true;
          this.finalidadePlaceholder = 'Finalidade*';
      }
      else{
        this.isFinalidadeValida = false;
        this.finalidadePlaceholder = 'Finalidade é um Campo Obrigatório';
      }

      //BRINCO DO ANIMAL
      if(this.brinco != null && this.brinco.trim() != ''){
          this.isBrincoValido = true;
          this.brincoPlaceholder = 'Brinco do Animal*';
      }
      else{
        this.isBrincoValido = false;
        this.brincoPlaceholder = 'Brinco do Animal é um Campo Obrigatório';
      }

      //PESO DO ANIMAL
      if(this.formData.peso != null && this.formData.peso.trim() == ''){
          this.formData.peso = null;
      }

      //VALOR TOTAL
      if(this.formData.valorTotal != null && this.formData.valorTotal != ''){
          this.isValorTotalValido = true;
          this.valorTotalPlaceholder = 'Valor Total*';
      }
      else{
        this.isValorTotalValido = false;
        this.valorTotalPlaceholder = 'Valor Total é um Campo Obrigatório';
      }

      //OBSERVAÇÕES
      if(this.formData.observacao != null && this.formData.observacao.trim() === ''){
        this.formData.observacao = null;
      } 

      return (
        this.isDataValida &&
        this.isFinalidadeValida &&
        this.isBrincoValido &&
        this.isValorTotalValido
      );
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
atualizaValorTotalPeloPeso(){
      if(this.formData.precoKg != null && this.formData.precoKg != ''){
        this.formData.valorTotal = parseFloat(this.replaceVirgulaPonto(this.formData.precoKg.toString())) * 
        parseFloat(this.replaceVirgulaPonto(this.formData.peso.toString()));
        this.ChamaMaskValorTotal();
      }
    },

    atualizaValorTotalPeloPrecoKg(){
      if(this.formData.peso != null && this.formData.peso != ''){
        this.formData.valorTotal = parseFloat(this.replaceVirgulaPonto(this.formData.precoKg.toString())) * 
        parseFloat(this.replaceVirgulaPonto(this.formData.peso.toString()));  
        this.ChamaMaskValorTotal();      
      }
    },

    ChamaMaskValorTotal(){
      let valorTotal = this.formData.valorTotal.toString();
      const temPonto = valorTotal.includes('.')
      if(temPonto){
        const regex = /^\d.\d+$/
        if(regex.test(valorTotal)){
          valorTotal = valorTotal.replace(/^(\d).(\d{2})\d+$/ , '0$1.$2');
        }
        const regex2 = /^\d+.\d$/
        if(regex2.test(valorTotal)){
          valorTotal = valorTotal.replace(/^(\d+).(d)/ , '$1.$20');
        }

        const regex3 = /^\d+.\d{2}\d+/
        if(regex3.test(valorTotal)){
          valorTotal = valorTotal.replace(/^(\d+).(d{2})\d+/ , '$1.$2');
        }

        valorTotal = this.replacePontoVirgula(valorTotal);
      }
      else{
        valorTotal = valorTotal + ',00'
      }

      this.aplicarValorTotalMask2(valorTotal)
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'vendas') {
        this.$router.push('/vendas-animais');
      }
    },

    replacePontoVirgula(valorString){
      if(valorString != null){
        valorString = valorString.replace(".", ",");
      }

      return valorString;
    },

    replaceVirgulaPonto(valorString){
      if(valorString != null){
        valorString = valorString.replace(",", ".");
      }
      return valorString;
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
</style>

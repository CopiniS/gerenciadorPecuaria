<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'vendas' }" id="nav-vet-tab" @click="selectTab('vendas')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Venda</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab" @click="selectTab('edicao')" 
        type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição de Venda</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'vendas' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel" aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Venda</h1>
            <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" :placeholder="dataPlaceholder" 
                    class="form-control" id="dataVenda" v-model="formData.dataVenda" :class="{'is-invalid': !isDataValida}">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                  <input ref="valor" @input="inputPrecoKg" v-model="formData.precoKg" type="text" class="form-control" id="precoKg" :placeholder="precoKgPlaceholder">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.finalidade" class="form-select" id="finalidade" aria-label="Finalidade"
                    :placeholder="finalidadePlaceholder" :class="{'is-invalid': !isFinalidadeValida}" required>
                    <option disabled value="">Finalidade</option>
                    <option value="Cria">Cria</option>
                    <option value="Recria">Recria</option>
                    <option value="Engorda">Engorda</option>
                    <option value="Abate">Abate</option>
                </select>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                    <input v-model="brinco" @input="inputBrinco" type="text" class="form-control" :placeholder="brincoPlaceholder" :class="{'is-invalid': !isBrincoValido}">
                </div>
                <div class="list-group" v-if="brinco && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                    {{ animal.brinco }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-weight-hanging"></i></span>
                  <input @input="inputPeso" v-model="formData.peso" type="text" class="form-control" id="peso" :placeholder="pesoPlaceholder">
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                  <input ref="valor" v-model="formData.valorTotal" type="text" class="form-control" @input="aplicarValorTotalMask"
                  id="valorTotal" :class="{'is-invalid': !isValorTotalValido}" :placeholder="valorTotalPlaceholder" required>
                </div>
                <div class="mb-3 input-group position-relative">
                  <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                  <textarea v-model="formData.observacao" class="form-control" id="observacao"
                    @input="aplicarObservacaoMask" placeholder="Observação"></textarea>
                  <div class="character-counter">({{ contadorObservacao }} / 255)</div>
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
      activeTab: 'edicao', // Começa na aba de edição
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      dataSelecionada: null,
      formData: {
        id: null,
        animal: '',
        dataVenda: '',
        peso: null,
        precoKg: null,
        valorTotal: '',
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
    const vendaId = this.$route.params.vendaId;
    if (vendaId) {
      this.fetchVenda(vendaId);
    }
    this.buscarAnimaisDaApi();
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

    aplicarObservacaoMask(event){
      const value = event.target.value;
      this.formData.observacao = this.observacoesMask(value);
      this.contadorObservacao = this.formData.observacao.length;
    },

    aplicarPesoMask(value) {
      this.formData.peso =  this.valorMask(value);
    },

    aplicarPrecoKgMask(value) {
      this.formData.precoKg =  this.valorMask(value);
    },

    aplicarBrincoMask(value){
      this.brinco =  this.brincoMask(value);
    },

    inputBrinco(event){
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
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
    async fetchVenda(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/vendas-animais/venda/${id}`);
        const venda = response.data;
        this.formData.id = venda[0].id;
        this.formData.animal = venda[0].animal.id;
        this.formData.dataVenda = venda[0].dataVenda;
        this.formData.peso = this.replacePontoVirgula(venda[0].peso);
        this.formData.precoKg = this.replacePontoVirgula(venda[0].precoKg);
        this.formData.valorTotal = this.replacePontoVirgula(venda[0].valorTotal);
        this.formData.finalidade = venda[0].finalidade;
        this.formData.observacao = venda[0].observacao;

        this.brinco = venda[0].animal.brinco;
        this.dataSelecionada = venda[0].dataVenda;
        if(this.formData.observacao){
          this.contadorObservacao = this.formData.observacao.length;
        }
      } catch (error) {
        console.error('Erro ao carregar dados da venda:', error);
      }
    },

    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/vivos', {
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

          const response = await api.patch(`http://127.0.0.1:8000/vendas-animais/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/vendas-animais');
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
    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectAnimal(animal) {
      this.brinco = animal.brinco;
      this.formData.animal = animal.id;
      this.animaisFiltrados = [];
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
    atualizaValorTotalPeloPeso(){
      if(this.formData.precoKg != null && this.formData.precoKg != ''){
        this.formData.valorTotal = parseFloat(this.replaceVirgulaPonto(this.formData.precoKg) * 
        this.replaceVirgulaPonto(this.formData.peso));
        this.formData.valorTotal = this.replacePontoVirgula(this.formData.valorTotal.toString());
        this.ChamaMaskValorTotal();
      }
    },

    atualizaValorTotalPeloPrecoKg(){
      if(this.formData.peso != null && this.formData.peso != ''){
        this.formData.valorTotal = parseFloat(this.replaceVirgulaPonto(this.formData.precoKg) * 
        this.replaceVirgulaPonto(this.formData.peso));
        this.formData.valorTotal = this.replacePontoVirgula(this.formData.valorTotal.toString());
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

    cancelarEdicao() {
      this.$router.push('/vendas-animais');
    },

    replacePontoVirgula(valorString){
        valorString = valorString.replace(".", ",");
      return valorString;
    },

    replaceVirgulaPonto(valorString){
        valorString = valorString.replace(",", ".");
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

.position-relative {
  position: relative;
}

.character-counter {
  position: absolute;
  top: 60px;
  right: 10px;
  font-size: 12px;
  color: #6c757d;
}
</style>

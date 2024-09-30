<template>
  <div class="background">
    <LoadSpinner :isLoading="loading" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'gastos' }" id="nav-vet-tab"
          @click="selectTab('gastos')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Gastos</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Gasto</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'gastos' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Gasto</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"><i class="fas fa-calendar-alt"></i></span>
              <input :class="{ 'is-invalid': !isDataValida }" type="text" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataPlaceholder" class="form-control" id="dataGasto"
                v-model="formData.dataGasto" title="Data" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Tipo"><i class="fas fa-clipboard-list"></i></span>
              <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                @change="categoriaPlaceholder = 'Categoria*'; formData.categoria = null" :class="{'is-invalid': !isTipoValido}" 
                title="Tipo">
                <option disabled :value="null">{{ tipoPlaceholder }}</option>
                <option value="Despesa">Despesa</option>
                <option value="Investimento">Investimento</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Valor"><i class="fas fa-dollar-sign"></i></span>
              <input v-model="formData.valor" :class="{ 'is-invalid': !isValorValido }" ref="valor" type="text" autocomplete="off"
                @input="aplicarValorMask" class="form-control" id="valor" :placeholder="valorPlaceholder" title="Valor">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Descrição"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.descricao" type="text" class="form-control" id="descricao" autocomplete="off"
                :placeholder="descricaoPlaceholder" :class="{ 'is-invalid': !isDescricaoValida }" title="Descrição">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Categoria"><i class="fas fa-clipboard-list"></i></span>
              <select :disabled="formData.tipo == '' || formData.tipo == null" v-model="formData.categoria"
              class="form-select" id="categoria" aria-label="Categoria"
              :class="{'is-invalid': !isCategoriaValida}" title="Categoria">
                <option disabled :value="null">{{ categoriaPlaceholder }}</option>
                <option v-if="formData.tipo == 'Despesa'" value="mao_de_obra">Mão de Obra</option>
                <option v-if="formData.tipo == 'Despesa'" value="manutencao_maquinas">Manutenção de Máquinas</option>
                <option v-if="formData.tipo == 'Despesa'" value="manutencao_benfeitorias">Manutenção de Benfeitorias</option>
                <option v-if="formData.tipo == 'Despesa'" value="medicamentos">Medicamentos</option>
                <option v-if="formData.tipo == 'Despesa'" value="combustiveis">Combustiveis</option>
                <option v-if="formData.tipo == 'Despesa'" value="despesa_administrativa">Despesa Administrativa</option>
                <option v-if="formData.tipo == 'Despesa'" value="sementes">Sementes</option>
                <option v-if="formData.tipo == 'Despesa'" value="adubos">Adubos</option>
                <option v-if="formData.tipo == 'Despesa'" value="outros">Outros</option>
                <option v-if="formData.tipo == 'Investimento'" value="compra_maquinas">Compra de Máquinas</option>
                <option v-if="formData.tipo == 'Investimento'" value="construcao_benfeitorias">Construção de Benfeitorias</option>
                <option v-if="formData.tipo == 'Investimento'" value="implantacao_lavouras">Implantação de Lavouras</option>
                <option v-if="formData.tipo == 'Investimento'" value="aquisicao_terra">Aquisição de Terra</option>
                <option v-if="formData.tipo == 'Investimento'" value="Outros">Outros</option>
              </select>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('gastos')">Cancelar</button>
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
import LoadSpinner from './LoadSpiner.vue';

export default {
  mixins: [masksMixin],

  components: {
    LoadSpinner,
  },

  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      loading: false,
      formData: {
        id: null,
        dataGasto: null,
        tipo: null,
        valor: null,
        descricao: null,
        categoria: null,
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      isDataValida: true,
      isTipoValido: true,
      isValorValido: true,
      isDescricaoValida: true,
      isCategoriaValida: true,
      dataPlaceholder: 'Data*',
      tipoPlaceholder: 'Tipo*',
      valorPlaceholder: 'Valor*',
      descricaoPlaceholder: 'Descrição*',
      categoriaPlaceholder: 'Categoria* (Selecione o Tipo do produto antes)'
    };
  },

  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarValorMask(event){
      const value = event.target.value;
      this.formData.valor = this.valorMask(value);
    },


//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async submitForm() {
      if (this.verificaVazio()) {
        this.loading = true;
        try {
          //FORMATA VALOR
          this.formData.valor = this.replaceVirgulaPonto(this.formData.valor);
          
          const response = await api.post('http://127.0.0.1:8000/gastos/', this.formData, {});
          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/gastos');
          } else {
            alert('Erro ao cadastrar veterinário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DO GASTO
      if(this.formData.dataGasto != null){
        if(this.formData.dataGasto.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Data*';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data é um Campo Obrigatório';
      }

      //TIPO DO GASTO
      if(this.formData.tipo != null){
        if(this.formData.tipo != ''){
          this.isTipoValido = true;
          this.tipoPlaceholder = 'Tipo*';
        }
        else{
          this.isTipoValido = false;
          this.tipoPlaceholder = 'Tipo é um Campo Obrigatório'
        }
      }
      else{
        this.isTipoValido = false;
        this.tipoPlaceholder = 'Tipo é um Campo Obrigatório'
      }

      //VALOR
      if(this.formData.valor != null){
        if(this.formData.valor.trim() != ''){
          this.isValorValido = true;
          this.valorPlaceholder = 'Valor*';
        }
        else{
          this.isValorValido = false;
          this.valorPlaceholder = 'Valor é um Campo Obrigatório';
        }
      }
      else{
        this.isValorValido = false;
        this.valorPlaceholder = 'Valor é um Campo Obrigatório';
      }

      //DESCRIÇÃO
      if(this.formData.descricao != null){
        if(this.formData.descricao.trim() != ''){
          this.isDescricaoValida = true;
          this.descricaoPlaceholder = 'Descrição*';
        }
        else{
          this.isDescricaoValida = false;
          this.descricaoPlaceholder = 'Descrição é um Campo Obrigatório';
        }
      }
      else{
        this.isDescricaoValida = false;
        this.descricaoPlaceholder = 'Descrição é um Campo Obrigatório';
      }

      //CATEGORIA
      if(this.formData.categoria != null){
        if(this.formData.categoria.trim() != ''){
          this.isCategoriaValida = true;
          this.categoriaPlaceholder = 'Categoria*';
        }
        else{
          this.isCategoriaValida = false;
          this.categoriaPlaceholder = 'Categoria é um Campo Obrigatório';
        }
      }
      else{
        this.isCategoriaValida = false;
        this.categoriaPlaceholder = 'Categoria é um Campo Obrigatório';
      }
      return (
        this.isDataValida &&
        this.isTipoValido &&
        this.isValorValido &&
        this.isDescricaoValida &&
        this.isCategoriaValida
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
      if (tab === 'gastos') {
        this.$router.push('/gastos');
      }
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

#legenda {
    font-size: 16px;
}

</style>

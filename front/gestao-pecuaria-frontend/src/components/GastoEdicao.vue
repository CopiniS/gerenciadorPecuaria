<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'gastos' }" id="nav-vet-tab"
          @click="selectTab('gastos')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Gastos</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Gasto</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'gastos' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Gasto</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data do Gasto"><i class="fas fa-calendar-alt"></i></span>
              <input :class="{ 'is-invalid': !isDataValida }" type="text" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataPlaceholder" class="form-control" id="dataGasto"
                v-model="formData.dataGasto" title="Data do Gasto">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Tipo do Gasto"><i class="fas fa-clipboard-list"></i></span>
              <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                @change="categoriaPlaceholder = 'Categoria*'; formData.categoria = null" :class="{'is-invalid': !isTipoValido}" 
                title="Categoria do Gasto">
                <option disabled :value="null">{{ tipoPlaceholder }}</option>
                <option value="despesa">Despesa</option>
                <option value="investimento">Investimento</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Valor da Gasto"><i class="fas fa-dollar-sign"></i></span>
              <input v-model="formData.valor" :class="{ 'is-invalid': !isValorValido }" ref="valor" type="text"
                @input="aplicarValorMask" class="form-control" id="valor" :placeholder="valorPlaceholder" title="Valor da Gasto">
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Descrição da Gasto "><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.descricao" type="text" class="form-control" id="descricao"
                :placeholder="descricaoPlaceholder" :class="{ 'is-invalid': !isDescricaoValida }" title="Descrição da Gasto">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Categoria do Gasto"><i class="fas fa-clipboard-list"></i></span>
              <select :disabled="formData.tipo == '' || formData.tipo == null" v-model="formData.categoria"
              class="form-select" id="categoria" aria-label="Categoria"
              :class="{'is-invalid': !isCategoriaValida}" title="Categoria do Gasto">
                <option disabled :value="null">{{ categoriaPlaceholder }}</option>
                <option v-if="formData.tipo == 'despesa'" value="mao_de_obra">Mão de Obra</option>
                <option v-if="formData.tipo == 'despesa'" value="manutencao_maquinas">Manutenção de Máquinas</option>
                <option v-if="formData.tipo == 'despesa'" value="manutencao_benfeitorias">Manutenção de Benfeitorias</option>
                <option v-if="formData.tipo == 'despesa'" value="medicamentos">Medicamentos</option>
                <option v-if="formData.tipo == 'despesa'" value="combustiveis">Combustiveis</option>
                <option v-if="formData.tipo == 'despesa'" value="despesa_administrativa">Despesa Administrativa</option>
                <option v-if="formData.tipo == 'despesa'" value="sementes">Sementes</option>
                <option v-if="formData.tipo == 'despesa'" value="adubos">Adubos</option>
                <option v-if="formData.tipo == 'despesa'" value="outros">Outros</option>
                <option v-if="formData.tipo == 'investimento'" value="compra_maquinas">Compra de Máquinas</option>
                <option v-if="formData.tipo == 'investimento'" value="construcao_benfeitorias">Construção de Benfeitorias</option>
                <option v-if="formData.tipo == 'investimento'" value="implantacao_lavouras">Implantação de Lavouras</option>
                <option v-if="formData.tipo == 'investimento'" value="aquisicao_terra">Aquisição de Terra</option>
                <option v-if="formData.tipo == 'investimento'" value="Outros">Outros</option>
              </select>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('gastos')">Cancelar</button>
              <button type="button" class="btn btn-success" @click="submitForm">Salvar</button>
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
      dataPlaceholder: 'Data da Gasto*',
      tipoPlaceholder: 'Tipo*',
      valorPlaceholder: 'Valor*',
      descricaoPlaceholder: 'Descrição*',
      categoriaPlaceholder: 'Categoria* (Selecione o Tipo do produto antes)'
    };
  },

  mounted() {
    const gastoId = this.$route.params.gastoId;
    if (gastoId) {
      this.fetchGasto(gastoId);
    }
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarValorMask(event){
      const value = event.target.value;
      this.formData.valor = this.valorMask(value);
    },
    
    
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
   async fetchGasto(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/gastos/${id}`);
        const gasto = response.data;
        this.formData.id = gasto.id;
        this.formData.dataGasto = gasto.dataGasto;
        this.formData.tipo = gasto.tipo;
        this.formData.valor = this.replacePontoVirgula(gasto.valor);
        this.formData.descricao = gasto.descricao;
        this.formData.categoria = gasto.categoria;
      } catch (error) {
        console.error('Erro ao carregar dados da gasto:', error);
      }
    },
    
    async submitForm() {
      if (this.verificaVazio()) {
        try {
          //FORMATA VALOR
          this.formData.valor = this.replaceVirgulaPonto(this.formData.valor);

          const response = await api.patch(`http://127.0.0.1:8000/gastos/${this.formData.id}/`, this.formData, {});
          if (response.status === 200) {
            alert('Gasto atualizada com sucesso!');
            this.$router.push('/gastos');
          } else {
            alert('Erro ao atualizar Gasto. Tente novamente mais tarde.');
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
          this.dataPlaceholder = 'Data da Gasto';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Gasto é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Gasto é um Campo Obrigatório';
      }

      //TIPO DO GASTO
      if(this.formData.tipo != null){
        if(this.formData.tipo != ''){
          this.isTipoValido = true;
          this.tipoPlaceholder = 'Tipo do Gasto';
        }
        else{
          this.isTipoValido = false;
          this.tipoPlaceholder = 'Tipo do Gasto é um Campo Obrigatório'
        }
      }
      else{
        this.isTipoValido = false;
        this.tipoPlaceholder = 'Tipo do Gasto é um Campo Obrigatório'
      }

      //VALOR
      if(this.formData.valor != null){
        if(this.formData.valor.trim() != ''){
          this.isValorValido = true;
          this.valorPlaceholder = 'Valor da Gasto';
        }
        else{
          this.isValorValido = false;
          this.valorPlaceholder = 'Valor da Gasto é um Campo Obrigatório';
        }
      }
      else{
        this.isValorValido = false;
        this.valorPlaceholder = 'Valor da Gasto é um Campo Obrigatório';
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

    cancelarEdicao() {
      this.$router.push('/gastos');
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
#legenda {
    font-size: 16px;
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
</style>

<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'despesas' }" id="nav-vet-tab"
          @click="selectTab('despesas')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Despesas</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Despesa</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'despesas' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Despesa</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar"></i></span>
              <input :class="{ 'is-invalid': !isDataValida }" type="text" onfocus="(this.type='date')"
                onblur="(this.type='text')" :placeholder="dataPlaceholder" class="form-control" id="dataDespesa"
                v-model="formData.dataDespesa" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.valor" :class="{ 'is-invalid': !isValorValido }" ref="valor" type="text"
                @input="aplicarValorMask" class="form-control" id="valor" :placeholder="valorPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.descricao" @input="aplicarDescricaoMask" type="text" class="form-control" id="descricao"
                :placeholder="descricaoPlaceholder" :class="{ 'is-invalid': !isDescricaoValida }" >
              <div>({{ contadorDescricao }} / 255)</div>   
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.categoria" type="text" class="form-control" id="categoria"
                :placeholder="categoriaPlaceholder" :class="{ 'is-invalid': !isCategoriaValida }" >
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('despesas')">Cancelar</button>
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
      contadorDescricao: 0,
      formData: {
        id: null,
        dataDespesa: '',
        valor: '',
        descricao: null,
        categoria: null,
        propriedade: localStorage.getItem('propriedadeSelecionada'),
      },
      isDataValida: true,
      isValorValido: true,
      isDescricaoValida: true,
      isCategoriaValida: true,
      dataPlaceholder: 'Data da Despesa*',
      valorPlaceholder: 'Valor*',
      descricaoPlaceholder: 'Descrição*',
      categoriaPlaceholder: 'Categoria*'
    };
  },

  mounted() {
    const despesaId = this.$route.params.despesaId;
    if (despesaId) {
      this.fetchDespesa(despesaId);
    }
  },
  methods: {
//MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarValorMask(event){
      const value = event.target.value;
      this.formData.valor = this.valorMask(value);
    },

    aplicarDescricaoMask(event){
      const value = event.target.value;
      this.formData.descricao = this.observacoesMask(value);
      this.contadorDescricao = this.formData.descricao.length;
    },
    
    
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
   async fetchDespesa(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/outras-despesas/${id}`);
        const despesa = response.data;
        this.formData.id = despesa.id;
        this.formData.dataDespesa = despesa.dataDespesa;
        this.formData.valor = this.replacePontoVirgula(despesa.valor);
        this.formData.descricao = despesa.descricao;
        this.formData.categoria = despesa.categoria;
      } catch (error) {
        console.error('Erro ao carregar dados da despesa:', error);
      }
    },
    
    async submitForm() {
      if (this.verificaVazio()) {
        try {
          //FORMATA VALOR
          this.formData.valor = this.replaceVirgulaPonto(this.formData.valor);

          const response = await api.patch(`http://127.0.0.1:8000/outras-despesas/${this.formData.id}/`, this.formData, {});
          if (response.status === 200) {
            alert('Despesa atualizada com sucesso!');
            this.$router.push('/outras-despesas');
          } else {
            alert('Erro ao atualizar Despesa. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },
    

//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //DATA DA DESPESA
      if(this.formData.dataDespesa != null){
        if(this.formData.dataDespesa.trim() != ''){
          this.isDataValida = true;
          this.dataPlaceholder = 'Data da Despesa';
        }
        else{
          this.isDataValida = false;
          this.dataPlaceholder = 'Data da Despesa é um Campo Obrigatório';
        }
      }
      else{
        this.isDataValida = false;
        this.dataPlaceholder = 'Data da Despesa é um Campo Obrigatório';
      }

      //VALOR
      if(this.formData.valor != null){
        if(this.formData.valor.trim() != ''){
          this.isValorValido = true;
          this.valorPlaceholder = 'Valor da Despesa';
        }
        else{
          this.isValorValido = false;
          this.valorPlaceholder = 'Valor da Despesa é um Campo Obrigatório';
        }
      }
      else{
        this.isValorValido = false;
        this.valorPlaceholder = 'Valor da Despesa é um Campo Obrigatório';
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
        this.isValorValido &&
        this.isDescricaoValida &&
        this.isCategoriaValida
      );
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'despesas') {
        this.$router.push('/outras-despesas');
      }
    },

    cancelarEdicao() {
      this.$router.push('/outras-despesas');
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
</style>

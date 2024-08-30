<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'produtos' }" id="nav-vet-tab"
          @click="selectTab('produtos')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de
          Produto</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab"
          @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Cadastro de Produto</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'produtos' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Produto</h1>
          <form @submit.prevent="submitForm" @keydown="checkEnter">
            <div class="mb-3 input-group">
                <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Nome"><i class="fas fa-box"></i></span>
              <input v-model="formData.nome" type="text" class="form-control" id="nome" 
              :placeholder="nomePlaceholder" :class="{'is-invalid': !isNomeValido}" title="Nome" autocomplete="off">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Tipo"><i class="fas fa-clipboard-list"></i></span>
              <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                @change="categoriaPlaceholder = 'Categoria*'; formData.categoria = ''" :class="{'is-invalid': !isTipoValido}" 
                title="Tipo">
                <option disabled value="">{{ tipoPlaceholder }}</option>
                <option value="sanitario">Sanitário</option>
                <option value="alimenticio">Alimentício</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Unidade de medida"><i class="fas fa-balance-scale"></i></span>
              <select v-model="formData.unidade" class="form-select" id="unidade" aria-label="Unidade"
                :placeholder="unidadePlaceholder" :class="{'is-invalid': !isUnidadeValida}" title="Unidade de medida">
                <option disabled value="">{{ unidadePlaceholder }}</option>
                <option value="ton">ton</option>
                <option value="kg">kg</option>
                <option value="gr">gr</option>
                <option value="lt">lt</option>
                <option value="ml">ml</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"  title="Categoria"><i class="fas fa-clipboard-list"></i></span>
              <select :disabled="formData.tipo == '' || formData.tipo == null" v-model="formData.categoria"
              class="form-select" id="categoria" aria-label="Categoria"
              :class="{'is-invalid': !isCategoriaValida}" title="Categoria">
                <option disabled value="">{{ categoriaPlaceholder }}</option>
                <option v-if="formData.tipo == 'sanitario'" value="vacinas">Vacinas</option>
                <option v-if="formData.tipo == 'sanitario'" value="vermifugos">Vermífugos</option>
                <option v-if="formData.tipo == 'sanitario'" value="vitaminas">Vitaminas</option>
                <option v-if="formData.tipo == 'sanitario'" value="antiboticos">Antibóticos</option>
                <option v-if="formData.tipo == 'sanitario'" value="antiparasitarios">Antiparasitários</option>
                <option v-if="formData.tipo == 'sanitario'" value="outros">Outros</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Sal branco">Sal branco</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Sal mineral">Sal mineral</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Sal proteinado">Sal proteinado</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Racao">Ração</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Silagem">Silagem</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Milho">Milho</option>
                <option v-if="formData.tipo == 'alimenticio'" value="Outros">Outros</option>
              </select>
            </div>
            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Descrição"><i class="fas fa-sticky-note"></i></span>
              <input v-model="formData.descricao" type="text" class="form-control" id="descricao"
                placeholder="Descrição" title="Descrição" autocomplete="off" />
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('produtos')">Cancelar</button>
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
      produtosDaApi: [],
      formData: {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
        unidade: ''
      },
      isNomeValido: true,
      isTipoValido: true,
      isCategoriaValida: true,
      isUnidadeValida: true,
      nomePlaceholder: 'Nome*',
      tipoPlaceholder: 'Tipo*',
      categoriaPlaceholder: 'Categoria* (Selecione o Tipo do produto antes)',
      unidadePlaceholder: 'Unidade de medida*'
    };
  },
  mounted() {
      this.buscarProdutosDaApi();
  },
  methods: {  
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.$router.push('/produtos');
          } else {
            alert('Erro ao cadastrar produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },  
    
    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/' , {
        });
        this.produtosDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio(){
      //NOME DO PRODUTO
      if(this.formData.nome != null){
        if(this.formData.nome.trim() != ''){
          this.isNomeValido = true;
          this.nomePlaceholder = 'Nome*';
        }
        else{
          this.isNomeValido = false;
          this.nomePlaceholder = 'Nome é um Campo Obrigatório';
        }
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome é um Campo Obrigatório';
      }

      //TIPO DO PRODUTO
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

      //DESCRIÇÃO
      if(this.formData.descricao != null && this.formData.descricao.trim() == ''){
        this.formData.descricao = null;
      }

      //CATEGORIA
      if(this.formData.categoria != null){
        if(this.formData.categoria != ''){
          this.isCategoriaValida = true;
          if(this.isTipoValido){
            this.categoriaPlaceholder = 'Categoria*';
          }
          else{
            this.categoriaPlaceholder = 'Categoria* (Selecione o Tipo do produto antes)';
          }
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


      //UNIDADE
      if(this.formData.unidade != null){
        if(this.formData.unidade != ''){
          this.isUnidadeValida = true;
          this.unidadePlaceholder = 'Unidade de medida*';
        }
        else{
          this.isUnidadeValida = false;
          this.unidadePlaceholder = 'Unidade de medida é um Campo Obrigatório';
        }
      }
      else{
        this.isUnidadeValida = false;
        this.unidadePlaceholder = 'Unidade de medida é um Campo Obrigatório';
      }

      return(
        this.isNomeValido &&
        this.isTipoValido && 
        this.isCategoriaValida &&
        this.isUnidadeValida
      );
    },

    validarFormulario(){
      let valido = true;
      this.isNomeValido = true;
      this.nomePlaceholder = 'Nome*';

      for (let produto of this.produtosDaApi) {
        if (produto.nome === this.formData.nome) {
          this.isNomeValido = false;
          this.nomePlaceholder = '"' + produto.nome + '"' + ' já está cadastrado no sistema';
          this.formData.nome = null;
          valido = false;
          break;
        }
      }
      return valido;
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'produtos') {
        this.$router.push('/produtos');
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

</style>

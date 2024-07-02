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
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <select v-model="formData.tipo" class="form-select" id="tipo" aria-label="Tipo"
                placeholder="Selecione o tipo" required>
                <option disabled value="">Tipo</option>
                <option value="sanitario">Sanitário</option>
                <option value="alimenticio">Alimentício</option>
              </select>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-seedling"></i></span>
              <input v-model="formData.categoria" type="text" class="form-control" id="categoria"
                placeholder="Categoria" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
              <textarea v-model="formData.descricao" class="form-control" id="descricao"
                placeholder="Descrição"></textarea>
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

export default {
  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      formData: {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
      },
      isNomeValido: true,
      isTipoValido: true,
      isCategoriaValida: true,
      nomePlaceholder: 'Nome do Produto',
      tipoPlaceholder: 'Tipo do produto',
      categoriaPlaceholder: 'Categoria do Produto',
    };
  },
  methods: {

    validarFormulario() {
      this.isNomeValido = !!this.formData.nome.trim();
      if (!this.isNomeValido) this.nomePlaceholder = 'Campo Nome do Produto é obrigatório';

      this.isTipoValido = !!this.formData.tipo.trim();
      if (!this.isTipoValido) this.tipoPlaceholder = 'Campo Tipo do produto é obrigatório';

      this.isCategoriaValida = !!this.formData.categoria.trim();
      if (!this.isCategoriaValida) this.categoriaPlaceholder = 'Campo Categoria do Produto é obrigatório';

      return this.isNomeValido && this.isTipoValido && this.isCategoriaValida;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'produtos') {
        this.$router.push('/produtos');
      }
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/produtos/', this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
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

    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        tipo: '',
        categoria: '',
        descricao: null,
      };

      this.isNomeValido = true,
        this.isTipoValido = true,
        this.isCategoriaValida = true,
        this.nomePlaceholder = 'Nome do Produto',
        this.tipoPlaceholder = 'Tipo do produto'
      this.categoriaPlaceholder = 'Categoria do Produto'
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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}
</style>

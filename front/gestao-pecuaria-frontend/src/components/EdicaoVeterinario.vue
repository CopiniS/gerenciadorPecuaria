<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'veterinarios' }" id="nav-vet-tab"
          @click="selectTab('veterinarios')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Veterinários</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'veterinarios' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Veterinário</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.nome" :class="{ 'is-invalid': !isNomeValido }" type="text" class="form-control"
                id="nome" :placeholder="nomePlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-phone"></i></span>
              <input v-model="formData.telefone" @input="applyPhoneMask" :class="{ 'is-invalid': !isTelefoneValido }"
                type="text" class="form-control" id="telefone" :placeholder="telefonePlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-envelope"></i></span>
              <input v-model="formData.email" :class="{ 'is-invalid': !isEmailValido }" type="email" class="form-control"
                id="email" :placeholder="emailPlaceholder">
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-id-card"></i></span>
              <input v-model="formData.crmv" :class="{ 'is-invalid': !isCrmvValido }" type="text" class="form-control"
                id="crmv" :placeholder="crmvPlaceholder">
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="cancelarEdicao">Cancelar</button>
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

export default {
  name: 'TelaVeterinarios',
  data() {
    return {
      activeTab: 'edicao', // Começa na aba de edição
      formData: {
        id: null,
        nome: '',
        telefone: '',
        email: '',
        crmv: '',
      },
      isNomeValido: true,
      isTelefoneValido: true,
      isEmailValido: true,
      isCrmvValido: true,
      nomePlaceholder: 'Nome',
      telefonePlaceholder: 'Telefone',
      emailPlaceholder: 'Email',
      crmvPlaceholder: 'CRMV',
    };
  },
  mounted() {
    // Verifica se há um veterinário selecionado no localStorage para edição
    const veterinarioId = localStorage.getItem('veterinarioSelecionado');
    if (veterinarioId) {
      // Requisição para obter os dados do veterinário
      this.fetchVeterinario(veterinarioId);
    }
  },
  methods: {
    async fetchVeterinario(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/veterinarios/${id}`);
        const veterinario = response.data;
        this.formData.id = veterinario.id;
        this.formData.nome = veterinario.nome;
        this.formData.telefone = veterinario.telefone;
        this.formData.email = veterinario.email;
        this.formData.crmv = veterinario.crmv;
      } catch (error) {
        console.error('Erro ao carregar dados do veterinário:', error);
      }
    },
    validarFormulario() {
      this.isNomeValido = !!this.formData.nome.trim();
      if (!this.isNomeValido) this.formData.nome = '';

      this.isTelefoneValido = /^\(\d{2}\)\s\d{4,5}-\d{4}$/.test(this.formData.telefone.trim());
      if (!this.isTelefoneValido) this.formData.telefone = '';

      this.isEmailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.formData.email.trim());
      if (!this.isEmailValido) this.formData.email = '';

      this.isCrmvValido = /^[0-9]+$/.test(this.formData.crmv.trim());
      if (!this.isCrmvValido) this.formData.crmv = '';

      this.nomePlaceholder = this.isNomeValido ? 'Nome' : 'Campo Nome é obrigatório';
      this.telefonePlaceholder = this.isTelefoneValido ? 'Telefone' : 'Campo Telefone é obrigatório (somente números)';
      this.emailPlaceholder = this.isEmailValido ? 'Email' : 'Campo Email é obrigatório e deve ser válido';
      this.crmvPlaceholder = this.isCrmvValido ? 'CRMV' : 'Campo CRMV é obrigatório (somente números)';

      return this.isNomeValido && this.isTelefoneValido && this.isEmailValido && this.isCrmvValido;
    },

    applyPhoneMask(event) {
      let value = event.target.value.replace(/\D/g, '');
      if (value.length > 10) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
      } else if (value.length > 5) {
        value = value.replace(/(\d{2})(\d{4})(\d+)/, '($1) $2-$3');
      } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d+)/, '($1) $2');
      } else {
        value = value.replace(/(\d+)/, '($1');
      }
      this.formData.telefone = value;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'veterinarios') {
        this.$router.push('/Veterinarios');
      }
    },

    cancelarEdicao() {
      this.$router.push('/Veterinarios');
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/veterinarios/${this.formData.id}/`, this.formData, {});
          if (response.status === 200) {
            alert('Veterinário atualizado com sucesso!');
            this.resetForm();
          } else {
            alert('Erro ao atualizar veterinário. Tente novamente mais tarde.');
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
        telefone: '',
        email: '',
        crmv: '',
      };

      this.isNomeValido = true;
      this.isTelefoneValido = true;
      this.isEmailValido = true;
      this.isCrmvValido = true;
      this.nomePlaceholder = 'Nome';
      this.telefonePlaceholder = 'Telefone';
      this.emailPlaceholder = 'Email';
      this.crmvPlaceholder = 'CRMV';
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

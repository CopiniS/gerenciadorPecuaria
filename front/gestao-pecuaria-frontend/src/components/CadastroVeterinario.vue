<template>
    <div class="background">
      <nav>
        <div class="nav nav-tabs" id="nav-tab" role="tablist">
          <button class="nav-link" :class="{ active: activeTab === 'veterinarios' }" id="nav-vet-tab" @click="selectTab('veterinarios')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Veterinários</button>
          <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro</button>
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'veterinarios' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
          <!-- Conteúdo da aba 'Veterinários' -->
        </div>
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
  
          <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
            <h1 class="title fs-5" id="cadastroLabel">Cadastro de Veterinários</h1>
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome">
              </div>
              <div v-if="!isNomeValido" class="text-danger">Campo Nome é obrigatório.</div>
  
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-phone"></i></span>
                <input v-model="formData.telefone" type="text" class="form-control" id="telefone" placeholder="Telefone">
              </div>
              <div v-if="!isTelefoneValido" class="text-danger">Campo Telefone é obrigatório.</div>
  
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                <input v-model="formData.email" type="email" class="form-control" id="email" placeholder="Email">
              </div>
              <div v-if="!isEmailValido" class="text-danger">Campo Email é obrigatório.</div>
  
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-id-card"></i></span>
                <input v-model="formData.crmv" type="text" class="form-control" id="crmv" placeholder="CRMV">
              </div>
              <div v-if="!isCrmvValido" class="text-danger">Campo CRMV é obrigatório.</div>
  
              <div class="button-group justify-content-end">
                <button type="button" class="btn btn-secondary" @click="selectTab('veterinarios')">Cancelar</button>
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
    name: 'TelaVeterinarios',
    data() {
      return {
        activeTab: 'cadastro',  // Aba inicial é 'cadastro'
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
      };
    },
    methods: {
      validarFormulario() {
        this.isNomeValido = !!this.formData.nome.trim();
        this.isTelefoneValido = !!this.formData.telefone.trim();
        this.isEmailValido = !!this.formData.email.trim();
        this.isCrmvValido = !!this.formData.crmv.trim();
        
        // Retorne true se todos os campos forem válidos
        return this.isNomeValido && this.isTelefoneValido && this.isEmailValido && this.isCrmvValido;
      },
  
      selectTab(tab) {
        this.activeTab = tab;
        if (tab === 'veterinarios') {
          this.$router.push('/Veterinarios');
        }
      },
  
      async submitForm() {
        if (this.validarFormulario()) {
          try {
            const response = await api.post('http://127.0.0.1:8000/veterinarios/', this.formData, {});
            if (response.status === 201) {
              alert('Cadastro realizado com sucesso!');
              this.resetForm();
            } else {
              alert('Erro ao cadastrar veterinário. Tente novamente mais tarde.');
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
        
        // Reiniciar validações
        this.isNomeValido = true;
        this.isTelefoneValido = true;
        this.isEmailValido = true;
        this.isCrmvValido = true;
      },
    },
  };
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

.nav-link.active {
  background-color: #d0d0d0 !important;
  /* Cor um pouco mais escura quando a aba está ativa */
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
  /* Cor de fundo das células da tabela */
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  /* Adiciona uma borda verde na parte inferior */
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
</style>

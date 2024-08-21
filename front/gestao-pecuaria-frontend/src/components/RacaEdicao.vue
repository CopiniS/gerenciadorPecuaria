
<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista
          de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'racas' }" id="nav-vet-tab"
          @click="selectTab('racas')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Racas</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Raca</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'animais' }" id="nav-animais" role="tabpanel"
        aria-labelledby="nav-animais-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'racas' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Raca</h1>
            <form @submit.prevent="submitForm" @keydown="checkEnter">
                <div class="mb-3 input-group">
                  <span class="input-group-text" title="Nome da Raça"><i class="fas fa-horse"></i></span>
                  <input v-model="formData.nome" :class="{'is-invalid': !isNomeValido}" type="text" 
                  class="form-control" id="nome" :placeholder="nomePlaceholder" title="Nome da Raça">
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('racas')">Cancelar</button>
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

export default {
    data() {
        return {
            activeTab: 'edicao', // Começa na aba de edição
            racasDaApi: null,
            formData: {
                id: null,
                nome: ''
            },
            isNomeValido: true,
            nomePlaceholder: 'Nome da Raca',
        };
    },
 
    mounted() {
        const racaId = this.$route.params.racaId;
        if (racaId) {
            this.fetchRaca(racaId);
        }

        this.buscarRacasDaApi();
    },
    methods: {
//REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async fetchRaca(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/racas/${id}`);
        const raca = response.data;
        this.formData.id = raca.id;
        this.formData.nome = raca.nome;
      } catch (error) {
        console.error('Erro ao carregar dados da raca:', error);
      }
    },

    async submitForm() {
      if (this.verificaVazio() && this.validarFormulario()) {
       try {
          const response = await api.patch(`http://127.0.0.1:8000/racas/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.$router.push('/racas');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/');
        this.racasDaApi = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },


//VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    validarFormulario() {
      let valido = true;
      this.isNomeValido = true;
      this.nomePlaceholder = 'Nome do raca';
      
      // Cria uma nova lista sem o item com o id atual
      let racasComExclusao = this.racasDaApi.filter(raca => raca.id !== this.formData.id);

      // Verifica se o nome do raca já existe na lista
      for (let i = 0; i < racasComExclusao.length; i++) {
        if (racasComExclusao[i].nome === this.formData.nome) {
          this.isNomeValido = false;
          this.nomePlaceholder = 'Esta Raça já está cadastrada';
          this.formData.nome = null;
          valido = false;
          break;
        }
      }
      
      return valido;
    },
    
    verificaVazio(){
      if(this.formData.nome != null){
        if(this.formData.nome.trim() != ''){
          this.isNomeValido = true;
          this.nomePlaceholder = 'Digite o nome da Raça';
        }
        else{
          this.isNomeValido = false;
          this.nomePlaceholder = 'Nome da Raça é um Campo Obrigatório'
        }
      }
      else{
        this.isNomeValido = false;
        this.nomePlaceholder = 'Nome da Raça é um Campo Obrigatório'
      }

      return this.isNomeValido;
    },


//FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
checkEnter(event) {
      if (event.key === 'Enter') {
        this.submitForm();
      }
    },    
selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'racas') {
        this.$router.push('/racas');
      }
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
    },

    cancelarEdicao() {
      this.$router.push('/racas');
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

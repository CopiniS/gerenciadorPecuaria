<template>
<div class="background">

  <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'propriedades' }" id="nav-propriedades-tab" @click="selectTab('propriedades')" 
        type="button" role="tab" aria-controls="nav-propriedades" aria-selected="true">Lista de Propriedades</button>
        
        <button class="nav-link" :class="{ active: activeTab === 'piquetes' }" id="nav-piquetes-tab" @click="selectTab('piquetes')" 
        type="button" role="tab" aria-controls="nav-piquetes" aria-selected="false">Lista de Piquetes</button>
        
      </div>
    </nav>
    
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'propriedades' }" id="nav-propriedades" role="tabpanel" aria-labelledby="nav-propriedades-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'piquetes' }" id="nav-piquetes" role="tabpanel" aria-labelledby="nav-piquetes-tab">
        
      </div>
    </div>

<h2>Lista de Piquetes</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Nome</label>
          <input type="text" class="form-control input-consistente" id="nome" v-model="filtro.nome">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="tipoCultivo" class="form-label me-2">Tipo de Cultivo</label>
          <select class="form-select select-consistente" id="tipoCultivo" v-model="filtro.tipoCultivo">
            <option value="">Selecione o tipo</option>
            <option>Pastagem Natural</option>
            <option>Lavoura</option>
            <option>Confinamento</option>
          </select>
        </div>
        <div class="col-12 d-flex justify-content-center mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

  <div>
    <div class="table-container">
        <div class="button-container">
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Piquete</button>
        </div>
        <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo de Cultivo</th>
            <th scope="col">Área</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(piquete, index) in piquetes" :key="index">
            <td>{{ piquete.nome }}</td>
            <td>{{ piquete.tipoCultivo }}</td>
            <td>{{ piquete.area }}</td>
            <td>
                <button @click="acessarEdicao(piquete)" class="btn-acoes btn-sm"><i class="fas fa-edit"></i></button>
                <button @click="confirmarExclusao(piquete)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
        
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir este Piquete?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarPiquete()">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  data() {
    return {
      activeTab: 'piquetes',
      piquetes: [],
      piquetesDaApi: [],
      formData: {
        id: null,
        nome: '',
        tipoCultivo: '',
        area: '',
        propriedade: localStorage.getItem('propriedadeSelecionada')
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
        tipoCultivo: '',
      },
    }
  },
  mounted() {
    this.buscarPiquetesDaApi();
  },
  methods: {
     selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'propriedades') {
        this.$router.push('/propriedades');
      }
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/' , {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetesDaApi = response.data;
        this.piquetes = this.piquetesDaApi;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },
    
    acessarEdicao(piquete) {
      this.$router.push({
        name: 'PiqueteEdicao', 
        params: { piqueteId: piquete.id } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'PiqueteCadastro', 
      })
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    confirmarExclusao(piquete) {
      this.formData = {
        id: piquete.id,
      };
    },

    async apagarPiquete() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/piquetes/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Piquete apagado com sucesso!');
          this.buscarPiquetesDaApi();
        } else {
          alert('Erro ao apagar piquete. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    aplicarFiltro() {
      this.piquetes = this.piquetesDaApi.filter(piquete => {
        return  piquete.nome.toLowerCase().includes(this.filtro.nome) &&
                piquete.tipoCultivo.includes(this.filtro.tipoCultivo);
        });
    },
    
    limparFiltro() {
      this.filtro.nome = '';
      this.filtro.tipoCultivo = '';
    },
    
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color:  #ededef; /* Um tom mais escuro que o branco */
  min-height: 100vh; /* Garante que o fundo cubra toda a altura da tela */
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
  background-color: #ededef !important; /* Cor de fundo das células da tabela */
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a; /* Adiciona uma borda verde na parte inferior */
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

.input-consistente, .select-consistente {
    width: 200px; 
}

</style>

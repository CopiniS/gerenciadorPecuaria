<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Veterinários</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Veterinários</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Nome</label>
          <input type="text" class="form-control" id="nome" v-model="filtro.nome">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="telefone" class="form-label me-2">Telefone</label>
          <input type="text" class="form-control" id="telefone" v-model="filtro.telefone">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="email" class="form-label me-2">Email</label>
          <input type="email" class="form-control" id="email" v-model="filtro.email">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="crmv" class="form-label me-2">CRMV</label>
          <input type="text" class="form-control" id="crmv" v-model="filtro.crmv">
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button class="btn btn-success" @click="aplicarFiltro">Filtrar</button>
        </div>
      </form>
    </div>

  <div>
    <div class="table-container">
    <div class="button-container">
      <button @click="() => {this.$router.push('/cadastroVeterinario');}" type="button" class="btn btn-success">Cadastrar Veterinário</button>
    </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Telefone</th>
            <th scope="col">Email</th>
            <th scope="col">CRMV</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(veterinario, index) in veterinarios" :key="index">
            <td>{{ veterinario.nome }}</td>
            <td>{{ veterinario.telefone }}</td>
            <td>{{ veterinario.email }}</td>
            <td>{{ veterinario.crmv }}</td>
            <td>
              <button @click="editarVeterinario(veterinario)" class="btn-acoes btn-sm"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(veterinario)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
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
            Tem certeza de que deseja excluir este veterinário?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarVeterinario()">Excluir</button>
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
  name: 'TelaVeterinarios',
  data() {
    return {
      veterinarios: [],
      formData: {
        id: null,
        nome: '',
        telefone: '',
        email: '',
        crmv: '',
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
        telefone: '',
        email: '',
        crmv: ''
      },
    }
  },
  mounted() {
    this.buscarVeterinariosDaApi();
  },
  methods: {
    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/' , {
          // Parâmetros da requisição (se houver)
        });
        this.veterinarios = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },
    editarVeterinario(veterinario) {
      localStorage.setItem('veterinarioSelecionado', veterinario.id);
      this.$router.push('/editarVeterinario')
    },

    confirmarExclusao(veterinario) {
      this.formData = {
        id: veterinario.id,
      };
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async apagarVeterinario() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/veterinarios/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Veterinário apagado com sucesso!');
          this.buscarVeterinariosDaApi();
        } else {
          alert('Erro ao apagar veterinário. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoModal');
    },

    aplicarFiltro() {
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
      this.filtro = {
        nome: '',
        telefone: '',
        email: '',
        crmv: ''
      };
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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px; 
}

</style>

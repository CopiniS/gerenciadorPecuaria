<template>
<div class="background">
<h2>Veterinários</h2>
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
      <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Veterinário</button>
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
          <tr v-for="(veterinario, index) in lotes" :key="index">
            <td>{{ veterinario.nome }}</td>
            <td>{{ veterinario.telefone }}</td>
            <td>{{ veterinario.email }}</td>
            <td>{{ veterinario.crmv }}</td>
            <td>
              <button @click="editarVeterinario(veterinario)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(veterinario)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Veterinários -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Veterinários</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-phone"></i></span>
                <input v-model="formData.telefone" type="text" class="form-control" id="telefone" placeholder="Telefone" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                <input v-model="formData.email" type="email" class="form-control" id="email" placeholder="Email" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-id-card"></i></span>
                <input v-model="formData.crmv" type="text" class="form-control" id="crmv" placeholder="CRMV" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição de Veterinário -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Veterinário</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-phone"></i></span>
                <input v-model="formData.telefone" type="text" class="form-control" id="telefoneEditar" placeholder="Telefone" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                <input v-model="formData.email" type="email" class="form-control" id="emailEditar" placeholder="Email" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-id-card"></i></span>
                <input v-model="formData.crmv" type="text" class="form-control" id="crmvEditar" placeholder="CRMV" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Salvar</button>
          </div>
        </div>
      </div>
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
      lotes: [],
      formData: {
        id: null,
        nome: '',
        telefone: '',
        email: '',
        crmv: '',
      },mostrarFormulario: false,
      filtro: {
        nome: '',
        telefone: '',
        email: '',
        crmv: ''
      },
      modalTitle: 'Cadastro de Veterinário',
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
        this.lotes = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinários da API:', error);
      }
    },
    editarVeterinario(veterinario) {
      this.modalTitle = 'Editar Veterinário';
      this.formData = {
        id: veterinario.id,
        nome: veterinario.nome,
        telefone: veterinario.telefone,
        email: veterinario.email,
        crmv: veterinario.crmv,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        telefone: '',
        email: '',
        crmv: '',
      };
      this.modalTitle = 'Cadastro de Veterinário';
    },
    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },
    confirmarExclusao(veterinario) {
      this.formData = {
        id: veterinario.id,
        nome: veterinario.nome,
        telefone: veterinario.telefone,
        email: veterinario.email,
        crmv: veterinario.crmv,
      };
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
      this.fecharModal("confirmacaoExclusaoModal");
    },
    
    
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Veterinário') {
        try {
          const response = await api.post('http://127.0.0.1:8000/veterinarios/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarVeterinariosDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar veterinário. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/veterinarios/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarVeterinariosDaApi();
            this.fecharModal("edicaoModal");
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
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
  border-bottom: 2px solid #4CAF50; /* Adiciona uma borda verde na parte inferior */
  background-color: #f0f0f0;
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #4CAF50;
}

.button-group {
  display: flex;
  gap: 10px; 
}

</style>

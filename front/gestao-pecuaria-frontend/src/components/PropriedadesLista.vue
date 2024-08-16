<template>
  <div class="background">

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" data-bs-target="#nav-vet" type="button"
          role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Propriedades</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0">
      </div>
    </div>

    <h2>Lista de Propriedades</h2>
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
          <label for="cidade" class="form-label me-2">Cidade</label>
          <input type="text" class="form-control input-consistente" id="cidade" v-model="filtro.cidade">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="estado" class="form-label me-2">Estado</label>
          <input type="text" class="form-control input-consistente" id="estado" v-model="filtro.estado">
        </div>
        <div class="col-12 d-flex justify-content-start mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>


    <div class="table-responsive">
      <div class="table-container">
        <div class="button-container">
          <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Propriedade</button>
          <button @click="() => { this.$router.push('/piquetes'); }" type="button" class="btn btn-success">Lista de
            Piquetes</button>
        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Nome</th>
              <th scope="col">Cidade</th>
              <th scope="col">Estado</th>
              <th scope="col">Endereço</th>
              <th scope="col">Latitude</th>
              <th scope="col">Longitude</th>
              <th scope="col">Área</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(propriedade, index) in propriedades" :key="index">
              <td>{{ propriedade.nome }}</td>
              <td>{{ propriedade.cidade }}</td>
              <td>{{ propriedade.estado }}</td>
              <td>{{ propriedade.endereco }}</td>
              <td>{{ replacePontoVirgula(propriedade.latitude) }}</td>
              <td>{{ replacePontoVirgula(propriedade.longitude) }}</td>
              <td>{{ replacePontoVirgula(propriedade.area) }}</td>
              <td>
                <button v-if="propriedadeAtual == propriedade.id" @click="acessarEdicao(propriedade)"
                  class="btn-acoes btn-sm" title="Editar Propriedade">
                  <i class="fas fa-edit"></i>
                </button>
                <button v-if="propriedadeAtual == propriedade.id" @click="confirmarExclusao(propriedade)"
                  class="btn-acoes btn-sm" data-bs-toggle="modal" title="Excluir Propriedade"
                  data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i>
                </button>
                <button v-if="propriedadeAtual != propriedade.id" @click="trocaPropriedade(propriedade.id)"
                  class="btn-acoes btn-sm" title="Trocar Propriedade">
                  <i class="fas fa-exchange-alt"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>

      </div>

      <!-- Modal de Confirmação de Exclusão -->
      <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
        aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir esta Propriedade?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarPropriedade()">Excluir</button>
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
      propriedades: [],
      propriedadesDaApi: [],
      propriedadeAtual: localStorage.getItem('propriedadeSelecionada'),
      formData: {
        id: null,
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
        area: '',
      },
      mostrarFormulario: false,
      filtro: {
        nome: '',
        cidade: '',
        estado: '',
      },
    }
  },
  mounted() {
    this.buscarPropriedadesDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarPropriedadesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/propriedades/', {
        });
        this.propriedadesDaApi = response.data;
        this.propriedades = this.propriedadesDaApi;
      } catch (error) {
        console.error('Erro ao buscar propriedades da API:', error);
      }
    },

    async apagarPropriedade() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/propriedades/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Propriedade apagada com sucesso!');
          this.buscarPropriedadesDaApi();
        } else {
          alert('Erro ao apagar propriedade. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },


    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.propriedades = this.propriedadesDaApi.filter(propriedade => {
        return propriedade.nome.toLowerCase().includes(this.filtro.nome) &&
          propriedade.cidade.toLowerCase().includes(this.filtro.cidade.toLowerCase()) &&
          propriedade.estado.toLowerCase().includes(this.filtro.estado.toLowerCase());
      });
    },

    limparFiltro() {
      this.filtro.nome = '';
      this.filtro.cidade = '';
      this.filtro.estado = '';
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    acessarEdicao(propriedade) {
      this.$router.push({
        name: 'PropriedadeEdicao',
        params: { propriedadeId: propriedade.id }
      })
    },

    acessarCadastro() {
      this.$router.push({
        name: 'PropriedadeCadastro',
      })
    },

    trocaPropriedade(propriedadeId) {
      localStorage.setItem('propriedadeSelecionada', propriedadeId);
      window.location.reload();
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    confirmarExclusao(propriedade) {
      this.formData = {
        id: propriedade.id,
      };
    },

    replacePontoVirgula(valorString) {
      if (typeof valorString === 'string') {
        valorString = valorString.replace(".", ",");
      } else {
        valorString = '-';
      }
      return valorString;
    },
  }
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
  overflow-x: auto;
}

.button-container {
  display: flex;
  flex-wrap: nowrap; /* Garante que os botões não vão para a linha seguinte */
  gap: 10px; /* Espaço entre os botões */
  margin-bottom: 20px; 
  white-space: nowrap; /* Evita quebras de linha nos botões */
}

.btn-success {
  margin-right: 10px;
  margin-bottom: 10px;
}
.table{
  min-width: 600px;
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

.button-group {
  display: flex;
  gap: 10px;
}

.input-consistente,
.select-consistente {
  width: 200px;
}

.btn {
  margin-bottom: 0;
}
</style>

<template>
<div class="background">

  <nav>
  <div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" 
    data-bs-target="#nav-vet" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Propriedades</button>
  </div>
</nav>
<div class="tab-content" id="nav-tabContent">
  <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0"></div>
 </div>

<h2>Lista de Propriedades</h2>
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
          <label for="tipoCultivo" class="form-label me-2">Cidade</label>
          <select class="form-select" id="cidade" v-model="filtro.tipoCultivo">
            <option value="">Selecione a cidade</option>
          </select>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="tipoCultivo" class="form-label me-2">Cidade</label>
          <select class="form-select" id="estado" v-model="filtro.tipoCultivo">
            <option value="">Selecione o estado</option>
          </select>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="area" class="form-label me-2">Área</label>
          <input type="number" class="form-control" id="area" v-model="filtro.area">
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
            <button @click="acessarCadastro()" type="button" class="btn btn-success" >Cadastrar Propriedade</button>
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="(propriedade, index) in propriedades" :key="index">
            <td>{{ propriedade.nome }}</td>
            <td>{{ propriedade.cidade }}</td>
            <td>{{ propriedade.estado }}</td>
            <td>{{ propriedade.endereco }}</td>
            <td>{{ propriedade.latitude }}</td>
            <td>{{ propriedade.longitude }}</td>
            <td>{{ propriedade.area }}</td>
            <td>
                <button v-if="propriedadeAtual == propriedade.id" @click="acessarEdicao(propriedade)" class="btn-acoes btn-sm">
                    <i class="fas fa-edit"></i>
                </button>
                <button v-if="propriedadeAtual == propriedade.id" @click="confirmarExclusao(propriedade)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i>
                </button>
                <button v-if="propriedadeAtual != propriedade.id" @click="trocaPropriedade(propriedade.id)">Trocar</button>
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
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
        area: '',
      },
    }
  },
  mounted() {
    this.buscarPropriedadesDaApi();
  },
  methods: {
    async buscarPropriedadesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/propriedades/' , {
        });
        this.propriedades = response.data;
      } catch (error) {
        console.error('Erro ao buscar propriedades da API:', error);
      }
    },
    
    acessarEdicao(propriedade) {
      this.$router.push({
        name: 'PropriedadeEdicao', 
        params: { propriedadeId: propriedade.id } 
      })
    },

    acessarCadastro(){
        this.$router.push({
        name: 'PropriedadeCadastro', 
      })
    },

    trocaPropriedade(propriedadeId){
        localStorage.setItem('propriedadeSelecionada', propriedadeId);
        this.$router.push('/inicio')
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
    async apagarPropriedade() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/propriedades/${this.formData.id}/` , {
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

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

    aplicarFiltro() {
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
        this.filtro = {
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
        area: '',
      }
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

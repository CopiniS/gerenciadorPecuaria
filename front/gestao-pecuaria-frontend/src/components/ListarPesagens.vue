<template>
  <h2>Pesagens</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataPesagem" class="form-label me-2">Data da pesagem</label>
          <input type="date" class="form-control" id="dataPesagem" v-model="filtro.dataPesagem">
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
      <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Pesagem</button>
    </div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Data Pesagem</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in datasPesagens" :key="index">
            <td>{{ formatarData(data) }}</td>
            <td>
              <button @click="preencherDetalhesPesagemPorData(data)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#visualizacaoModal"><i class="fas fa-eye"></i></button>
              <button @click="confirmarExclusao(data)" class="btn-acoes btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro de Pesagem -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">{{ modalTitle }}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.dataPesagem" type="date" class="form-control" id="dataPesagem" required>
              </div>
              <hr>
              <div class="mb-3 input-group">
                <input v-model="brinco" @input="filterAnimais" type="text" class="form-control" placeholder="Digite o brinco...">
              </div>
              <div class="list-group" v-if="brinco && filteredAnimais.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="animal in filteredAnimais" :key="animal.id" @click="selectAnimal(animal)">
                  {{ animal.brinco }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-weight"></i></span>
                <input v-model="formData.peso" type="text" class="form-control" id="peso" :disabled="!camposHabilitados" placeholder="Peso" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-comment"></i></span>
                <input v-model="formData.observacao" type="text" class="form-control" id="observacao" :disabled="!camposHabilitados" placeholder="Observação" required>
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

    <!-- Modal de Visualização de Pesagem -->
    <div class="modal fade" id="visualizacaoModal" tabindex="-1" aria-labelledby="visualizacaoModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="visualizacaoModalLabel">Detalhes da Pesagem</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Data da Pesagem:</strong> {{ formatarData(this.dataSelecionada) }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Brinco</th>
                  <th scope="col">Peso</th>
                  <th scope="col">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pesagem in this.detalhesPesagem" :key="pesagem.id">
                  <td>{{ pesagem.animal.brinco}}</td>
                  <td>{{ pesagem.peso}}</td>
                  <td>
                    <button @click="confirmarExclusaoPesagem(pesagem)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoAnimalModal"><i class="fas fa-trash-alt"></i></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão de Pesagem por Data -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir esta pesagem?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarPesagemPorData">Excluir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão de Pesagem -->
    <div class="modal fade" id="confirmacaoExclusaoAnimalModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoAnimalModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoAnimalModalLabel">Confirmação de Exclusão de Animal</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir este animal da pesagem?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarPesagem">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaPesagens',
  data() {
    return {
      pesagens: [],
      formData: {
        id: null,
        dataPesagem: '',
        peso: '',
        observacao: '',
        animal: null
      },
      animais: [],
      filteredAnimais: [],
      modalTitle: 'Cadastro de Pesagem',
      camposHabilitados: false,
      brinco: '',
      detalhesPesagem: [],
      pesagemParaExcluir: null,
      dataParaExclusao: null,
      datasPesagens: [], 
      dataSelecionada: null, 
      mostrarFormulario: false,
      filtro: {
        dataPesagem: '',
      }
    }
  },
  mounted() {
    this.buscarAnimais();
    this.buscarPesagens();
  },
  methods: {

    async buscarPesagens(data) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/pesagens/?data=${data}`);
        this.pesagens = response.data; 

        this.preencherDatasPesagens();

      } catch (error) {
        console.error('Erro ao buscar pesagens por data:', error);
      }
    },

    async preencherDatasPesagens(){
      const datasSet = new Set();
      this.pesagens.forEach(pesagem => {
        datasSet.add(pesagem.dataPesagem);
      });
      this.datasPesagens = Array.from(datasSet).sort((b, a) => new Date(a) - new Date(b));
    },

    async preencherDetalhesPesagemPorData(data){
      this.detalhesPesagem = []
      this.pesagens.forEach(pesagem => {
        if(data === pesagem.dataPesagem){
          this.detalhesPesagem.push(pesagem);
        }
      });
      this.dataSelecionada = data;

    },

    async buscarAnimais() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/');
        this.animais = response.data;
        this.filteredAnimais = this.animais;
      } catch (error) {
        console.error('Erro ao buscar animais:', error);
      }
    },
    filterAnimais() {
      this.filteredAnimais = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },
    selectAnimal(animal) {
      this.brinco = animal.brinco;
      this.formData.animal = animal.id;
      this.camposHabilitados = true;
      this.filteredAnimais = [];
    },
    resetForm() {
      this.formData = {
        id: null,
        dataPesagem: new Date().toISOString().substr(0, 10),
        peso: '',
        observacao: null,
        animal: null
      };
      this.brinco = '';
      this.modalTitle = 'Cadastro de Pesagem';
      this.camposHabilitados = false;
      this.filteredAnimais = this.animais;
    },
    confirmarExclusao(data) {
      this.dataParaExclusao = data;
    },
    confirmarExclusaoPesagem(pesagem) {
      this.pesagemParaExcluir = pesagem;
    },

    async apagarPesagemPorData() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/pesagens/datas/${this.dataParaExclusao}/`, {
        });

        if (response.status === 204) {
          alert('Pesagem excluída com sucesso!');
        } else {
          alert('Erro ao excluir pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.buscarPesagens();
      this.fecharModal('confirmacaoExclusaoModal');
    },
    async apagarPesagem() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/pesagens/${this.pesagemParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Animal excluído com sucesso!');
          this.detalhesPesagem = this.detalhesPesagem.filter(animal => animal.id !== this.pesagemParaExcluir.id);
          this.pesagemParaExcluir = null;
        } else {
          alert('Erro ao excluir animal. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.buscarPesagens();
      this.fecharModal('confirmacaoExclusaoAnimalModal');
    },

    async fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async submitForm() {
      try {
        const response = await api.post('http://127.0.0.1:8000/pesagens/', {
          ...this.formData
        });

        if (response.status === 201) {
          this.resetForm();
          this.buscarPesagens();
          alert('Pesagem cadastrada com sucesso!');
        } else {
          alert('Erro ao cadastrar pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }

      this.fecharModal("cadastroModal");
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
        dataPesagem: '',
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

.table-container table thead tr th {
  border-bottom: 2px solid #4CAF50; /* Adiciona uma borda verde na parte inferior */
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
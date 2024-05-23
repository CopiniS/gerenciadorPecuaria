<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Pesagem</button>
    </div>
    <h2>Lista de Pesagens</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Data Pesagem</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(pesagem, index) in pesagens" :key="index">
            <td>{{ formatarData(pesagem.dataPesagem) }}</td>
            <td>
              <button @click="buscarPesagensPorData(pesagem)" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#visualizacaoModal"><i class="fas fa-eye"></i></button>
              <button @click="confirmarExclusao(pesagem)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
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
            <p><strong>Data da Pesagem:</strong> {{ formatarData(formData.dataPesagem) }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Brinco</th>
                  <th scope="col">Peso</th>
                  <th scope="col">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="animal in detalhesPesagem" :key="animal.id">
                  <td>{{ animal.brinco }}</td>
                  <td>{{ animal.peso }}</td>
                  <td>
                    <button @click="confirmarExclusaoAnimal(animal)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoAnimalModal"><i class="fas fa-trash-alt"></i></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão de Pesagem -->
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
            <button type="button" class="btn btn-danger" @click="apagarPesagem">Excluir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão de Animal -->
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
            <button type="button" class="btn btn-danger" @click="apagarAnimal">Excluir</button>
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
      animalParaExcluir: null,
      datasPesagens: [], 
      dataSelecionada: null, 
    }
  },
  mounted() {
    this.buscarAnimais();
    this.buscarPesagensPorData();
  },
  methods: {

    async buscarPesagensPorData(data) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/pesagens/?data=${data}`);
        this.pesagens = response.data; 
        this.formData.dataPesagem = this.pesagens.dataPesagem;
        this.detalhesPesagem = this.pesagens.animais;
      } catch (error) {
        console.error('Erro ao buscar pesagens por data:', error);
      }
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
    confirmarExclusao(pesagem) {
      this.formData = {
        id: pesagem.id,
        dataPesagem: pesagem.dataPesagem,
        peso: pesagem.peso,
        observacao: pesagem.observacao,
        animal: pesagem.animal
      };
    },
    confirmarExclusaoAnimal(animal) {
      this.animalParaExcluir = animal;
    },
    async apagarPesagem() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/pesagens/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Pesagem excluída com sucesso!');
          this.buscarPesagensPorData();
        } else {
          alert('Erro ao excluir pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async apagarAnimal() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/animais/${this.animalParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Animal excluído com sucesso!');
          this.detalhesPesagem = this.detalhesPesagem.filter(animal => animal.id !== this.animalParaExcluir.id);
          this.animalParaExcluir = null;
        } else {
          alert('Erro ao excluir animal. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async submitForm() {
      try {
        const response = await api.post('http://127.0.0.1:8000/pesagens/', {
          ...this.formData
        });

        if (response.status === 201) {
          this.resetForm();
          this.buscarPesagensPorData();
          alert('Pesagem cadastrada com sucesso!');
        } else {
          alert('Erro ao cadastrar pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    formatarData(data) {
      console.log('data: ' , data);
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(data).toLocaleDateString('pt-BR', options);
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
.table-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>
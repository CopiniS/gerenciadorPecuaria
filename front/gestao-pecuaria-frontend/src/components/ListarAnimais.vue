<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar</button>
    </div>
    <h2>Lista de Animais</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Brinco</th>
            <th scope="col">Data Nascimento</th>
            <th scope="col">Sexo</th>
            <th scope="col">Raça</th>
            <th scope="col">Observações</th>
            <th scope="col">Lote</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(animal, index) in animais" :key="index">
            <td>{{ animal.brinco }}</td>
            <td>{{ animal.data }}</td>
            <td>{{ animal.sexo }}</td>
            <td>{{ animal.raca }}</td>
            <td>{{ animal.observacoes }}</td>
            <td>{{ nomeDoLote(animal.lote) }}</td>
            <td>
              <button @click="editarAnimal(animal)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                <button class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Cadastro-->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de animal</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="brinco" class="col-form-label">Brinco:</label>
                <input v-model="formData.brinco" type="text" class="form-control" id="brinco">
              </div>
              <div class="mb-3">
                <label for="dataNascimento" class="col-form-label">Data de Nascimento:</label>
                <input v-model="formData.dataNascimento" type="date" class="form-control" id="dataNascimento">
              </div>
              <div class="mb-3">
                <label for="sexo" class="col-form-label">Sexo:</label>
                <select v-model="formData.sexo" class="form-select" id="sexo">
                  <option selected>Selecione o sexo</option>
                  <option value="masculino">Masculino</option>
                  <option value="feminino">Feminino</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="racaPredominante" class="col-form-label">Raça Predominante:</label>
                <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante">
                  <option disabled value="">Selecione a raça predominante</option>
                  <option v-for="raca in racas" :key="raca.nome" :value="raca.nome">{{ raca.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="observacoesRaca" class="col-form-label">Observações da Raça:</label>
                <textarea v-model="formData.observacoesRaca" class="form-control" id="observacoesRaca"></textarea>
              </div>
              <div class="mb-3">
                <label for="lote" class="col-form-label">Lote:</label>
                <select v-model="formData.lote" class="form-select" id="lote">
                  <option disabled value="">Selecione o lote</option>
                  <option v-for="lote in lotes" :key="lote.id" :value="lote.id">{{ lote.nome }}</option>
                </select>
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

    <!-- Modal de Edição -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar animal</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="brinco" class="col-form-label">Brinco:</label>
                <input v-model="formData.brinco" type="text" class="form-control" id="brincoEditar">
              </div>
              <div class="mb-3">
                <label for="dataNascimento" class="col-form-label">Data de Nascimento:</label>
                <input v-model="formData.dataNascimento" type="date" class="form-control" id="dataNascimentoEditar">
              </div>
              <div class="mb-3">
                <label for="sexo" class="col-form-label">Sexo:</label>
                <select v-model="formData.sexo" class="form-select" id="sexoEditar">
                  <option selected>Selecione o sexo</option>
                  <option value="masculino">Masculino</option>
                  <option value="feminino">Feminino</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="racaPredominante" class="col-form-label">Raça Predominante:</label>
                <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante">
                  <option selected>{{ formData.racaPredominante }}</option>
                  <option v-for="raca in racas" :key="raca.nome" :value="raca.nome">{{ raca.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="observacoesRaca" class="col-form-label">Observações da Raça:</label>
                <textarea v-model="formData.observacoesRaca" class="form-control" id="observacoesRacaEditar"></textarea>
                <div class="mb-3">
                  <label for="lote" class="col-form-label">Lote:</label>
                  <select v-model="formData.lote" class="form-select" id="lote">
                    <option disabled value="">Selecione o lote</option>
                    <option v-for="lote in lotes" :key="lote.id" :value="lote.id">{{ lote.nome }}</option>
                  </select>
                </div>
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
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir este animal?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarAnimal(animal)">Excluir</button>
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
            Tem certeza de que deseja excluir este animal?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarAnimal(animal)">Excluir</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TelaAnimais',
  data() {
    return {
      animais: [],
      racas: [],
      lotes: [],
      formData: {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: '',
        observacoesRaca: '',
        lote: ''
      },
      modalTitle: 'Cadastro de Animal',
    }
  },
  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarRacasDaApi();
  },
  methods: {
    nomeDoLote(idLote) {
      const lote = this.lotes.find(lote => lote.id === idLote);
      return lote ? lote.nome : '';
    },
    async buscarRacasDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/racas/');
        this.racas = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },
    async buscarAnimaisDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/animais/');
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },
    editarAnimal(animal) {
      this.modalTitle = 'Editar Animal';
      this.formData = {
        id: animal.id,
        brinco: animal.brinco,
        dataNascimento: animal.data,
        sexo: animal.sexo,
        racaPredominante: animal.raca,
        observacoesRaca: animal.observacoes,
        lote: animal.lote
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: '',
        observacoesRaca: '',
        lote: ''
      };
      this.modalTitle = 'Cadastro de Animal';
    },
    async apagarAnimal(animal) {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/animais/${animal.id}/`);

        if (response.status === 204) {
          alert('Animal apagado com sucesso!');
          this.buscarAnimaisDaApi();
        } else {
          alert('Erro ao apagar animal. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Animal') {
        try {
          const response = await axios.post(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
          } else {
            alert('Erro ao cadastrar animal. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await axios.put(`http://127.0.0.1:8000/animais/${this.formData}/`, this.formData);

          if (response.status === 201) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    }
  }
};
</script>

<style scoped>
.table-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>

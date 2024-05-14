<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar de Pesagens</button>
    </div>
    <h2>Lista de Pesagens</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
           
            <th scope="col">Data Pesagem</th>
            <th scope="col">Peso</th>
            <th scope="col">Observacao</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(produto, index) in produtos" :key="index">
            <td>{{ produto.dataPesagem }}</td>
            <td>{{ produto.peso }}</td>
            <td>{{ produto.observacao }}</td>
            <td>
              <button @click="editarProduto(produto)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(produto)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
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
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Pesagem</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <div class="mb-3 input-group">
                  <input v-model="brinco" type="text" class="form-control" placeholder="Digite o brinco...">
                    <button @click="buscarAnimal" class="btn btn-primary" type="button">Buscar</button>
              </div>
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.dataPesagem" type="date" class="form-control" id="dataPesagem" :disabled="!camposHabilitados" required>
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
            <button type="button" class="btn btn-primary" @click="submitForm" :disabled="!camposHabilitados">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição de Pesagem -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Pesagem</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                <input v-model="formData.dataPesagem" type="date" class="form-control" id="dataPesagemEditar" :disabled="!camposHabilitados" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-weight"></i></span>
                <input v-model="formData.peso" type="text" class="form-control" id="pesoEditar" :disabled="!camposHabilitados" placeholder="Peso" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-comment"></i></span>
                <input v-model="formData.observacao" type="text" class="form-control" id="observacaoEditar" :disabled="!camposHabilitados" placeholder="Observação" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm" :disabled="!camposHabilitados">Salvar</button>
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
            Tem certeza de que deseja excluir esta pesagem?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarPesagem()">Excluir</button>
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
      },
      modalTitle: 'Cadastro de Pesagem',
      camposHabilitados: false,
      brinco: ''
    }
  },
  mounted() {
    this.buscarPesagensDaApi();
  },
  methods: {
    async buscarPesagensDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/pesagens/' , {});
        this.pesagens = response.data;
      } catch (error) {
        console.error('Erro ao buscar pesagens da API:', error);
      }
    },
    async buscarAnimal() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/animais/${this.brinco}`, {});

        if (response.data) {
          this.camposHabilitados = true;
          this.formData.dataPesagem = new Date().toISOString().substr(0, 10); // Preenche a data atual
        } else {
          alert('Animal não encontrado com o brinco especificado.');
        }
      } catch (error) {
        console.error('Erro ao buscar animal:', error);
        alert('Erro ao buscar animal. Verifique o console para mais detalhes.');
      }
    },
    editarPesagem(pesagem) {
      this.modalTitle = 'Editar Pesagem';
      this.formData = {
        id: pesagem.id,
        dataPesagem: pesagem.dataPesagem,
        peso: pesagem.peso,
        observacao: pesagem.observacao,
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        brinco: '',
        dataPesagem: '',
        peso: '',
        observacao: '',
      };
      this.modalTitle = 'Cadastro de Pesagem';
      this.camposHabilitados = false;
    },
    confirmarExclusao(pesagem) {
      this.formData = {
        id: pesagem.id,
        dataPesagem: pesagem.dataPesagem,
        peso: pesagem.peso,
        observacao: pesagem.observacao,
      };
    },
    async apagarPesagem() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/pesagens/${this.formData.id}/`, {});

        if (response.status === 204) {
          alert('Pesagem excluída com sucesso!');
          this.buscarPesagensDaApi();
        } else {
          alert('Erro ao excluir pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Pesagem') {
        try {
          const response = await api.post('http://127.0.0.1:8000/pesagens/', this.formData, {});

          if (response.status === 201) {
            alert('Pesagem cadastrada com sucesso!');
            this.resetForm();
            this.buscarPesagensDaApi();
          } else {
            alert('Erro ao cadastrar pesagem. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/pesagens/${this.formData.id}/`, this.formData, {});

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarPesagensDaApi();
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
/* Estilos */
</style>
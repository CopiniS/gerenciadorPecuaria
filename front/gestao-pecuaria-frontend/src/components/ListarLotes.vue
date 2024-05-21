<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Lote</button>
    </div>
    <h2>Lista de Lotes</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo de Cultivo</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(lote, index) in lotes" :key="index">
            <td>{{ lote.nome }}</td>
            <td>{{ lote.tipoCultivo }}</td>
            <td>
              <button @click="editarLote(lote)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="editarLote(lote)" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
        <!-- Modal de Cadastro de Lote -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Lote</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nome" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <select v-model="formData.tipoCultivo" class="form-select" id="tipoCultivo" aria-label="Tipo de Cultivo" required>
                  <option disabled selected>Selecione o tipo de cultivo</option>
                  <option v-for="tipo in tiposCultivo" :key="tipo" :value="tipo">{{ tipo }}</option>
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

    <!-- Modal de Edição de Lote -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Lote</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tags"></i></span>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar" placeholder="Nome" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-seedling"></i></span>
                <select v-model="formData.tipoCultivo" class="form-select" id="tipoCultivoEditar" aria-label="Tipo de Cultivo" required>
                  <option disabled selected>Selecione o tipo de cultivo</option>
                  <option v-for="tipo in tiposCultivo" :key="tipo" :value="tipo">{{ tipo }}</option>
                </select>
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
            Tem certeza de que deseja excluir este lote?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarLote()">Excluir</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaLotes',
  data() {
    return {
      lotes: [],
      tiposCultivo: ['Pastagem Natural', 'Lavoura', 'Confinamento'],
      formData: {
        id: null,
        nome: '',
        tipoCultivo: '',
        propriedade: localStorage.getItem('propriedadeSelecionada')
      },
      modalTitle: 'Cadastro de Lote',
    }
  },
  mounted() {
    this.buscarLotesDaApi();
  },
  methods: {
    async buscarLotesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/lotes/' , {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.lotes = response.data;
      } catch (error) {
        console.error('Erro ao buscar lotes da API:', error);
      }
    },
    editarLote(lote) {
      this.modalTitle = 'Editar Lote';
      this.formData = {
        id: lote.id,
        nome: lote.nome,
        tipoCultivo: lote.tipoCultivo,
        propriedade: localStorage.getItem('propriedadeSelecionada')
      };
    },
    resetForm() {
      this.formData = {
        id: null,
        nome: '',
        propriedade: localStorage.getItem('propriedadeSelecionada'),
        tipoCultivo: ''
      };
      this.modalTitle = 'Cadastro de Lote';
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async apagarLote() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/lotes/${this.formData.id}/` , {
        });

        if (response.status === 204) {
          alert('Lote apagado com sucesso!');
          this.buscarLotesDaApi();
        } else {
          alert('Erro ao apagar lote. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },
    
    async submitForm() {
      if (this.modalTitle === 'Cadastro de Lote') {
        try {
          const response = await api.post('http://127.0.0.1:8000/lotes/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarLotesDaApi();
          } else {
            alert('Erro ao cadastrar lote. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("cadastroModal");

      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/lotes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarLotesDaApi();
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
         this.fecharModal("edicaoModal");
      }
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
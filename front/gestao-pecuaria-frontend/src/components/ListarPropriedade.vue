<template>
  <!-- Modal de Propriedades -->
  <div class="modal" id="listModal" tabindex="-1" role="dialog" style="display: block;">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Selecione uma Propriedade</h5>
        </div>
        <div class="modal-body">
          <!-- Lista de propriedades -->
          <ul class="list-group">
            <li class="list-group-item" v-for="propriedade in propriedades" :key="propriedade.id">
              <button class="btn btn-link" @click="selecionarPropriedade(propriedade)">
                {{ propriedade.nome }}, {{ propriedade.cidade }}, {{ propriedade.estado }}
              </button>
            </li>
          </ul>
        </div>
        <div class="modal-footer">
          <button class="btn btn-link" @click="criarPropriedadeForm()">Criar Propriedade</button>
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
      formData: {
        id: null,
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
        produtor: [],
        componeteVisivel: false
      },
  };
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

    async mostrarComponente(){
      this.componeteVisivel = true;
    },

    async ocultarComponente(){
      this.componeteVisivel = false;
    },

    async fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
      this.mostrarComponente();
    },

    async selecionarPropriedade(propriedade) {
      // Salvar o ID da propriedade selecionada no localStorage
      localStorage.setItem('propriedadeSelecionada', propriedade.id);
      this.propriedades = [];
      // Fechar o modal de propriedades
      this.fecharModal("listModal")
      this.$router.push('/inicio');
  },
  criarPropriedadeForm() {
    this.$router.push('/cadastropropriedade');
    }
  }
};
</script>

<style>
/* Estilos para o modal */


.modal {
  display: none;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  position: relative;
  width: auto;
  margin: 10px auto;
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
  outline: 0;
}

.modal-header {
  padding: 15px;
  border-bottom: 1px solid #e9ecef;
  border-top-left-radius: 0.3rem;
  border-top-right-radius: 0.3rem;
}

.modal-title {
  margin-bottom: 0;
  line-height: 1.5;
}

.modal-body {
  position: relative;
  flex: 1 1 auto;
  padding: 15px;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 15px;
  border-top: 1px solid #e9ecef;
  border-bottom-right-radius: 0.3rem;
  border-bottom-left-radius: 0.3rem;
}
</style>
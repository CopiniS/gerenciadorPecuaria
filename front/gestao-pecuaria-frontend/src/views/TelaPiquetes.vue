<template>
  <div class="background">
    <LoadSpiner :isLoading="loadingDelete || loadingInicial" />

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'propriedades' }"
          id="nav-propriedades-tab"
          @click="selectTab('propriedades')"
          type="button"
          role="tab"
          aria-controls="nav-propriedades"
          aria-selected="true"
        >
          Lista de Propriedades
        </button>

        <button
          class="nav-link"
          :class="{ active: activeTab === 'piquetes' }"
          id="nav-piquetes-tab"
          @click="selectTab('piquetes')"
          type="button"
          role="tab"
          aria-controls="nav-piquetes"
          aria-selected="false"
        >
          Lista de Piquetes
        </button>
      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'propriedades' }"
        id="nav-propriedades"
        role="tabpanel"
        aria-labelledby="nav-propriedades-tab"
      ></div>
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'piquetes' }"
        id="nav-piquetes"
        role="tabpanel"
        aria-labelledby="nav-piquetes-tab"
      ></div>
    </div>

    <h2>Lista de Piquetes</h2>


      <div class="d-flex align-items-start table-container flex-column">
        <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario">
            <i class="fas fa-chevron-down"></i>
          </button>
        </div>
        <form
          @submit.prevent="aplicarFiltro"
          @keyup.enter="aplicarFiltro"
          class="row g-3 align-items-center"
          v-show="mostrarFormulario"
        >
          <div class="col-auto d-flex align-items-center">
            <label for="nome" class="form-label me-2">Nome</label>
            <input
              type="text"
              class="form-control input-consistente"
              id="nome"
              v-model="filtro.nome"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="tipoCultivo" class="form-label me-2"
              >Tipo de Cultivo</label
            >
            <select
              class="form-select select-consistente"
              id="tipoCultivo"
              v-model="filtro.tipoCultivo"
            >
              <option value="">Selecione o tipo</option>
              <option>Pastagem Natural</option>
              <option>Lavoura</option>
              <option>Confinamento</option>
            </select>
          </div>
          <div class="col-12 d-flex justify-content-start mt-3">
            <button class="btn btn-secondary me-2" @click="limparFiltro">
              Limpar
            </button>
            <button type="submit" class="btn btn-success">Filtrar</button>
          </div>
        </form>
      </div>

      <div>
        <div class="table-container">
          <div class="button-container">
            <button
              @click="acessarCadastro()"
              type="button"
              class="btn btn-success"
            >
              Cadastrar Piquete
            </button>
            <RelatorioPdf
              titulo="Relatório de Piquetes"
              :cabecalho="[
                'Produtor: ' + nomeProdutor,
                'Propriedade: ' + propriedadeAtualNome,
              ]"
              :colunas="['Nome do Piquete', 'Tipo de Cultivo', 'Área']"
              :dados="
                piquetes.map((piquete) => [
                  piquete.nome,
                  piquete.tipoCultivo,
                  piquete.area,
                ])
              "
              :mostrarSoma="true"
            />
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Nome</th>
                <th scope="col">Tipo de Cultivo</th>
                <th scope="col">Área</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(piquete, index) in piquetes" :key="index">
                <td>{{ piquete.nome }}</td>
                <td>{{ piquete.tipoCultivo }}</td>
                <td>{{ piquete.area }}</td>
                <td>
                  <button
                    @click="acessarEdicao(piquete)"
                    class="btn-acoes btn-sm"
                    title="Editar Piquete"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button
                    @click="confirmarExclusao(piquete)"
                    class="btn-acoes btn-sm"
                    data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal"
                    title="Excluir Piquete"
                  >
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Modal de Confirmação de Exclusão -->
        <div
          class="modal fade"
          id="confirmacaoExclusaoModal"
          tabindex="-1"
          aria-labelledby="confirmacaoExclusaoModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">
                  Confirmação de Exclusão
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Tem certeza de que deseja excluir este Piquete?
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="apagarPiquete()"
                >
                  Excluir
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import api from "/src/interceptadorAxios";
import RelatorioPdf from "../components/RelatorioPdf.vue";
import LoadSpiner from "../components/LoadSpiner.vue";

export default {
  components: {
    RelatorioPdf,
    LoadSpiner,
  },
  data() {
    return {
      activeTab: "piquetes",
      piquetes: [],
      piquetesDaApi: [],
      propriedadeAtualNome: localStorage.getItem("propriedadeSelecionadaNome"),
      nomeProdutor: localStorage.getItem("produtorNome"),
      formData: {
        id: null,
        nome: "",
        tipoCultivo: "",
        area: "",
        propriedade: localStorage.getItem("propriedadeSelecionada"),
      },
      mostrarFormulario: false,
      filtro: {
        nome: "",
        tipoCultivo: "",
      },
      loadingInicial: true,
      loadingDelete: false,
    };
  },
  mounted() {
    this.buscarPiquetesDaApi();
  },
  methods: {
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === "propriedades") {
        this.$router.push("/propriedades");
      }
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get("http://127.0.0.1:8000/piquetes/", {
          params: {
            propriedadeSelecionada: localStorage.getItem(
              "propriedadeSelecionada"
            ),
          },
        });
        this.piquetesDaApi = response.data;
        this.piquetes = this.piquetesDaApi;
        this.loadingInicial = false;
      } catch (error) {
        console.error("Erro ao buscar piquetes da API:", error);
      }
    },

    acessarEdicao(piquete) {
      this.$router.push({
        name: "PiqueteEdicao",
        params: { piqueteId: piquete.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "PiqueteCadastro",
      });
    },

    fecharModal(modalId) {
      var closeButton = document
        .getElementById(modalId)
        .querySelector(".btn-close");
      if (closeButton) {
        closeButton.click();
      } else {
        console.error("Botão de fechar não encontrado no modal:", modalId);
      }
    },

    confirmarExclusao(piquete) {
      this.formData = {
        id: piquete.id,
      };
    },

    async apagarPiquete() {
      this.loadingDelete = true;
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/piquetes/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          this.loadingDelete = false;

          setTimeout(() => {
            
            alert("Exclusão realizada com sucesso!");
            this.buscarPiquetesDaApi();
          }, 100);
        } else {
          this.loadingDelete = false;
          alert("Erro ao apagar piquete. Tente novamente mais tarde.");
        }
      } catch (error) {
        this.loadingDelete = false;
        console.error("Erro ao enviar requisição:", error);
        alert(
          "Erro ao enviar requisição. Verifique o console para mais detalhes."
        );
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    aplicarFiltro() {
      this.piquetes = this.piquetesDaApi.filter((piquete) => {
        return (
          piquete.nome.toLowerCase().includes(this.filtro.nome) &&
          piquete.tipoCultivo.includes(this.filtro.tipoCultivo)
        );
      });
    },

    limparFiltro() {
      this.filtro.nome = "";
      this.filtro.tipoCultivo = "";
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },
  },
};
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  /*z-index: 0;  /*Garante que a imagem de fundo fique na camada mais baixa */
}

.background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("../assets/logo-sem-fundo.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}

nav,
.tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
}

.table-container,
.button-container {
  position: relative;
  z-index: 1; /* Garante que as tabelas e botões estejam acima da imagem de fundo */
}

.table-container table tbody tr td {
  background-color: transparent !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  /* Adiciona uma borda verde na parte inferior */
  background-color: transparent !important;
}

.button-container {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
  margin-bottom: 20px;
  white-space: nowrap;
}

.btn-success {
  margin-right: 10px;
  margin-bottom: 10px;
  z-index: 2; /* Garante que o botão esteja acima da imagem */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  z-index: 2; /* Garante que o botão de ação esteja acima da imagem */
}

.btn-acoes i {
  color: #176d1a;
}
.button-group {
  display: flex;
  gap: 10px;
}

.button-container {
  display: flex;
  flex-wrap: nowrap; /* Garante que os botões não vão para a linha seguinte */
  gap: 10px; /* Espaço entre os botões */
  margin-bottom: 20px;
  white-space: nowrap; /* Evita quebras de linha nos botões */
}

.input-consistente,
.select-consistente {
  width: 200px;
}
</style>

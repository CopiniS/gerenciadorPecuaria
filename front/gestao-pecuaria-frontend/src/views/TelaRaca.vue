<template>
  <div class="background">
    <LoadSpiner :isLoading="loadingDelete || loadingInicial" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'animais' }"
          id="nav-animais-tab"
          @click="selectTab('animais')"
          type="button"
          role="tab"
          aria-controls="nav-animais"
          aria-selected="true"
        >
          Lista de Animais
        </button>
        <button
          class="nav-link"
          :class="{ active: activeTab === 'racas' }"
          id="nav-cadastro-tab"
          @click="selectTab('racas')"
          type="button"
          role="tab"
          aria-controls="nav-cadastro"
          aria-selected="false"
        >
          Lista de Raças
        </button>
      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'animais' }"
        id="nav-animais"
        role="tabpanel"
        aria-labelledby="nav-animais-tab"
      ></div>
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'racas' }"
        id="nav-cadastro"
        role="tabpanel"
        aria-labelledby="nav-cadastro-tab"
      >
        <div
          id="cadastro"
          tabindex="-1"
          aria-labelledby="cadastroLabel"
          aria-hidden="true"
        >
          <h2>Lista de Racas</h2>

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
                    Cadastrar Raca
                  </button>
                  <RelatorioPdf
                    titulo="Relatório de Raças"
                    :cabecalho="['Nome do produtor: ' + nomeProdutor]"
                    :colunas="['Nome da Raça']"
                    :dados="racas.map((raca) => [raca.nome])"
                    :mostrarSoma="false"
                  />
                </div>
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">Nome</th>
                      <th scope="col">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(raca, index) in racas" :key="index">
                      <td>{{ raca.nome }}</td>
                      <td>
                        <button
                          @click="acessarEdicao(raca)"
                          class="btn-acoes btn-sm"
                          title="Editar Raça"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button
                          @click="confirmarExclusao(raca)"
                          class="btn-acoes btn-sm"
                          data-bs-toggle="modal"
                          data-bs-target="#confirmacaoExclusaoModal"
                          title="Excluir Raça"
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
                      <h5
                        class="modal-title"
                        id="confirmacaoExclusaoModalLabel"
                      >
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
                      Tem certeza de que deseja excluir esta Raca?
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
                        @click="apagarRaca()"
                      >
                        Excluir
                      </button>
                    </div>
                  </div>
                </div>
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
      activeTab: "racas",
      racas: [],
      racasDaApi: [],
      nomeProdutor: localStorage.getItem("produtorNome"),
      mostrarFormulario: false,
      formData: {
        id: null,
        nome: "",
      },
      filtro: {
        nome: "",
      },
      loadingInicial: true,
      loadingDelete: false,
    };
  },
  mounted() {
    this.buscarRacasDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarRacasDaApi() {
      try {
        const response = await api.get("http://127.0.0.1:8000/racas/");
        this.racasDaApi = response.data;
        this.racas = this.racasDaApi;
        this.loadingInicial = false;
      } catch (error) {
        console.error("Erro ao buscar raças da API:", error);
      }
    },

    async apagarRaca() {
      this.loadingDelete = true;
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/racas/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          this.loadingDelete = false;
          setTimeout(() => {
            alert("Exclusão realizada com sucesso!");
            this.buscarRacasDaApi();
          }, 100);
        } else {
          this.loadingDelete = false;
          alert("Erro ao apagar raca. Tente novamente mais tarde.");
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

    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.racas = this.racasDaApi.filter((raca) => {
        return raca.nome.toLowerCase().includes(this.filtro.nome);
      });
    },

    limparFiltro() {
      this.filtro.nome = "";
      this.racas = this.racasDaApi;
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === "animais") {
        this.$router.push("/animais");
      }
    },

    acessarEdicao(raca) {
      this.$router.push({
        name: "RacaEdicao",
        params: { racaId: raca.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "RacaCadastro",
        params: { animalJSON: "racasLista" },
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

    confirmarExclusao(raca) {
      this.formData = {
        id: raca.id,
      };
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
  position: relative; /* Permite que os elementos filhos usem posição absoluta */
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
  background-size: 40%; /* Ajuste o tamanho da imagem conforme necessário */
  opacity: 0.1; /* Define a opacidade para criar o efeito de marca d'água */
  z-index: 0; /* Garante que a imagem fique atrás do conteúdo */
}

nav,
.tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
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
  background-color: transparent !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  /* Adiciona uma borda verde na parte inferior */
  background-color: transparent !important;
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

.input-consistente {
  width: 200px;
}

.button-container {
  display: flex;
  flex-wrap: nowrap; /* Garante que os botões não vão para a linha seguinte */
  gap: 10px; /* Espaço entre os botões */
  margin-bottom: 20px;
  white-space: nowrap; /* Evita quebras de linha nos botões */
}
</style>

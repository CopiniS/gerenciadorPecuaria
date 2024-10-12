<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button
          class="nav-link active"
          id="nav-vet-tab"
          data-bs-toggle="tab"
          data-bs-target="#nav-vet"
          type="button"
          role="tab"
          aria-controls="nav-vet"
          aria-selected="true"
        >
          Lista de Veterinários
        </button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div
        class="tab-pane fade show active"
        id="nav-home"
        role="tabpanel"
        aria-labelledby="nav-vet-tab"
        tabindex="0"
      ></div>
    </div>

    <h2>Lista de Veterinários</h2>

    <!-- Exibe o skeleton enquanto carrega os dados -->
    <SkeletonListagem v-if="loading" />

    <div v-else>
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
            <button @click="acessarCadastro()" class="btn btn-success">
              Cadastrar Veterinário
            </button>
            <RelatorioPdf
              titulo="Relatório de Veterinário"
              :cabecalho="['Produtor: ' + nomeProdutor]"
              :colunas="['Nome', 'Telefone', 'Email', 'CRMV']"
              :dados="
                veterinarios.map((veterinario) => [
                  veterinario.nome,
                  veterinario.telefone,
                  veterinario.email,
                  veterinario.crmv,
                ])
              "
              :mostrarSoma="false"
            />
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Nome</th>
                <th scope="col">Telefone</th>
                <th scope="col">Email</th>
                <th scope="col">CRMV</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(veterinario, index) in veterinarios" :key="index">
                <td>{{ veterinario.nome }}</td>
                <td>{{ veterinario.telefone }}</td>
                <td>{{ veterinario.email }}</td>
                <td>{{ veterinario.crmv }}</td>
                <td>
                  <button
                    @click="acessarEdicao(veterinario)"
                    class="btn-acoes btn-sm"
                    title="Editar Veterinário"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button
                    @click="confirmarExclusao(veterinario)"
                    class="btn-acoes btn-sm"
                    data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal"
                    title="Excluir Veterinário"
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
                Tem certeza de que deseja excluir este veterinário?
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
                  @click="apagarVeterinario()"
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
</template>
  
  <script>
import api from "/src/interceptadorAxios";
import RelatorioPdf from "../components/RelatorioPdf.vue";
import SkeletonListagem from "../components/SkeletonListagem.vue";

export default {
  components: {
    RelatorioPdf,
    SkeletonListagem,
  },
  name: "TelaVeterinarios",
  data() {
    return {
      veterinarios: [],
      veterinariosDaApi: [],
      nomeProdutor: localStorage.getItem("produtorNome"),
      formData: {
        id: null,
        nome: "",
        telefone: "",
        email: "",
        crmv: "",
      },
      mostrarFormulario: false,
      filtro: {
        nome: "",
      },
      loading: true,
    };
  },
  mounted() {
    this.buscarVeterinariosDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarVeterinariosDaApi() {
      try {
        const response = await api.get("http://127.0.0.1:8000/veterinarios/", {
          // Parâmetros da requisição (se houver)
        });
        this.veterinariosDaApi = response.data;
        this.veterinarios = this.veterinariosDaApi;
        this.loading = false;
      } catch (error) {
        console.error("Erro ao buscar veterinários da API:", error);
      }
    },

    async apagarVeterinario() {
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/veterinarios/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          alert("Exclusão realizada com sucesso!");
          this.buscarVeterinariosDaApi();
        } else {
          alert("Erro ao apagar veterinário. Tente novamente mais tarde.");
        }
      } catch (error) {
        console.error("Erro ao enviar requisição:", error);
        alert(
          "Erro ao enviar requisição. Verifique o console para mais detalhes."
        );
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    //FILTROS-------------------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.veterinarios = this.veterinariosDaApi.filter((veterinario) =>
        veterinario.nome.toLowerCase().includes(this.filtro.nome)
      );
    },

    limparFiltro() {
      this.filtro.nome = "";
      this.veterinarios = this.veterinariosDaApi;
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    acessarEdicao(veterinario) {
      this.$router.push({
        name: "VeterinarioEdicao",
        params: { veterinarioId: veterinario.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "VeterinarioCadastro",
      });
    },

    confirmarExclusao(veterinario) {
      this.formData = {
        id: veterinario.id,
      };
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
  z-index: 0; /* Garante que a imagem de fundo fique na camada mais baixa */
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

.input-consistente,
.select-consistente {
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
  
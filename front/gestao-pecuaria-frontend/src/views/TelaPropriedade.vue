<template>
  <div class="background">
    <LoadSpinner :isLoading="loadingDelete || loadingInicial" />
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" data-bs-target="#nav-vet" type="button"
          role="tab" aria-controls="nav-vet" aria-selected="true">
          Lista de Propriedades
        </button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0">
      </div>
    </div>

    <h2>Lista de Propriedades</h2>

      <div class="d-flex align-items-start table-container flex-column">
        <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario">
            <i class="fas fa-chevron-down"></i>
          </button>
        </div>
        <form @submit.prevent="aplicarFiltro" @keyup.enter="aplicarFiltro" class="row g-3 align-items-center"
          v-show="mostrarFormulario">
          <div class="col-auto d-flex align-items-center">
            <label for="nome" class="form-label me-2">Nome</label>
            <input type="text" class="form-control input-consistente" id="nome" v-model="filtro.nome" />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="cidade" class="form-label me-2">Cidade</label>
            <input type="text" class="form-control input-consistente" id="cidade" v-model="filtro.cidade" />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="estado" class="form-label me-2">Estado</label>
            <input type="text" class="form-control input-consistente" id="estado" v-model="filtro.estado" />
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
            <button @click="acessarCadastro()" type="button" class="btn btn-success">
              Cadastrar Propriedade
            </button>
            <button @click="() => {
                this.$router.push('/piquetes');
              }
              " type="button" class="btn btn-success">
              Lista de Piquetes
            </button>
            <RelatorioPdf titulo="Relatório de Propriedades" :cabecalho="['Produtor: ' + nomeProdutor]" :colunas="[
              'Nome',
              'Endereço',
              'Cidade',
              'Estado',
              'Latitude',
              'Longitude',
              'Área',
            ]" :dados="propriedades.map((propriedade) => [
                propriedade.nome,
                propriedade.endereco,
                propriedade.cidade,
                propriedade.estado,
                formatarValor(replacePontoVirgula(propriedade.latitude)),
                formatarValor(replacePontoVirgula(propriedade.longitude)),
                formatarValor(replacePontoVirgula(propriedade.area)),
              ])
                " :mostrarSoma="true" />
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
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(propriedade, index) in propriedades" :key="index">
                <td>{{ propriedade.nome }}</td>
                <td>{{ propriedade.cidade }}</td>
                <td>{{ propriedade.estado }}</td>
                <td>{{ propriedade.endereco }}</td>
                <td>
                  {{ formatarValor(replacePontoVirgula(propriedade.latitude)) }}
                </td>
                <td>
                  {{
                    formatarValor(replacePontoVirgula(propriedade.longitude))
                  }}
                </td>
                <td>
                  {{ formatarValor(replacePontoVirgula(propriedade.area)) }}
                </td>
                <td>
                  <button v-if="propriedadeAtualId == propriedade.id" @click="acessarEdicao(propriedade)"
                    class="btn-acoes btn-sm" title="Editar Propriedade">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button v-if="propriedadeAtualId == propriedade.id" @click="confirmarExclusao(propriedade)"
                    class="btn-acoes btn-sm" data-bs-toggle="modal" title="Excluir Propriedade"
                    data-bs-target="#confirmacaoExclusaoModal">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                  <button v-if="propriedadeAtualId != propriedade.id" @click="trocaPropriedade(propriedade.id)"
                    class="btn-acoes btn-sm" title="Trocar Propriedade">
                    <i class="fas fa-exchange-alt"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Modal de Confirmação de Exclusão -->
        <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
          aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">
                  Confirmação de Exclusão
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                Tem certeza de que deseja excluir esta Propriedade?
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Cancelar
                </button>
                <button type="button" class="btn btn-danger" @click="apagarPropriedade()">
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
import LoadSpinner from "../components/LoadSpiner.vue";

export default {
  components: {
    RelatorioPdf,
    LoadSpinner,
  },
  data() {
    return {
      propriedades: [],
      propriedadesDaApi: [],
      propriedadeAtualId: localStorage.getItem("propriedadeSelecionada"),
      nomeProdutor: localStorage.getItem("produtorNome"),
      formData: {
        id: null,
        nome: "",
        endereco: "",
        estado: "",
        cidade: "",
        latitude: "",
        longitude: "",
        area: "",
      },
      mostrarFormulario: false,
      filtro: {
        nome: "",
        cidade: "",
        estado: "",
      },
      loadingInicial: true,
      loadingDelete: false,
    };
  },
  mounted() {
    this.buscarPropriedadesDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarPropriedadesDaApi() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/propriedades/",
          {}
        );
        this.propriedadesDaApi = response.data;
        this.propriedades = this.propriedadesDaApi;
        this.loadingInicial = false;
      } catch (error) {
        console.error("Erro ao buscar propriedades da API:", error);
      }
    },

    async apagarPropriedade() {
      this.loadingDelete = true;
      
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/propriedades/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          this.loadingDelete = false;
          setTimeout(() => {
            alert("Exclusão realizada com sucesso!");
            this.buscarPropriedadesDaApi();
          }, 100);
        } else {
          this.loadingDelete = false;
          alert("Erro ao apagar propriedade. Tente novamente mais tarde.");
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
      this.propriedades = this.propriedadesDaApi.filter((propriedade) => {
        return (
          propriedade.nome.toLowerCase().includes(this.filtro.nome) &&
          propriedade.cidade
            .toLowerCase()
            .includes(this.filtro.cidade.toLowerCase()) &&
          propriedade.estado
            .toLowerCase()
            .includes(this.filtro.estado.toLowerCase())
        );
      });
    },

    limparFiltro() {
      this.filtro.nome = "";
      this.filtro.cidade = "";
      this.filtro.estado = "";
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    acessarEdicao(propriedade) {
      this.$router.push({
        name: "PropriedadeEdicao",
        params: { propriedadeId: propriedade.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "PropriedadeCadastro",
      });
    },

    trocaPropriedade(propriedadeId) {
      localStorage.setItem("propriedadeSelecionada", propriedadeId);
      window.location.reload();
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

    confirmarExclusao(propriedade) {
      this.formData = {
        id: propriedade.id,
      };
    },

    replacePontoVirgula(valorString) {
      if (typeof valorString === "string") {
        valorString = valorString.replace(".", ",");
      } else {
        valorString = "-";
      }
      return valorString;
    },

    formatarValor(valor) {
      if (typeof valor !== "number") {
        valor = parseFloat(valor);
      }
      return valor.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
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
}

nav,
.tab-content {
  position: relative;
  z-index: 1;
  /* Coloca o conteúdo acima da marca d'água */
}

.table-container,
.button-container {
  position: relative;
  z-index: 1;
  /* Garante que as tabelas e botões estejam acima da imagem de fundo */
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
  z-index: 2;
  /* Garante que o botão esteja acima da imagem */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  z-index: 2;
  /* Garante que o botão de ação esteja acima da imagem */
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

.btn {
  margin-bottom: 0;
}
</style>

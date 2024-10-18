<template>
  <div class="background">
    <LoadSpiner :isLoading="loadingDelete || loadingInicial" />
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
          Lista de Vendas
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

    <h2>Lista de Vendas</h2>

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
            <label for="dataVenda" class="form-label me-2">Data</label>
            <DateRangePicker
              ref="dateRangePicker"
              class="input-consistente"
              :startDate="filtro.dataVendaInicio"
              :endDate="filtro.dataVendaFim"
              @update:startDate="(val) => (filtro.dataVendaInicio = val)"
              @update:endDate="(val) => (filtro.dataVendaFim = val)"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Animal</label>
            <input
              type="text"
              class="form-control input-consistente"
              id="animal"
              v-model="filtro.animal"
              @input="aplicarBrincoMask"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Piquete</label>
            <input
              type="text"
              class="form-control input-consistente"
              id="piquete"
              v-model="filtro.piquete"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Peso</label>
            <input
              type="text"
              class="form-control input-consistente"
              id="pesoInicio"
              v-model="filtro.pesoInicio"
              @input="aplicarPesoInicioMask"
              placeholder="Inicial"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <input
              type="text"
              class="form-control input-consistente"
              id="pesoFim"
              v-model="filtro.pesoFim"
              @input="aplicarPesoFimMask"
              placeholder="Final"
            />
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="tipo" class="form-label me-2">Finalidade</label>
            <select
              class="form-select select-consistente"
              id="finalidade"
              v-model="filtro.finalidade"
            >
              <option value=""></option>
              <option value="Cria">Cria</option>
              <option value="Recria">Recria</option>
              <option value="Engorda">Engorda</option>
              <option value="Abate">Abate</option>
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
              Cadastrar Venda
            </button>
            <RelatorioPdf
              titulo="Relatório de Venda"
              :cabecalho="[
                'Nome do produtor: ' + nomeProdutor,
                'Propriedade: ' + propriedadeAtual,
              ]"
              :colunas="[
                'Brinco',
                'Data da venda',
                'Peso',
                'Preço por Kg',
                'Valor Total',
              ]"
              :dados="
                vendas.map((venda) => [
                  venda.animal.brinco,
                  formatarData(venda.dataVenda),
                  venda.peso,
                  venda.precoKg,
                  venda.valorTotal,
                ])
              "
              :mostrarSoma="true"
            />
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Data</th>
                <th scope="col">Animal</th>
                <th scope="col">Piquete</th>
                <th scope="col">Finalidade</th>
                <th scope="col">Peso</th>
                <th scope="col">Preço do Kg</th>
                <th scope="col">Valor total</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(venda, index) in vendas" :key="index">
                <td>{{ formatarData(venda.dataVenda) }}</td>
                <td>{{ venda.animal.brinco }}</td>
                <td>{{ venda.animal.piquete.nome }}</td>
                <td>{{ venda.finalidade }}</td>
                <td>{{ formatarValor(venda.peso) }}</td>
                <td>{{ formatarValor(venda.precoKg) }}</td>
                <td>{{ formatarValor(venda.valorTotal) }}</td>
                <td>
                  <button
                    @click="acessarEdicao(venda)"
                    class="btn-acoes btn-sm"
                    title="Editar Venda"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button
                    @click="confirmarExclusaoVenda(venda)"
                    class="btn-acoes btn-sm"
                    data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal"
                    title="Excluir Venda"
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
                Tem certeza de que deseja excluir esta Venda?
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
                  @click="apagarVenda()"
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
import { masksMixin } from "../mixins/maks";
import DateRangePicker from "../components/DateRangePicker.vue";
import RelatorioPdf from "../components/RelatorioPdf.vue";
import LoadSpiner from "../components/LoadSpiner.vue";

export default {
  mixins: [masksMixin],
  components: {
    DateRangePicker,
    RelatorioPdf,
    LoadSpiner,
  },

  data() {
    return {
      propriedadeAtual: localStorage.getItem("propriedadeSelecionadaNome"),
      nomeProdutor: localStorage.getItem("produtorNome"),
      vendas: [],
      vendasDaApi: [],
      formData: {
        id: null,
        animal: "",
        dataVenda: "",
        peso: "",
        precoKg: "",
        valorTotal: "",
        finalidade: "",
        observacao: null,
      },
      mostrarFormulario: false,
      filtro: {
        dataVendaInicio: "",
        dataVendaFim: "",
        animal: "",
        piquete: "",
        pesoInicio: "",
        pesoFim: "",
        finalidade: "",
      },
      loadingInicial: true,
      loadingDelete: false,
    };
  },
  mounted() {
    this.buscarVendasDaApi();
  },
  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(event) {
      const value = event.target.value;
      this.filtro.animal = this.brincoFiltroMask(value);
    },

    aplicarPesoInicioMask(event) {
      const value = event.target.value;
      this.filtro.pesoInicio = this.valorMask(value);
    },

    aplicarPesoFimMask(event) {
      const value = event.target.value;
      this.filtro.pesoFim = this.valorMask(value);
    },

    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarVendasDaApi() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/vendas-animais/",
          {
            params: {
              propriedadeSelecionada: localStorage.getItem(
                "propriedadeSelecionada"
              ),
            },
          }
        );
        this.vendasDaApi = response.data;
        this.vendas = this.vendasDaApi;
        this.loadingInicial = false;
      } catch (error) {
        console.error("Erro ao buscar vendas da API:", error);
      }
    },

    async apagarVenda() {
      this.loadingDelete = true;
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/vendas-animais/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          this.loadingDelete = false;
          setTimeout(() => {
            alert("Exclusão realizada com sucesso!");
            this.buscarVendasDaApi();
          }, 100);
        } else {
          this.loadingDelete = false;
          alert("Erro ao excluir vendas. Tente novamente mais tarde.");
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
      this.vendas = this.vendasDaApi.filter((venda) => {
        return (
          new Date(venda.dataVenda) >=
            new Date(this.filtro.dataVendaInicio || "1970-01-01") &&
          new Date(venda.dataVenda) <=
            new Date(this.filtro.dataVendaFim || "9999-12-31") &&
          (venda.peso >= parseFloat(this.filtro.pesoInicio) ||
            this.filtro.pesoInicio == "") &&
          (venda.peso <= parseFloat(this.filtro.pesoFim) ||
            this.filtro.pesoFim == "") &&
          venda.animal.brinco.includes(this.filtro.animal) &&
          venda.animal.piquete.nome.includes(this.filtro.piquete) &&
          venda.finalidade.includes(this.filtro.finalidade)
        );
      });
    },

    limparFiltro() {
      this.filtro.dataVendaInicio = "";
      this.filtro.dataVendaFim = "";
      this.filtro.animal = "";
      this.filtro.piquete = "";
      this.filtro.pesoInicio = "";
      this.filtro.pesoFim = "";
      this.filtro.finalidade = "";

      this.vendas = this.vendasDaApi;

      // Resetando as datas no DateRangePicker
      this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    acessarEdicao(venda) {
      this.$router.push({
        name: "VendaAnimalEdicao",
        params: { vendaId: venda.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "VendaAnimalCadastro",
      });
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(
        date.getUTCFullYear(),
        date.getUTCMonth(),
        date.getUTCDate()
      );
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        timeZone: "UTC",
      };
      return utcDate.toLocaleDateString("pt-BR", options);
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

    confirmarExclusaoVenda(venda) {
      this.formData.id = venda.id;
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
</style>
  
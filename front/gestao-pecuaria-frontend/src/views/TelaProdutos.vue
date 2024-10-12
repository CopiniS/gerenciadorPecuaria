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
          Lista de Produtos
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

    <h2>Lista de Produtos</h2>

    <!-- Exibe o skeleton enquanto carrega os dados -->
    <SkeletonListagem v-if="loadingProdutos || loadingEstoque" />

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
          <div class="col-auto d-flex align-items-center">
            <label for="tipo" class="form-label me-2">Tipo</label>
            <select
              class="form-select select-consistente"
              id="tipo"
              v-model="filtro.tipo"
            >
              <option value="">Selecione o tipo</option>
              <option value="alimenticio">Alimentício</option>
              <option value="sanitario">Sanitário</option>
            </select>
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="categoria" class="form-label me-2">Categoria</label>
            <input
              type="text"
              class="form-control input-consistente"
              id="categoria"
              v-model="filtro.categoria"
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
              Cadastrar Produto
            </button>
            <button
              @click="
                () => {
                  this.$router.push('/compraprodutos');
                }
              "
              type="button"
              class="btn btn-success"
            >
              Histórico de Compras
            </button>

            <button
              @click="buscarEstoqueGeral"
              type="button"
              class="btn btn-success"
              data-bs-toggle="modal"
              data-bs-target="#escolhaRelatorioModal"
            >
              Gerar Relatório
            </button>
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Nome</th>
                <th scope="col">Tipo</th>
                <th scope="col">Categoria</th>
                <th scope="col">Estoque</th>
                <th scope="col">Unidade</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(produto, index) in produtos" :key="index">
                <td>{{ produto.nome }}</td>
                <td>{{ produto.tipo }}</td>
                <td>{{ produto.categoria }}</td>
                <td
                  :class="{
                    'is-invalid': achaEstoque(produto.id, estoque) <= 0,
                  }"
                >
                  {{
                    replacePontoVirgula(
                      achaEstoque(produto.id, estoque).toString()
                    )
                  }}
                </td>
                <td>{{ produto.unidade }}</td>
                <td>
                  <button
                    @click="acessarEdicao(produto)"
                    class="btn-acoes btn-sm"
                    title="Editar Produto"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button
                    @click="confirmarExclusao(produto)"
                    class="btn-acoes btn-sm"
                    data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal"
                    title="Excluir Produto"
                  >
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Modal para escolher o tipo de relatório -->
        <div
          class="modal fade"
          id="escolhaRelatorioModal"
          tabindex="-1"
          aria-labelledby="escolhaRelatorioModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="escolhaRelatorioModalLabel">
                  Escolha o Tipo de Relatório
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="mostrarRelatorio">
                  <div class="mb-3">
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="radio"
                        name="tipoRelatorio"
                        id="relatorioGeral"
                        value="geral"
                        v-model="tipoRelatorio"
                      />
                      <label class="form-check-label" for="relatorioGeral">
                        Relatório de Estoque de Produto Geral
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="radio"
                        name="tipoRelatorio"
                        id="relatorioPorPropriedade"
                        value="porPropriedade"
                        v-model="tipoRelatorio"
                      />
                      <label
                        class="form-check-label"
                        for="relatorioPorPropriedade"
                      >
                        Relatório de Estoque de Produto por Propriedade
                      </label>
                    </div>
                  </div>
                </form>

                <!-- Relatório de Estoque de Produto Geral -->
                <div v-if="tipoRelatorio === 'geral'">
                  <RelatorioPdf
                    titulo="Relatório de Estoque de Produto Geral"
                    :cabecalho="['Nome do produtor: ' + nomeProdutor]"
                    :colunas="[
                      'Nome do Produto',
                      'Categoria',
                      'Quantidade em Estoque',
                    ]"
                    :dados="
                      produtos.map((produto) => [
                        produto.nome,
                        produto.categoria,
                        achaEstoque(produto.id, estoqueGeral),
                      ])
                    "
                    :mostrarSoma="true"
                  />
                </div>

                <!-- Relatório de Estoque de Produto por Propriedade -->
                <div v-if="tipoRelatorio === 'porPropriedade'">
                  <RelatorioPdf
                    titulo="Relatório de Estoque de Produto por Propriedade"
                    :cabecalho="[
                      'Nome do produtor: ' + nomeProdutor,
                      'Propriedade: ' + propriedadeAtualNome,
                    ]"
                    :colunas="[
                      'Nome do Produto',
                      'Categoria',
                      'Quantidade em Estoque',
                    ]"
                    :dados="
                      produtos.map((produto) => [
                        produto.nome,
                        produto.categoria,
                        achaEstoque(produto.id, estoque),
                      ])
                    "
                    :mostrarSoma="false"
                  />
                </div>
              </div>
            </div>
          </div>
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
                Tem certeza de que deseja excluir este Produto?
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
                  @click="apagarProduto()"
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
  data() {
    return {
      produtos: [],
      produtosDaApi: [],
      estoque: [],
      tipoRelatorio: null,
      estoqueGeral: [],
      propriedadeAtualNome: localStorage.getItem("propriedadeSelecionadaNome"),
      nomeProdutor: localStorage.getItem("produtorNome"),
      formData: {
        id: null,
        nome: "",
        tipo: "",
        categoria: "",
        descricao: null,
      },
      mostrarFormulario: false,
      filtro: {
        nome: "",
        tipo: "",
        categoria: "",
      },
      loadingProdutos: true,
      loadingEstoque: true,
    };
  },
  mounted() {
    this.buscarProdutosDaApi();
    this.buscarEstoqueDaApi();
  },
  methods: {
    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarProdutosDaApi() {
      try {
        const response = await api.get("http://127.0.0.1:8000/produtos/", {
          // Parâmetros da requisição (se houver)
        });
        this.produtosDaApi = response.data;
        this.produtos = this.produtosDaApi;
        this.loadingProdutos = false;
      } catch (error) {
        console.error("Erro ao buscar produtos da API:", error);
      }
    },

    async buscarEstoqueDaApi() {
      try {
        const response = await api.get("http://127.0.0.1:8000/estoque/", {
          params: {
            propriedadeSelecionada: localStorage.getItem(
              "propriedadeSelecionada"
            ),
          },
        });
        this.estoque = response.data;
        this.loadingEstoque = false;
      } catch (error) {
        console.error("Erro ao buscar estoque da API:", error);
      }
    },

    async buscarEstoqueGeral() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/estoque/geral",
          {}
        );
        this.estoqueGeral = response.data;
      } catch (error) {
        console.error("Erro ao buscar estoque da API:", error);
      }
    },

    async apagarProduto() {
      try {
        const response = await api.delete(
          `http://127.0.0.1:8000/produtos/${this.formData.id}/`,
          {}
        );

        if (response.status === 204) {
          alert("Exclusão realizada com sucesso!");
          this.buscarProdutosDaApi();
        } else {
          alert("Erro ao apagar produto. Tente novamente mais tarde.");
        }
      } catch (error) {
        console.error("Erro ao enviar requisição:", error);
        alert(
          "Erro ao enviar requisição. Verifique o console para mais detalhes."
        );
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.produtos = this.produtosDaApi.filter((produto) => {
        if (produto.categoria == null) {
          produto.categoria = "";
        }

        return (
          produto.nome.toLowerCase().includes(this.filtro.nome) &&
          produto.tipo.includes(this.filtro.tipo) &&
          produto.categoria.toLowerCase().includes(this.filtro.categoria)
        );
      });
    },

    limparFiltro() {
      this.filtro.nome = "";
      this.filtro.tipo = "";
      this.filtro.categoria = "";
      this.produtos = this.produtosDaApi;
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    //FUNÇÕES AUXILIARES---------------------------------------------------------------------------------------------------------------------
    achaEstoque(produtoId, estoque) {
      let quantidade = 0;
      estoque.forEach((e) => {
        if (e.produto == produtoId) {
          quantidade = quantidade + e.quantidade;
        }
      });
      if (!quantidade) {
        quantidade = 0;
      }
      return quantidade;
    },

    acessarEdicao(produto) {
      this.$router.push({
        name: "ProdutoEdicao",
        params: { produtoId: produto.id },
      });
    },

    acessarCadastro() {
      this.$router.push({
        name: "ProdutoCadastro",
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

    confirmarExclusao(produto) {
      this.formData = {
        id: produto.id,
      };
    },

    replacePontoVirgula(valorString) {
      valorString = valorString.replace(".", ",");

      return valorString;
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
}

.table-container,
.button-container {
  position: relative;
  z-index: 1;
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
  /* z-index: 2;  */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  /* z-index: 2;  */
}

.btn-acoes i {
  color: #176d1a;
}

.btn-success {
  margin-right: 10px;
  margin-bottom: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  color: #ff0015;
}

.input-consistente,
.select-consistente {
  width: 200px;
}

.btn {
  margin-bottom: 0;
}

.form-check-label:hover {
  cursor: pointer;
  font-weight: bold; /* Deixa o texto em negrito */
  color: #007bff; /* Altera a cor do texto para destacar (você pode escolher qualquer cor) */
}

.form-check-input:hover {
  cursor: pointer;
}

.form-check-input:hover ~ .form-check-label {
  font-weight: bold; /* Deixa o texto em negrito */
  color: #007bff; /* Altera a cor do texto */
}

.form-check-input:checked ~ .form-check-label {
  font-weight: bold; /* Deixa o texto em negrito */
  color: #007bff; /* Altera a cor do texto */
}
</style>

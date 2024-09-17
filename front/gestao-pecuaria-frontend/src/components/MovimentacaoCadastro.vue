<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'movimentacoes' }"
          id="nav-vet-tab"
          @click="selectTab('movimentacoes')"
          type="button"
          role="tab"
          aria-controls="nav-vet"
          aria-selected="true"
        >
          Lista de Movimentação
        </button>
        <button
          class="nav-link"
          :class="{ active: activeTab === 'cadastro' }"
          id="nav-cadastro-tab"
          @click="selectTab('cadastro')"
          type="button"
          role="tab"
          aria-controls="nav-cadastro"
          aria-selected="false"
        >
          Cadastro de Movimentação
        </button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'movimentacoes' }"
        id="nav-vet"
        role="tabpanel"
        aria-labelledby="nav-vet-tab"
      ></div>
      <div
        class="tab-pane fade"
        :class="{ 'show active': activeTab === 'cadastro' }"
        id="nav-cadastro"
        role="tabpanel"
        aria-labelledby="nav-cadastro-tab"
      >
        <div
          class="table-container"
          id="cadastro"
          tabindex="-1"
          aria-labelledby="cadastroLabel"
          aria-hidden="true"
        >
          <h1 class="title fs-5" id="cadastroLabel">
            Cadastro de Movimentação
          </h1>
          <form @submit.prevent="confirmarCadastroMov" @keydown="checkEnter">
            <div class="mb-3 input-group">
              <h2 id="legenda">* Campos Obrigatórios</h2>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text" title="Data"
                ><i class="fas fa-calendar-alt"></i
              ></span>
              <input
                type="text"
                onfocus="(this.type='date')"
                onblur="(this.type='text')"
                :placeholder="dataPlaceholder"
                class="form-control"
                id="dataMovimentacaoCadastro"
                v-model="formData.dataMovimentacao"
                :class="{ 'is-invalid': !isDataValida }"
                title="Data"
              />
            </div>

            <div
              ref="dropdownPiqueteDestino"
              class="select mb-3 input-group"
              @keydown.up.prevent="navigateOptionsPiqueteDestino('up')"
              @keydown.down.prevent="navigateOptionsPiqueteDestino('down')"
              @keydown.enter.prevent="selectHighlightedPiqueteDestino"
            >
              <div
                class="select-option mb-3 input-group"
                @click.stop="toggleDropdownPiqueteDestino"
              >
                <span class="input-group-text" title="Piquete de Destino"
                  ><i class="fas fa-box"></i
                ></span>
                <input
                  v-model="nomePiqueteDestino"
                  :class="{ 'is-invalid': !isPiqueteDestinoValido }"
                  @input="inputPiqueteDestino"
                  @keydown.up.prevent="navigateOptionsPiqueteDestino('up')"
                  autocomplete="off"
                  @keydown.down.prevent="navigateOptionsPiqueteDestino('down')"
                  type="text"
                  class="form-control"
                  :placeholder="piqueteDestinoPlaceholder"
                  id="caixa-select"
                  title="Piquete de Destino"
                />
              </div>
              <div class="itens" v-show="dropdownPiqueteDestinoOpen">
                <ul class="options">
                  <li
                    v-for="(piqueteDestino, index) in piquetesDestinoFiltrados"
                    :key="piqueteDestino.id"
                    :value="piqueteDestino.id"
                    @click="selectPiqueteDestino(piqueteDestino)"
                    :class="{
                      highlighted: index === highlightedIndexPiqueteDestino,
                    }"
                  >
                    {{ piqueteDestino.nome }} -
                    {{ piqueteDestino.propriedade.nome }}
                  </li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group position-relative">
              <span class="input-group-text" title="Motivo"
                ><i class="fas fa-comment"></i
              ></span>
              <input
                v-model="formData.motivo"
                type="text"
                class="form-control"
                id="motivo"
                placeholder="Motivo"
                title="Motivo"
                autocomplete="off"
              />
            </div>

            <div
              ref="dropdownPiqueteOrigem"
              class="select mb-3 input-group"
              @keydown.up.prevent="navigateOptionsPiqueteOrigem('up')"
              @keydown.down.prevent="navigateOptionsPiqueteOrigem('down')"
              @keydown.enter.prevent="selectHighlightedPiqueteOrigem"
            >
              <div
                class="select-option mb-3 input-group"
                @click.stop="toggleDropdownPiqueteOrigem"
              >
                <span class="input-group-text" title="Piquete de Origem"
                  ><i class="fas fa-box"></i
                ></span>
                <input
                  v-model="nomePiqueteOrigem"
                  :class="{ 'is-invalid': !isPiqueteOrigemValido }"
                  @input="inputPiqueteOrigem"
                  @keydown.up.prevent="navigateOptionsPiqueteOrigem('up')"
                  autocomplete="off"
                  @keydown.down.prevent="navigateOptionsPiqueteOrigem('down')"
                  type="text"
                  class="form-control"
                  :placeholder="piqueteOrigemPlaceholder"
                  id="caixa-select"
                  title="Piquete de Origem"
                />
              </div>
              <div class="itens" v-show="dropdownPiqueteOrigemOpen">
                <ul class="options">
                  <li
                    v-for="(piqueteOrigem, index) in piquetesOrigemFiltrados"
                    :key="piqueteOrigem.id"
                    :value="piqueteOrigem.id"
                    @click="selectPiqueteOrigem(piqueteOrigem)"
                    :class="{
                      highlighted: index === highlightedIndexPiqueteOrigem,
                    }"
                  >
                    {{ piqueteOrigem.nome }} -
                    {{ piqueteOrigem.propriedade.nome }}
                  </li>
                </ul>
              </div>
            </div>

            <div class="mb-3 input-group" v-if="animaisFiltrados.length != 0">
              <div class="checkbox-container">
                <label v-if="animaisFiltrados.length != 0">
                  <input
                    type="checkbox"
                    v-model="selecionaTodos"
                    @change="ativaSelecaoTodos"
                  />
                  Selecionar todos
                </label>
                <hr />
                <label
                  @change="desativaSelecaoTodos"
                  v-for="animal in animaisOrdenados"
                  :key="animal.id"
                >
                  <input
                    type="checkbox"
                    :value="animal.id"
                    v-model="formData.animal"
                  />
                  {{ animal.brinco }}
                </label>
              </div>
            </div>
            <div class="button-group justify-content-end">
              <button
                type="button"
                class="btn btn-secondary"
                @click="selectTab('movimentacoes')"
              >
                Cancelar
              </button>
              <button type="submit" class="btn btn-success">Enviar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "/src/interceptadorAxios";
import { masksMixin } from "../mixins/maks";

export default {
  mixins: [masksMixin],

  data() {
    return {
      activeTab: "cadastro", // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      piquetesDestino: [],
      piquetesOrigem: [],
      piquetesDestinoPossiveis: [],
      piquetesOrigemPossiveis: [],
      piquetesDestinoFiltrados: [],
      piquetesOrigemFiltrados: [],
      nomePiqueteOrigem: "",
      nomePiqueteDestino: "",
      highlightedIndexPiqueteDestino: -1,
      dropdownPiqueteDestinoOpen: false,
      highlightedIndexPiqueteOrigem: -1,
      dropdownPiqueteOrigemOpen: false,
      selecionaTodos: false,
      formData: {
        animal: [],
        dataMovimentacao: null,
        piqueteOrigem: null,
        piqueteDestino: null,
        motivo: null,
      },
      isDataValida: true,
      isPiqueteOrigemValido: true,
      isPiqueteDestinoValido: true,
      dataPlaceholder: "Data*",
      piqueteOrigemPlaceholder: "Piquete de Origem*",
      piqueteDestinoPlaceholder: "Piquete de Destino*",
    };
  },
  computed: {
    animaisOrdenados() {
      return this.animaisFiltrados
        .slice()
        .sort((a, b) => a.brinco.localeCompare(b.brinco));
    },
  },
  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarPiquetesParaDestino();
    this.buscarPiquetesParaOrigem();
    document.addEventListener("click", this.handleClickOutsidePiqueteOrigem);
    document.addEventListener("click", this.handleClickOutsidePiqueteDestino);
  },

  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(value) {
      this.brinco = this.brincoMask(value);
    },

    inputBrinco(event) {
      const value = event.target.value;
      this.aplicarBrincoMask(value);
      this.filterAnimais();
    },

    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarAnimaisDaApi() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/animais/vivos-piquetes",
          {
            params: {
              propriedadeSelecionada: localStorage.getItem(
                "propriedadeSelecionada"
              ),
            },
          }
        );
        this.animais = response.data;
      } catch (error) {
        console.error("Erro ao buscar animais da API:", error);
      }
    },

    async buscarPiquetesParaDestino() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/piquetes/piquetes-propriedades"
        );
        this.piquetesDestino = response.data.slice();
        this.piquetesDestinoPossiveis = response.data.slice();
      } catch (error) {
        console.error("Erro ao buscar piquetes da API:", error);
      }
    },

    async buscarPiquetesParaOrigem() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/piquetes/com-animais-propriedade",
          {
            params: {
              propriedadeSelecionada: localStorage.getItem(
                "propriedadeSelecionada"
              ),
            },
          }
        );
        this.piquetesOrigem = response.data.slice();
        this.piquetesOrigemPossiveis = response.data.slice();
      } catch (error) {
        console.error("Erro ao buscar piquetes da API:", error);
      }
    },

    async submitForm() {
      if (this.verificaVazio()) {
        if (this.verificaVazioAnimais()) {
          try {
            const response = await api.post(
              "http://127.0.0.1:8000/movimentacoes/",
              this.formData,
              {}
            );

            if (response.status === 201) {
              alert("Cadastro realizado com sucesso!");
              this.$router.push("/movimentacoes");
            } else {
              alert(
                "Erro ao cadastrar movimentacao. Tente novamente mais tarde."
              );
            }
          } catch (error) {
            console.error("Erro ao enviar requisição:", error);
            alert(
              "Erro ao enviar requisição. Verifique o console para mais detalhes."
            );
          }
        } else {
          alert("Nenhum animal foi selecionado");
        }
      }
    },

    //LÓGICA DOS SELECT PIQUETE DESTINO----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetesDestino() {
      this.atualizaDestino();
      this.piquetesDestinoFiltrados = this.piquetesDestinoPossiveis.filter(
        (piqueteDestino) =>
          piqueteDestino.nome
            .toLowerCase()
            .includes(this.nomePiqueteDestino.toLowerCase())
      );
    },

    async selectPiqueteDestino(piqueteDestino) {
      this.nomePiqueteDestino =
        piqueteDestino.nome + " - " + piqueteDestino.propriedade.nome;
      this.formData.piqueteDestino = piqueteDestino.id;
      this.piquetesDestinoFiltrados = [];
      this.dropdownPiqueteDestinoOpen = false;
      this.highlightedIndexPiqueteDestino = -1; // Reseta o índice após a seleção
    },

    toggleDropdownPiqueteDestino() {
      this.dropdownPiqueteDestinoOpen = !this.dropdownPiqueteDestinoOpen;
      let nomeCorreto = false;

      if (!this.dropdownPiqueteDestinoOpen) {
        this.piquetesDestinoFiltrados.forEach((piqueteDestino) => {
          if (
            piqueteDestino.nome.toLowerCase() ===
            this.nomePiqueteDestino.toLowerCase()
          ) {
            this.selectPiqueteDestino(piqueteDestino);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiqueteDestino = "";
          this.formData.piqueteDestino = null;
        }
      } else if (this.dropdownPiqueteOrigemOpen) {
        this.piquetesOrigemPossiveis.forEach((piqueteOrigem) => {
          if (
            piqueteOrigem.nome.toLowerCase() ===
            this.nomePiqueteOrigem.toLowerCase()
          ) {
            this.selectPiqueteOrigem(piqueteOrigem);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.piqueteOrigem = null;
          this.nomePiqueteOrigem = "";
          this.animaisFiltrados = [];
        }
        this.dropdownPiqueteOrigemOpen = false;
        this.filterPiquetesDestino();
      } else {
        this.filterPiquetesDestino();
      }
    },

    handleClickOutsidePiqueteDestino(event) {
      let nomeCorreto = false;
      if (
        this.dropdownPiqueteDestinoOpen &&
        this.$refs.dropdownPiqueteDestino &&
        !this.$refs.dropdownPiqueteDestino.contains(event.target)
      ) {
        this.piquetesDestinoPossiveis.forEach((piqueteDestino) => {
          if (
            piqueteDestino.nome.toLowerCase() ===
            this.nomePiqueteDestino.toLowerCase()
          ) {
            this.selectPiqueteDestino(piqueteDestino);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiqueteDestino = "";
          this.formData.piqueteDestino = null;
        }
      }
      this.dropdownPiqueteDestinoOpen = false;
    },

    inputPiqueteDestino() {
      this.filterPiquetesDestino();
      this.dropdownPiqueteDestinoOpen = true;
      this.highlightedIndexPiqueteDestino = 0; // Inicia o índice ao começar a digitação
    },

    navigateOptionsPiqueteDestino(direction) {
      if (direction === "up" && this.highlightedIndexPiqueteDestino > 0) {
        this.highlightedIndexPiqueteDestino--;
      } else if (
        direction === "down" &&
        this.highlightedIndexPiqueteDestino <
          this.piquetesDestinoFiltrados.length - 1
      ) {
        this.highlightedIndexPiqueteDestino++;
      }
    },

    selectHighlightedPiqueteDestino() {
      if (
        this.highlightedIndexPiqueteDestino >= 0 &&
        this.highlightedIndexPiqueteDestino <
          this.piquetesDestinoFiltrados.length
      ) {
        this.selectPiqueteDestino(
          this.piquetesDestinoFiltrados[this.highlightedIndexPiqueteDestino]
        );
      }
    },

    //LÓGICA DOS SELECT PIQUETE ORIGEM----------------------------------------------------------------------------------------------------------------------------------------------------
    filterPiquetesOrigem() {
      this.atualizaOrigem();
      this.piquetesOrigemFiltrados = this.piquetesOrigemPossiveis.filter(
        (piqueteOrigem) =>
          piqueteOrigem.nome
            .toLowerCase()
            .includes(this.nomePiqueteOrigem.toLowerCase())
      );
    },

    async selectPiqueteOrigem(piqueteOrigem) {
      this.nomePiqueteOrigem =
        piqueteOrigem.nome + " - " + piqueteOrigem.propriedade.nome;
      this.formData.piqueteOrigem = piqueteOrigem.id;
      this.piquetesOrigemFiltrados = [];
      this.dropdownPiqueteOrigemOpen = false;
      this.highlightedIndexPiqueteOrigem = -1; // Reseta o índice após a seleção

      this.preencheCheckBox();
    },

    toggleDropdownPiqueteOrigem() {
      this.dropdownPiqueteOrigemOpen = !this.dropdownPiqueteOrigemOpen;
      let nomeCorreto = false;
      this.filterPiquetesOrigem();

      if (!this.dropdownPiqueteOrigemOpen) {
        this.piquetesOrigemFiltrados.forEach((piqueteOrigem) => {
          if (
            piqueteOrigem.nome.toLowerCase() ===
            this.nomePiqueteOrigem.toLowerCase()
          ) {
            this.selectPiqueteOrigem(piqueteOrigem);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiqueteOrigem = "";
          this.formData.piqueteOrigem = null;
          this.animaisFiltrados = [];
        }
      } else if (this.dropdownPiqueteDestinoOpen) {
        this.piquetesDestinoPossiveis.forEach((piqueteDestino) => {
          if (
            piqueteDestino.nome.toLowerCase() ===
            this.nomePiqueteDestino.toLowerCase()
          ) {
            this.selectPiqueteDestino();
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.formData.piqueteDestino = null;
          this.nomePiqueteDestino = "";
        }
        this.dropdownPiqueteDestinoOpen = false;
      }
    },

    handleClickOutsidePiqueteOrigem(event) {
      let nomeCorreto = false;
      if (
        this.dropdownPiqueteOrigemOpen &&
        this.$refs.dropdownPiqueteOrigem &&
        !this.$refs.dropdownPiqueteOrigem.contains(event.target)
      ) {
        this.piquetesOrigemPossiveis.forEach((piqueteOrigem) => {
          if (
            piqueteOrigem.nome.toLowerCase() ===
            this.nomePiqueteOrigem.toLowerCase()
          ) {
            this.selectPiqueteOrigem(piqueteOrigem);
            nomeCorreto = true;
          }
        });
        if (!nomeCorreto) {
          this.nomePiqueteOrigem = "";
          this.formData.piqueteOrigem = null;
          this.animaisFiltrados = [];
        }
      }
      this.dropdownPiqueteOrigemOpen = false;
    },

    inputPiqueteOrigem() {
      this.filterPiquetesOrigem();
      this.dropdownPiqueteOrigemOpen = true;
      this.highlightedIndexPiqueteOrigem = 0; // Inicia o índice ao começar a digitação

      if (this.nomePiqueteOrigem.trim() === "") {
        this.animaisFiltrados = [];
      }
    },

    navigateOptionsPiqueteOrigem(direction) {
      if (direction === "up" && this.highlightedIndexPiqueteOrigem > 0) {
        this.highlightedIndexPiqueteOrigem--;
      } else if (
        direction === "down" &&
        this.highlightedIndexPiqueteOrigem <
          this.piquetesOrigemFiltrados.length - 1
      ) {
        this.highlightedIndexPiqueteOrigem++;
      }
    },

    selectHighlightedPiqueteOrigem() {
      if (
        this.highlightedIndexPiqueteOrigem >= 0 &&
        this.highlightedIndexPiqueteOrigem < this.piquetesOrigemFiltrados.length
      ) {
        this.selectPiqueteOrigem(
          this.piquetesOrigemFiltrados[this.highlightedIndexPiqueteOrigem]
        );
      }
    },

    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
    verificaVazio() {
      //DATA DA MOVIMENTAÇÃO
      if (this.formData.dataMovimentacao != null) {
        if (this.formData.dataMovimentacao.trim() != "") {
          this.isDataValida = true;
          this.dataPlaceholder = "Data*";
        } else {
          this.isDataValida = false;
          this.dataPlaceholder = "Data é um Campo Obrigatório";
        }
      } else {
        this.isDataValida = false;
        this.dataPlaceholder = "Data é um Campo Obrigatório";
      }

      //PIQUETE ORIGEM
      if (this.nomePiqueteOrigem != null) {
        if (this.nomePiqueteOrigem.trim() != "") {
          this.isPiqueteOrigemValido = true;
          this.piqueteOrigemPlaceholder = "Piquete de Origem*";
        } else {
          this.isPiqueteOrigemValido = false;
          this.piqueteOrigemPlaceholder =
            "Piquete de Origem é um Campo Obrigatório";
        }
      } else {
        this.isPiqueteOrigemValido = false;
        this.piqueteOrigemPlaceholder =
          "Piquete de Origem é um Campo Obrigatório";
      }

      //PIQUETE DE DESTINO
      if (this.nomePiqueteDestino != null) {
        if (this.nomePiqueteDestino.trim() != "") {
          this.isPiqueteDestinoValido = true;
          this.piqueteDestinoPlaceholder = "Piquete de Destino*";
        } else {
          this.isPiqueteDestinoValido = false;
          this.piqueteDestinoPlaceholder =
            "Piquete de Destino é um Campo Obrigatório";
        }
      } else {
        this.isPiqueteDestinoValido = false;
        this.piqueteDestinoPlaceholder =
          "Piquete de Destino é um Campo Obrigatório";
      }

      //MOTIVO
      if (this.formData.motivo != null && this.formData.motivo.trim() == "") {
        this.formData.motivo = null;
      }

      return (
        this.isDataValida &&
        this.isPiqueteOrigemValido &&
        this.isPiqueteDestinoValido
      );
    },

    verificaVazioAnimais() {
      return this.formData.animal.length > 0;
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    confirmarCadastroMov() {
      if (confirm("Movimentações não podem ser alteradas ou apagadas do sistema. Tem certeza que deseja continuar com o cadastro?")) {
        this.submitForm();
      }
    },

    checkEnter(event) {
      if (event.key === "Enter") {
        this.submitForm();
      }
    },
    preencheCheckBox() {
      this.animaisFiltrados = this.animais.filter(
        (animal) => animal.piquete.id === this.formData.piqueteOrigem
      );
    },

    ativaSelecaoTodos() {
      this.formData.animal = [];
      if (this.selecionaTodos) {
        this.animais.forEach((animal) => {
          this.formData.animal.push(animal.id);
        });
      }
    },

    desativaSelecaoTodos() {
      this.selecionaTodos = false;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === "movimentacoes") {
        this.$router.push("/movimentacoes");
      }
    },

    atualizaOrigem() {
      this.piquetesOrigemPossiveis = this.piquetesOrigem.slice();
      let indice = null;
      for (
        let index = 0;
        index < this.piquetesOrigemPossiveis.length;
        index++
      ) {
        const piquete = this.piquetesOrigemPossiveis[index];
        if (piquete.id === this.formData.piqueteDestino) {
          indice = index;
          break;
        }
      }
      if (indice != null) {
        this.piquetesOrigemPossiveis.splice(indice, 1);
      }
    },

    atualizaDestino() {
      this.piquetesDestinoPossiveis = this.piquetesDestino.slice();
      let indice = null;
      for (
        let index = 0;
        index < this.piquetesDestinoPossiveis.length;
        index++
      ) {
        const piquete = this.piquetesDestinoPossiveis[index];
        if (piquete.id === this.formData.piqueteOrigem) {
          indice = index;
          break;
        }
      }
      if (indice != null) {
        this.piquetesDestinoPossiveis.splice(indice, 1);
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
}

.nav-link.active {
  background-color: #d0d0d0 !important;
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
  background-color: #ededef !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  background-color: #f0f0f0;
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

.is-invalid {
  border-color: #dc3545;
}

#legenda {
  font-size: 16px;
}

.checkbox-container {
  gap: 10px;
  border: 1px solid #6c757d;
  border-radius: 5px;
  padding: 20px;
  width: 40%; /* Largura do contêiner */
  height: 150px; /* Altura do contêiner */
  overflow-y: auto; /* Adiciona uma barra de rolagem se necessário */
}

.checkbox-container label {
  display: flex;
  align-items: center;
}

.select-option {
  width: 100%;
  cursor: pointer;
}

.itens {
  position: absolute;
  background-color: #fff;
  color: #000;
  border: 1px solid #ccc;
  border-radius: 7px;
  width: 100%;
  margin-top: 40px;
  z-index: 999;
  padding: 20px;
}

.options {
  max-height: 200px;
  /* Ajuste a altura conforme necessário */
  overflow-y: auto;
  border: 1px solid #ddd;
  margin: 0;
  padding: 0;
  list-style: none;
}

.options li {
  padding: 10px;
  cursor: pointer;
}

.options li:hover {
  background-color: #f0f0f0;
}

.select {
  margin-bottom: 0px !important;
}

.highlighted {
  background-color: #f0f0f0;
}
</style>

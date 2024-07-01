<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista
          de Animais</button>

        <button class="nav-link" :class="{ active: activeTab === 'aplicacao' }" id="nav-aplicacao-tab"
          @click="selectTab('aplicacao')" type="button" role="tab" aria-controls="nav-aplicacao"
          aria-selected="false">Lista de Aplicação</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao" aria-selected="false">Edição
          de Aplicação</button>
      </div>
    </nav>

    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'animais' }" id="nav-animais" role="tabpanel"
        aria-labelledby="nav-animais-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacao' }" id="nav-aplicacao"
        role="tabpanel" aria-labelledby="nav-aplicacao-tab">

      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">

        <!-- Modal de Edição de Aplicação -->
        <div class="table-container" id="aplicacao" tabindex="-1" aria-labelledby="aplicacaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="aplicacaoLabel">Edição de Aplicação</h1>
          <form @submit.prevent="submitForm">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
              <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                placeholder="Data da aplicação" class="form-control" id="dataAplicacaoEdicao"
                v-model="formData.dataAplicacao" required>
            </div>
            <div class="mb-3 input-group">
              <input v-model="brinco" @input="filterAnimais" type="text" class="form-control"
                placeholder="Digite o brinco...">
            </div>
            <div class="list-group" v-if="brinco && animaisFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados"
                :key="animal.id" @click="selectAnimal(animal)">
                {{ animal.brinco }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <input v-model="nomeProduto" @input="filterProdutos" type="text" class="form-control"
                placeholder="Digite o produto...">
            </div>
            <div class="list-group" v-if="nomeProduto && produtosFiltrados.length">
              <button type="button" class="list-group-item list-group-item-action" v-for="produto in produtosFiltrados"
                :key="produto.id" @click="selectProduto(produto)">
                {{ produto.nome }}
              </button>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.dosagem" type="text" class="form-control" id="dosagem"
                :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Dosagem" required>
            </div>
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tags"></i></span>
              <input v-model="formData.observacao" type="text" class="form-control" id="observacao"
                :disabled="!(camposHabilitadosAnimal && camposHabilitadosProduto)" placeholder="Observação" required>
            </div>
            <div class="button-group justify-content-end">
              <button type="button" class="btn btn-secondary" @click="selectTab('aplicacao')">Cancelar</button>
              <button type="submit" class="btn btn-success">Enviar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaAplicacoesProdutos',
  data() {
    return {
      activeTab: 'edicao',
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      aplicacao: null,
      produtos: [],
      produtosFiltrados: [],
      nomeProduto: '',
      datasAplicacoes: [],
      dataSelecionada: null,
      detalhesAplicacao: [],
      aplicacaoParaExcluir: null,
      dataParaExclusao: null,
      camposHabilitadosAnimal: false,
      camposHabilitadosPiquete: false,
      camposHabilitadosProduto: false,
      piquetes: [],
      piquete: '',
      piqueteId: null,
      filteredPiquetes: [],
      radioEscolha: 'brinco',
      formData: {
        id: null,
        produto: '',
        animal: [],
        dosagem: '',
        dataAplicacao: '',
        observacao: null,
      },
      aplicacaoId: null,
      isProdutoValido: true,
      isDosagemValido: true,
      isDataAplicacaoValido: true,
      isBrincoValido: true,
      isPiqueteValido: true,
      piquetePlaceholder: 'Selecione o piquete',
      brincoPlaceholder: 'Digite o brinco',
      dataAplicacaoPlaceholder: 'Selecione a data da aplicacao',
      dosagemPlaceholder: 'Digite a dosagem',
      produtoPlaceholder: 'Selecione o produto',
    }

  },
  async mounted() {
    const aplicacaoId = localStorage.getItem('aplicacaoSelecionado');
    if (aplicacaoId) {
      this.aplicacaoId = aplicacaoId;
      await this.buscarAplicacaoDaApi(aplicacaoId);
    }
    this.buscarAnimaisDaApi();
    this.buscarProdutosDaApi();
    this.buscarPiquetesDaApi();
  },
  methods: {
    validarFormulario() {
      this.isProdutoValido = !!this.formData.produto;
      this.isDosagemValido = !!this.formData.dosagem;
      this.isDataAplicacaoValido = !!this.formData.dataAplicacao;
      this.isBrincoValido = !!this.formData.brinco;
      this.isPiqueteValido = !!this.formData.piquete;

      this.produtoPlaceholder = this.isProdutoValido ? 'Selecione o produto' : 'Produto é obrigatório';
      this.dosagemPlaceholder = this.isDosagemValido ? 'Digite a dosagem' : 'Dosagem é obrigatória';
      this.dataAplicacaoPlaceholder = this.isDataAplicacaoValido ? 'Selecione a data da aplicacao' : 'Data de aplicação é obrigatória';
      this.brincoPlaceholder = this.isBrincoValido ? 'Digite o brinco' : 'Brinco é obrigatório';
      this.piquetePlaceholder = this.isPiqueteValido ? 'Selecione o piquete' : 'Piquete é obrigatório';

      return this.isProdutoValido && this.isDosagemValido && this.isDataAplicacaoValido && this.isBrincoValido && this.isPiqueteValido;
    },
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'animais') {
        this.$router.push('/animais');
      }
      if (tab === 'aplicacao') {
        this.$router.push('/aplicacoes-produtos');
      }
    },

    async buscarAplicacaoDaApi() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/aplicacoes-produtos/aplicacao-produto/${this.aplicacaoId}/`);
        this.aplicacao = response.data;
        this.editarAplicacao(this.aplicacao);
      } catch (error) {
        console.error('Erro ao buscar aplicações de produtos da API:', error);
      }
    },

    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/vivos', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    filtrarPiquetes() {
      this.filteredPiquetes = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piquete));
    },

    selecionarPiquete(piquete) {
      this.camposHabilitadosPiquete = true;
      this.piqueteId = piquete.id;
      this.piquete = piquete.nome;
      this.filteredPiquetes = [];
      this.preencheListaAnimais()
    },

    filterAnimais() {
      this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectAnimal(animal) {
      this.formData.animal = [];
      this.brinco = animal.brinco;
      console.log('animalId antes: ', this.formData.animal);
      this.formData.animal.push(animal.id);
      console.log('animalId depois: ', this.formData.animal);
      this.camposHabilitadosAnimal = true;
      this.animaisFiltrados = [];
    },

    async buscarProdutosDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/produtos/sanitarios', {});
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtos da API:', error);
      }
    },

    filterProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => produto.nome.toLowerCase().includes(this.nomeProduto));
    },

    selectProduto(produto) {
      this.nomeProduto = produto.nome;
      this.formData.produto = produto.id;
      this.camposHabilitadosProduto = true;
      this.produtosFiltrados = [];
    },

    editarAplicacao(aplicacao) {
      this.formData = {
        id: aplicacao.id,
        animal: aplicacao.animal.id,
        produto: aplicacao.produto.id,
        dataAplicacao: aplicacao.dataAplicacao,
        dosagem: aplicacao.dosagem,
        observacao: aplicacao.observacao,
      };
      this.brinco = aplicacao.animal.brinco;
      this.nomeProduto = aplicacao.produto.nome;
      this.camposHabilitadosAnimal = true;
      this.camposHabilitadosProduto = true;
    },

    preencheListaAnimais() {
      this.formData.animal = [];
      let listaAnimais;
      listaAnimais = this.animais.filter(animal => animal.piquete == this.piqueteId);
      listaAnimais.forEach(animal => {
        this.formData.animal.push(animal.id);
      });
    },

    async submitForm() {
      if (this.validarFormulario()) {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/aplicacoes-produtos/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarAplicacoesDaApi();
            this.fecharModal("edicaoModal");
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },


  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color: #ededef;
  /* Um tom mais escuro que o branco */
  min-height: 100vh;
  /* Garante que o fundo cubra toda a altura da tela */
  padding: 20px;
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

.button-group {
  display: flex;
  gap: 10px;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
  /* Cor um pouco mais escura quando a aba está ativa */
}
</style>
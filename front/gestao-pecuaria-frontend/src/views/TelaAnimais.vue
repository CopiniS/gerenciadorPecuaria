<template>
  <div class="background">

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link active" id="nav-aniamis-tab" data-bs-toggle="tab" data-bs-target="#nav-animais"
          type="button" role="tab" aria-controls="nav-animais" aria-selected="true">Lista de Animais</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-animais-tab"
        tabindex="0"></div>
    </div>

    <h2>Lista de Animais</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" @keyup.enter="aplicarFiltro" class="row g-3 align-items-center"
        v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="brinco" class="form-label me-2">Brinco</label>
          <input type="text" @input="aplicarBrincoMask" class="form-control input-consistente" id="brinco"
            v-model="filtro.brinco">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataNascimento" class="form-label me-2">Data de Nascimento</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataNascimentoInicio"
            :endDate="filtro.dataNascimentoFim" @update:startDate="val => filtro.dataNascimentoInicio = val"
            @update:endDate="val => filtro.dataNascimentoFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="sexo" class="form-label me-2">Sexo</label>
          <select class="form-select select-consistente" id="sexo" v-model="filtro.sexo">
            <option value="">Selecione o sexo</option>
            <option value="macho">Macho</option>
            <option value="femea">Fêmea</option>
          </select>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="raca" class="form-label me-2">Raça</label>
          <input type="text" class="form-control input-consistente" id="raca" v-model="filtro.raca">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="brincoPai" class="form-label me-2">Brinco Pai</label>
          <input type="text" @input="aplicarBrincoPaiMask" class="form-control input-consistente" id="brincoPai"
            v-model="filtro.brincoPai">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="brincoMae" class="form-label me-2">Brinco Mãe</label>
          <input type="text" @input="aplicarBrincoMaeMask" class="form-control input-consistente" id="brincoMae"
            v-model="filtro.brincoMae">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="piquete" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control input-consistente" id="piquete" v-model="filtro.piquete">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="status" class="form-label me-2">Status</label>
          <select class="form-select select-consistente" id="status" v-model="filtro.status">
            <option value="">Selecione o status</option>
            <option>Morto</option>
            <option>Vivo</option>
            <option>Vendido</option>
          </select>
        </div>
        <div class="col-12 d-flex justify-content-start mt-3">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

    <div>
      <div class="table-container">
        <div class="button-container">
          <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Animal</button>

          <button @click="() => { this.$router.push('/racas'); }" type="button" class="btn btn-success">Lista de
            Raças</button>
          <button @click="mostrarPopupEscolhaRelatorio" type="button" class="btn btn-success" data-bs-toggle="modal"
            data-bs-target="#escolhaRelatorioModal">Gerar Relatório</button>

        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Brinco</th>
              <th scope="col">Data Nascimento</th>
              <th scope="col">Sexo</th>
              <th scope="col">Piquete</th>
              <th scope="col">Status</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(animal, index) in animais" :key="index"
              >
              <td>{{ animal.brinco }}</td>
              <td>{{ formatarData(animal.dataNascimento) }}</td>
              <td>{{ animal.sexo }}</td>
              <td>{{ animal.piquete.nome }}</td>
              <td :class="{ 'status-Vivo': animal.status === 'Vivo', 'status-morto': animal.status === 'morto', 'status-doente': animal.status === 'doente' }"
              >{{ animal.status }}</td>
              <td>
                <div class="d-flex justify-content-center button-group">
                  <button @click="acessarVisualizacao(animal)" class="btn-acoes btn-sm" data-bs-toggle="tooltip"
                    title="Visualizar Animal"><i class="fas fa-eye"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal para escolher o tipo de relatório -->
      <div class="modal fade" id="escolhaRelatorioModal" tabindex="-1" aria-labelledby="escolhaRelatorioModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="escolhaRelatorioModalLabel">Escolha o Tipo de Relatório</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="mostrarRelatorio">
                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipoRelatorio" id="relatorioResumido"
                      value="resumido" v-model="tipoRelatorio">
                    <label class="form-check-label" for="relatorioResumido">
                      Relatório de Animais Resumido
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipoRelatorio" id="relatorioDetalhado"
                      value="detalhado" v-model="tipoRelatorio">
                    <label class="form-check-label" for="relatorioDetalhado">
                      Relatório de Animais Detalhado
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="tipoRelatorio" id="relatorioCompra"
                      value="compraAnimais" v-model="tipoRelatorio">
                    <label class="form-check-label" for="relatorioCompra">
                      Relatório de Compra de Animais
                    </label>
                  </div>

                </div>
              </form>

              <!-- Relatório de Animal resumido -->
              <div v-if="tipoRelatorio === 'resumido'">
                <RelatorioPdf titulo="Relatório de Animal Resumido"
                  :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtualNome]"
                  :colunas="['Brinco', 'Data de nascimento', 'Sexo', 'Piquete']"
                  :dados="animais.map(animal => [animal.brinco, formatarData(animal.dataNascimento), animal.sexo, animal.piquete.nome])" />

              </div>

              <!-- Relatório de Animal detalhado -->
              <div v-if="tipoRelatorio === 'detalhado'">
                <RelatorioPdf titulo="Relatório de Animal Detalhado"
                  :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtualNome]"
                  :colunas="['Brinco', 'Data de nascimento', 'Sexo', 'Piquete', 'Raça predominante', 'Raça observacao', 'Brinco pai', 'Brinco mãe']"
                  :dados="animais.map(animal => [animal.brinco, formatarData(animal.dataNascimento), animal.sexo, animal.piquete.nome, animal.racaPredominante?.nome, animal.racaObservacao, animal.brincoPai, animal.brincoMae])"
                  :orientacaoPaisagem="true" />
              </div>
              <div v-if="tipoRelatorio === 'compraAnimais'">
                <!-- Relatório de Compra de Animais -->
                <RelatorioPdf v-if="tipoRelatorio === 'compraAnimais'" titulo="Relatório de Compra de Animais"
                  :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtualNome]"
                  :colunas="['Brinco', 'Data da Compra', 'Valor da Compra']"
                  :dados="animaisComprados.map(animal => [animal.brinco, formatarData(animal.dataCompra), animal.valorCompra])"
                  :mostrarSoma="true" />
              </div>
            </div>
          </div>
        </div>
      </div>



    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';
import { masksMixin } from '../mixins/maks';
import DateRangePicker from '../components/DateRangePicker.vue';
import RelatorioPdf from '../components/RelatorioPdf.vue';

export default {
  mixins: [masksMixin],

  name: 'TelaAnimais',
  components: {
    DateRangePicker,
    RelatorioPdf
  },
  data() {
    return {
      animais: [],
      animaisDaApi: [],
      mostrarFormulario: false,
      filtro: {
        brinco: '',
        dataNascimentoInicio: '',
        dataNascimentoFim: '',
        sexo: '',
        raca: '',
        brincoPai: '',
        brincoMae: '',
        observacoes: '',
        piquete: '',
        status: '',
      },
      tipoRelatorio: null,
      propriedadeAtualNome: localStorage.getItem('propriedadeSelecionadaNome'),
      nomeProdutor: localStorage.getItem('produtorNome'),
    }
  },
  async mounted() {
    this.buscarAnimaisDaApi();
  },
  computed: {
    // Filtra os animais comprados
    animaisComprados() {
      return this.animais.filter(animal => animal.dataCompra && animal.valorCompra);
    }
  },
  methods: {
    //MÁSCARAS-------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarBrincoMask(event) {
      const value = event.target.value;
      this.filtro.brinco = this.brincoFiltroMask(value);
    },

    aplicarBrincoPaiMask(event) {
      const value = event.target.value;
      this.filtro.brincoPai = this.brincoFiltroMask(value);
    },

    aplicarBrincoMaeMask(event) {
      const value = event.target.value;
      this.filtro.brincoMae = this.brincoFiltroMask(value);
    },


    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async buscarAnimaisDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/animais/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animaisDaApi = response.data;
        this.animais = this.animaisDaApi;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
    },

    //FILTROS-----------------------------------------------------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.animais = this.animaisDaApi.filter(animal => {

        //essas verificações é para o caso de o ususario nao ter cadastrado raça, brinco pai ou brinco mae
        if (animal.raca == null) {
          animal.raca = { nome: '' };
        }
        if (animal.brincoPai == null) {
          animal.brincoPai = '';
        }
        if (animal.brincoMae == null) {
          animal.brincoMae = '';
        }
        return (new Date(animal.dataNascimento) >= new Date(this.filtro.dataNascimentoInicio || '1970-01-01')) &&
          (new Date(animal.dataNascimento) <= new Date(this.filtro.dataNascimentoFim || '9999-12-31')) &&
          animal.brinco.includes(this.filtro.brinco) &&
          animal.sexo.includes(this.filtro.sexo) &&
          animal.piquete.nome.includes(this.filtro.piquete) &&
          (animal.raca.nome.includes(this.filtro.raca)) &&
          (animal.brincoPai.includes(this.filtro.brincoPai)) &&
          (animal.brincoMae.includes(this.filtro.brincoMae)) &&
          animal.status.includes(this.filtro.status);
      });
    },

    limparFiltro() {
      this.filtro.brinco = '';
      this.filtro.dataNascimentoInicio = '';
      this.filtro.dataNascimentoFim = '';
      this.filtro.sexo = '';
      this.filtro.raca = '';
      this.filtro.brincoPai = '';
      this.filtro.brincoMae = '';
      this.filtro.piquete = '';
      this.filtro.status = '';

      this.animais = this.animaisDaApi;

      // Resetando as datas no DateRangePicker
      this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------

    acessarCadastro() {
      this.$router.push({
        name: 'AnimaisCadastro',
        params: { animalJSON: 'animaisLista' }
      });
    },

    acessarVisualizacao(animal) {
      this.$router.push({
        name: 'VizualizarAnimal',
        params: { animalId: animal.id }
      })
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  z-index: 0;  
}

.background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../assets/logo-sem-fundo.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; 
} 

.modal {
  z-index: 2000; /* Z-index padrão do Bootstrap para modais */
}

nav, .tab-content {
  position: relative;
  z-index: 1;  
}

.table-container, .button-container {
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

.status-Vivo {
  color: #28b649;
  /* Verde claro para 'Vivo' */
}

.status-morto {
  color: #ff5260;
  /* Vermelho claro para 'morto' */
}

.status-doente {
  color: #ff9800;
  /* Amarelo claro para 'doente' */
}

.nav-link.active {
  background-color: #d0d0d0 !important;
  /* Cor um pouco mais escura quando a aba está ativa */
}

.input-consistente,
.select-consistente {
  width: 200px;
}

.btn {
  margin-bottom: 0;
}

.form-check {
  cursor: pointer;
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
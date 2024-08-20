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

    <h2>Animais</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro"  @keyup.enter="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
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
              :class="{ 'status-Vivo': animal.status === 'Vivo', 'status-morto': animal.status === 'morto', 'status-doente': animal.status === 'doente' }">
              <td>{{ animal.brinco }}</td>
              <td>{{ formatarData(animal.dataNascimento) }}</td>
              <td>{{ animal.sexo }}</td>
              <td>{{ animal.piquete.nome }}</td>
              <td>{{ animal.status }}</td>
              <td>
                <div class="d-flex justify-content-center button-group">
                  <button @click="acessarVisualizacao(animal)" class="btn-acoes btn-sm" 
                  data-bs-toggle="tooltip" title="Visualizar Animal"><i class="fas fa-eye"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';
import { masksMixin } from '../mixins/maks';
import DateRangePicker from './DateRangePicker.vue';

export default {
  mixins: [masksMixin],

  name: 'TelaAnimais',
  components: {
    DateRangePicker
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
    }
  },
  async mounted() {
    this.buscarAnimaisDaApi();
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
  overflow-x: auto;
}

.table-container table tbody tr td {
  background-color: #f0f0f0;
  /* Cor de fundo das células da tabela */
}

.button-container {
  display: flex;
  flex-wrap: nowrap; /* Garante que os botões não vão para a linha seguinte */
  gap: 10px; /* Espaço entre os botões */
  margin-bottom: 20px; 
  white-space: nowrap; /* Evita quebras de linha nos botões */
}

.btn-success {
  margin-right: 10px;
  margin-bottom: 10px;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  background-color: #f0f0f0;
  /* Adiciona uma borda verde na parte inferior */
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

.status-Vivo {
  background-color: #d4edda;
  /* Verde claro para 'Vivo' */
}

.status-morto {
  background-color: #f8d7da;
  /* Vermelho claro para 'morto' */
}

.status-doente {
  background-color: #fff3cd;
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
</style>
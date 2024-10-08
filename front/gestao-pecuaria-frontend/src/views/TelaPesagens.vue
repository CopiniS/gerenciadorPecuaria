<template>
  <div class="background">

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link active" id="nav-vet-tab" data-bs-toggle="tab" data-bs-target="#nav-vet" type="button"
          role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Pesagens</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-vet-tab" tabindex="0">
      </div>
    </div>

    <h2>Lista de Pesagens</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form @submit.prevent="aplicarFiltro" @keyup.enter="aplicarFiltro" class="row g-3 align-items-center"
        v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="dataPesagem" class="form-label me-2">Data</label>
          <DateRangePicker ref="dateRangePicker" class="input-consistente" :startDate="filtro.dataPesagemInicio"
            :endDate="filtro.dataPesagemFim" @update:startDate="val => filtro.dataPesagemInicio = val"
            @update:endDate="val => filtro.dataPesagemFim = val" />
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Animal</label>
          <input type="text" @input="aplicarBrincoMask" class="form-control input-consistente" id="animal"
            v-model="filtro.animal">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Peso </label>
          <input type="text" @input="aplicarPesoInicioMask" class="form-control input-consistente" id="pesoInicio"
            placeholder="Inicial" v-model="filtro.pesoInicio">
        </div>
        <div class="col-auto d-flex align-items-center">
          <input type="text" @input="aplicarPesoFimMask" class="form-control input-consistente" id="pesoFim"
            placeholder="Final" v-model="filtro.pesoFim">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="produto" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control input-consistente" id="piquete" v-model="filtro.piquete">
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
          <button @click="acessarCadastro()" type="button" class="btn btn-success">Cadastrar Pesagem</button>
          <RelatorioPdf titulo="Relatório de Pesagem"
            :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtualNome]"
            :colunas="['Brinco', 'Data da pesagem', 'Peso']"
            :dados="pesagens.map(pesagem => [pesagem.animal.brinco, formatarData(pesagem.dataPesagem), pesagem.peso])"
            :mostrarMedia="true" />

        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data</th>
              <th scope="col">Brinco</th>
              <th scope="col">Piquete</th>
              <th scope="col">Peso</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pesagem, index) in pesagens" :key="index">
              <td>{{ formatarData(pesagem.dataPesagem) }}</td>
              <td>{{ pesagem.animal.brinco }}</td>
              <td>{{ pesagem.animal.piquete.nome }}</td>
              <td>{{ replacePontoVirgula(pesagem.peso) }}</td>
              <td>
                <button @click="acessarEdicao(pesagem)" class="btn-acoes btn-sm" title="Editar Pesagem">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="confirmarExclusaoPesagem(pesagem)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal" title="Excluir Pesagem">
                  <i class="fas fa-trash-alt"></i>
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
              <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir esta Pesagem?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarPesagem()">Excluir</button>
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
  components: {
    DateRangePicker,
    RelatorioPdf
  },

  data() {
    return {
      pesagens: [],
      pesagensDaApi: [],
      propriedadeAtualNome: localStorage.getItem('propriedadeSelecionadaNome'),
      nomeProdutor: localStorage.getItem('produtorNome'),
      formData: {
        id: null,
        dataPesagem: '',
        peso: '',
        observacao: null,
        animal: null
      },
      mostrarFormulario: false,
      filtro: {
        dataPesagemInicio: '',
        dataPesagemFim: '',
        animal: '',
        pesoInicio: '',
        pesoFim: '',
        piquete: '',
      },
    }
  },
  mounted() {
    this.buscarPesagensDaApi();
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
    async buscarPesagensDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/pesagens/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.pesagensDaApi = response.data;
        this.pesagens = this.pesagensDaApi;

      } catch (error) {
        console.error('Erro ao buscar pesagens da API:', error);
      }
    },

    async apagarPesagem() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/pesagens/${this.formData.id}/`);

        if (response.status === 204) {
          alert('Exclusão realizada com sucesso!');
          this.buscarPesagensDaApi();
        } else {
          alert('Erro ao excluir a pesagem. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoModal');
    },


    //FILTROS---------------------------------------------------------------------------------------------------------------------
    aplicarFiltro() {
      this.pesagens = this.pesagensDaApi.filter(pesagem => {
        return (new Date(pesagem.dataPesagem) >= new Date(this.filtro.dataPesagemInicio || '1970-01-01')) &&
          (new Date(pesagem.dataPesagem) <= new Date(this.filtro.dataPesagemFim || '9999-12-31')) &&
          (pesagem.peso >= parseFloat(this.filtro.pesoInicio) || this.filtro.pesoInicio == '') &&
          (pesagem.peso <= parseFloat(this.filtro.pesoFim) || this.filtro.pesoFim == '') &&
          pesagem.animal.brinco.includes(this.filtro.animal) &&
          pesagem.animal.piquete.nome.includes(this.filtro.piquete);
      });
    },

    limparFiltro() {
      this.filtro.dataPesagemInicio = '';
      this.filtro.dataPesagemFim = '';
      this.filtro.animal = '';
      this.filtro.pesoInicio = '';
      this.filtro.pesoFim = '';
      this.filtro.piquete = '';

      this.pesagens = this.pesagensDaApi;

      // Resetando as datas no DateRangePicker
      this.$refs.dateRangePicker.resetDates();
    },

    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },


    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    confirmarExclusaoPesagem(pesagem) {
      this.formData.id = pesagem.id;
    },

    acessarEdicao(pesagem) {
      this.$router.push({
        name: 'PesagemEdicao',
        params: { pesagemId: pesagem.id }
      })
    },

    acessarCadastro() {
      this.$router.push({
        name: 'PesagemCadastro',
      })
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    replacePontoVirgula(valorString) {
      valorString = valorString.replace(".", ",");

      return valorString;
    },
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

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
  background-image: url('../assets/logo-sem-fundo.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}

nav, .tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
}

.table-container, .button-container {
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
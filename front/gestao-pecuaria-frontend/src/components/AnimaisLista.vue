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
      <form @submit.prevent="aplicarFiltro" class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="brinco" class="form-label me-2">Brinco</label>
          <input type="text" @input="aplicarBrincoMask" class="form-control" id="brinco" v-model="filtro.brinco">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataNascimento" class="form-label me-2">Data de Nascimento</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Início"
            class="form-control" id="dataNascimentoInicio" v-model="formData.dataNascimentoInicio">
        </div>
        <div class="col-auto d-flex align-items-center">
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Fim"
            class="form-control" id="dataNascimentoFim" v-model="formData.dataNascimentoFim">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="sexo" class="form-label me-2">Sexo</label>
          <select class="form-select" id="sexo" v-model="filtro.sexo">
            <option value="">Selecione o sexo</option>
            <option value="macho">Macho</option>
            <option value="femea">Fêmea</option>
          </select>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="raca" class="form-label me-2">Raça</label>
          <input type="text" class="form-control" id="raca" v-model="filtro.raca">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="brincoPai" class="form-label me-2">Brinco Pai</label> 
          <input type="text" @input="aplicarBrincoPaiMask" class="form-control" id="brincoPai" v-model="filtro.brincoPai">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="brincoMae" class="form-label me-2">Brinco Mãe</label>
          <input type="text" @input="aplicarBrincoMaeMask" class="form-control" id="brincoMae" v-model="filtro.brincoMae">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="piquete" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control" id="piquete" v-model="filtro.piquete">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="status" class="form-label me-2">Status</label>
          <select class="form-select" id="status" v-model="filtro.status">
            <option value="">Selecione o status</option>
            <option >Morto</option>
            <option >Vivo</option>
            <option >Vendido</option>
          </select>
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button type="submit" class="btn btn-success">Filtrar</button>
        </div>
      </form>
    </div>

    <div>
      <div class="table-container">
        <div class="button-container">
          <button @click="acessarCadastro()" type="button"
            class="btn btn-success">Cadastrar Animal</button>

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
                  <button @click="vizualizarAnimal(animal)" class="btn-acoes btn-sm"><i class="fas fa-eye"></i></button>
                  <button @click="editarAnimal(animal)" class="btn-acoes" data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
                </div>
              </td>

            </tr>
          </tbody>
        </table>
      </div>


      <!-- Modal de Confirmação de Exclusão -->
      <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
        aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir este animal?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarAnimal">Excluir</button>
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

export default {
  mixins: [masksMixin],

  name: 'TelaAnimais',
  data() {
    return {
      animais: [],
      animaisDaApi: [],
      racas: [],
      piquetes: [],
      listaMachos: [],
      listaFemeas: [],
      femeasFiltradas: [],
      machosFiltrados: [],
      comprado: false,
      formData: {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: null,
        racaObservacao: null,
        piquete: '',
        brincoPai: '',
        brincoMae: '',
        status: 'Vivo',
        rfid: '',
        observacoes: '',
        dataBaixa: null,
        dataCompra: null,
        valorCompra: null,
      },
      mostrarFormulario: false,
      filtro: {
        brinco: '',
        dataNascimento: '',
        sexo: '',
        raca: '',
        brincoPai: '',
        brincoMae: '',
        observacoes: '',
        piquete: '',
        status: '',
      },
      novaOcorrencia: {
        dataOcorrencia: '',
        tipoOcorrencia: '',
        descricao: null,
      },
      modalTitle: 'Cadastro de Animal',
    }
  },
  async mounted() {
    this.buscarAnimaisDaApi();
    this.buscarRacasDaApi();
    this.buscarPiquetesDaApi();
  },

  methods: {
    aplicarBrincoMask(event){
      const value = event.target.value;
      this.filtro.brinco =  this.brincoMask(value);
    },
    
    aplicarBrincoPaiMask(event){
      const value = event.target.value;
      this.filtro.brincoPai =  this.brincoMask(value);
    },

    aplicarBrincoMaeMask(event){
      const value = event.target.value;
      this.filtro.brincoMae =  this.brincoMask(value);
    },


    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/', {
        });
        this.racas = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },

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

    acessarCadastro(){
      this.$router.push({
          name: 'AnimaisCadastro',
          params: {animalJSON: 'animaisLista'}
        });
    },

    editarAnimal(animal) {
      this.modalTitle = 'Editar Animal';
      this.formData = {
        id: animal.id,
        brinco: animal.brinco,
        dataNascimento: animal.dataNascimento,
        sexo: animal.sexo,
        racaPredominante: animal.racaPredominante.id,
        racaObservacao: animal.racaObservacao,
        piquete: animal.piquete.id,
        brincoPai: animal.brincoPai,
        brincoMae: animal.brincoMae,
        status: 'Vivo',
        rfid: animal.rfid,
        observacoes: animal.observacoes,
        dataBaixa: animal.dataBaixa,
        dataCompra: animal.dataCompra,
        valorCompra: animal.valorCompra,
      };
    },

    resetForm() {
      this.formData = {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: null,
        racaObservacao: null,
        piquete: this.formData.piquete,
        status: 'Vivo',
        rfid: null,
        observacoes: null,
        dataBaixa: null,
        dataCompra: null,
        valorCompra: null,
      };
      this.modalTitle = 'Cadastro de Animal';
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async apagarAnimal() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/animais/${this.formData.id}/`, {
        });

        if (response.status === 204) {
          alert('Animal apagado com sucesso!');
          this.buscarAnimaisDaApi();
        } else {
          alert('Erro ao apagar animal. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal("confirmacaoExclusaoModal");
    },

    async submitForm() {
      if (this.modalTitle === 'Cadastro de Animal') {
        try {
          const response = await api.post(`http://127.0.0.1:8000/animais/`, this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
            this.preencherListaFemeas();
            this.preencherListaMachos();
          } else {
            alert('Erro ao cadastrar animal. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }

      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData, {
          });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
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

    async preencheListas() {
      this.preencherListaMachos();
      this.preencherListaFemeas();
    },

    async preencherListaFemeas() {
      const response = await api.get(`http://127.0.0.1:8000/animais/femeas`, {
        params: {
          propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
        },
      });
      this.listaFemeas = response.data;
    },

    async preencherListaMachos() {
      const response = await api.get(`http://127.0.0.1:8000/animais/machos`, {
        params: {
          propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
        },
      });
      this.listaMachos = response.data;
    },

    filterFemeas() {
      this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoMae));
    },

    filterMachos() {
      this.machosFiltrados = this.listaMachos.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoPai));
    },

    selectPai(animal) {
      this.formData.brincoPai = animal.brinco;
      this.machosFiltrados = [];
    },

    selectMae(animal) {
      this.formData.brincoMae = animal.brinco;
      this.femeasFiltradas = [];
    },

    formatarData(data) {
      const date = new Date(data);
      const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
      return utcDate.toLocaleDateString('pt-BR', options);
    },

    aplicarFiltro() {
      this.animais = this.animaisDaApi.filter(animal => {

        //essas verificações é para o caso de o ususario nao ter cadastrado raça, brinco pai ou brinco mae
        if(animal.raca == null){
          animal.raca = {nome: ''};
        }
        if(animal.brincoPai == null){
          animal.brincoPai = '';
        }
        if(animal.brincoMae == null){
          animal.brincoMae = '';
        }
        return  (new Date(animal.dataNascimento) >= new Date(this.filtro.dataNascimentoInicio || '1970-01-01')) &&
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
      this.filtro.dataNascimento = '';
      this.filtro.sexo = '';
      this.filtro.raca = '';
      this.filtro.brincoPai = '';
      this.filtro.brincoMae = '';
      this.filtro.piquete = '';
      this.filtro.status = '';

      this.animais = this.animaisDaApi;
    },
    
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },

    vizualizarAnimal(animal) {
      this.$router.push({
        name: 'VizualizarAnimal', 
        params: { animalId: animal.id } 
      })
    }

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
}

.table-container table tbody tr td {
  background-color: #f0f0f0;
  /* Cor de fundo das células da tabela */
}

.button-container {
  text-align: left;
  margin-bottom: 20px;
  margin-right: 10px;
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
</style>
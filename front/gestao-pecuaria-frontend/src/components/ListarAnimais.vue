<template>
<div>
  <h2>Animais</h2>
  <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="brinco" class="form-label me-2">Brinco</label>
          <input type="text" class="form-control" id="brinco" v-model="filtro.brinco">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataNascimento" class="form-label me-2">Data de Nascimento</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data de nascimento" 
          class="form-control" id="dataNascimento" v-model="formData.dataNascimento" required>
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
          <input type="text" class="form-control" id="brincoPai" v-model="filtro.brincoPai">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="brincoMae" class="form-label me-2">Brinco Mãe</label>
          <input type="text" class="form-control" id="brincoMae" v-model="filtro.brincoMae">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="observacoes" class="form-label me-2">Observações</label>
          <input type="text" class="form-control" id="observacoes" v-model="filtro.observacoes">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="piquete" class="form-label me-2">Piquete</label>
          <input type="text" class="form-control" id="piquete" v-model="filtro.piquete">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="status" class="form-label me-2">Status</label>
          <select class="form-select" id="status" v-model="filtro.status">
            <option value="">Selecione o status</option>
            <option value="morto">Morto</option>
            <option value="Vivo">Vivo</option>
            <option value="desaparecido">Desaparecido</option>
            <option value="vendido">vendido</option>
          </select>
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary me-2" @click="limparFiltro">Limpar</button>
          <button class="btn btn-success" @click="aplicarFiltro">Filtrar</button>
        </div>
      </form>
    </div>

  <div>
    <div class="table-container">
      <div class="button-container">
    <button @click="resetForm(); preencheListas()" type="button" class="btn btn-success" data-bs-toggle="modal"
      data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Adicionar</button>
  </div>
      <table class="table table-bordered">
        <thead >
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
          <tr v-for="(animal, index) in animais" :key="index" :class="{'status-Vivo': animal.status === 'Vivo', 'status-morto': animal.status === 'morto', 'status-doente': animal.status === 'doente'}">
            <td>{{ animal.brinco }}</td>
            <td>{{ formatarData(animal.dataNascimento) }}</td>
            <td>{{ animal.sexo }}</td>
            <td>{{ animal.piquete.nome }}</td>
            <td>{{ animal.status }}</td>
            <td>
              <div class="button-group">
                <button @click="vizualizarAnimal(animal)" class="btn-acoes btn-sm" ><i class="fas fa-eye"></i></button>
                
                <button @click="editarAnimal(animal)" class="btn-acoes" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
              </div>
            </td>

          </tr>
        </tbody>
      </table>
  </div>

    <!-- Modal de Cadastro -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de animal</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tag"></i>*</span>
              <select v-model="formData.piquete" class="form-select" id="piquete" aria-label="Piquete"
                placeholder="Selecione o piquete" required>
                <option disabled value="">Selecione o piquete</option>
                <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{ piquete.nome }}</option>
              </select>
            </div>
            <hr>
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i>*</span>
                <input v-model="formData.brinco" type="text" class="form-control" id="brinco"
                  placeholder="Número do Brinco" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar">*</i></span>
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data de nascimento" 
                class="form-control" id="dataNascimentoCadastro" v-model="formData.dataNascimento" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus-mars">*</i></span>
                <select v-model="formData.sexo" class="form-select" id="sexo" aria-label="Sexo" required
                  placeholder="Selecione o sexo">
                  <option disabled value="">Selecione o sexo</option>
                  <option value="macho">Macho</option>
                  <option value="femea">Fêmea</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-horse"></i></span>
                <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante"
                  aria-label="Raça Predominante" required>
                  <option disabled value="">Selecione a raça predominante</option>
                  <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacao"
                  placeholder="Observações sobre a Raça"></textarea>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-mars"></i></span>
                <input v-model="formData.brincoPai" @input="filterMachos()" type="text" class="form-control"
                  placeholder="Digite o brinco do Pai...">
              </div>
              <div class="list-group" v-if="formData.brincoPai && machosFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="animal in machosFiltrados"
                  :key="animal.id" @click="selectPai(animal)">
                  {{ animal.brinco }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus"></i></span>
                <input v-model="formData.brincoMae" @input="filterFemeas()" type="text" class="form-control"
                  placeholder="Digite o brinco da Mãe...">
              </div>
              <div class="list-group" v-if="formData.brincoMae && femeasFiltradas.length">
                <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                  :key="animal.id" @click="selectMae(animal)">
                  {{ animal.brinco }}
                </button>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="formData.rfid" type="text" class="form-control" id="rfid"
                  placeholder="RFID" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="formData.observacoes" type="text" class="form-control" id="observacoes"
                  placeholder="Observações" required>
              </div>
              <div class="mb-3 input-group">
                <input v-model="comprado" type="checkbox" id="check-comprado">  Animal Comprado
              </div>
              <div v-if="comprado" class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar">*</i></span>
                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da compra" 
                class="form-control" id="dataDaCompra" v-model="formData.dataCompra" required>
              </div>
              <div v-if="comprado" class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-weight"></i>*</span>
                <input v-model="formData.valorCompra" type="text" class="form-control" id="valorCompra"  placeholder="Valor da compra" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
      aria-hidden="true">
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

export default {
  name: 'TelaAnimais',
  data() {
    return {
      animais: [],
      racas: [],
      piquetes: [],
      listaMachos:[],
      listaFemeas:[],
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
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar animais da API:', error);
      }
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

    async preencheListas(){
      this.preencherListaMachos();
      this.preencherListaFemeas();
    },

    async preencherListaFemeas(){
      const response = await api.get(`http://127.0.0.1:8000/animais/femeas`, {
        params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
      });
      this.listaFemeas = response.data;
    },

    async preencherListaMachos(){
      const response = await api.get(`http://127.0.0.1:8000/animais/machos`, {
        params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
      });
      this.listaMachos = response.data;
    },

    filterFemeas(){
      this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoMae));
    },

    filterMachos(){
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
      // Implementar a lógica para aplicar o filtro
    },
    limparFiltro() {
      this.filtro.brinco ='';
      this.filtro.dataNascimento ='';
      this.filtro.sexo ='';
      this.filtro.raca ='';
      this.filtro.brincoPai ='';
      this.filtro.brincoMae =''; 
      this.filtro.observacoes =''; 
      this.filtro.piquete =''; 
      this.filtro.status =''; 
    },
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },
    
  vizualizarAnimal(animal) {
    localStorage.setItem('animalSelecionado', animal.id);
    this.$router.push('/vizualizarAnimal');
  }

  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

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

.table-container table thead tr th {
  border-bottom: 2px solid #4CAF50; /* Adiciona uma borda verde na parte inferior */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
}

.btn-acoes i {
  color: #4CAF50;
}

.button-group {
  display: flex;
  gap: 10px; 
}
.status-Vivo {
  background-color: #d4edda; /* Verde claro para 'Vivo' */
}

.status-morto {
  background-color: #f8d7da; /* Vermelho claro para 'morto' */
}

.status-doente {
  background-color: #fff3cd; /* Amarelo claro para 'doente' */
}
</style>
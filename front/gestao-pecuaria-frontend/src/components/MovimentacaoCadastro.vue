<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'movimentacoes' }" id="nav-vet-tab" @click="selectTab('movimentacoes')" 
        type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Lista de Movimentação</button>
        <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
        type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Movimentação</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'movimentacoes' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'cadastro' }" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Cadastro de Movimentação</h1>
            <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da movimentação" 
                    class="form-control" id="dataMovimentacaoCadastro" v-model="formData.dataMovimentacao" required>
                </div>
                <div class="mb-3 input-group">
                    <input type="radio" v-model="radioEscolha" value="brinco"> Animal
                </div>
                <div class="mb-3 input-group">
                    <input type="radio" v-model="radioEscolha" value="piquete"> Todos animais do piquete
                </div>
                <div class="mb-3 input-group" v-if="radioEscolha === 'brinco'">
                    <input v-model="brinco" @input="filterAnimais" type="text" class="form-control" placeholder="Digite o brinco...">
                </div>
                <div class="list-group" v-if="brinco && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                    {{ animal.brinco }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                  <input v-model="piqueteOrigemNome" @input="filtrarPiquetesOrigem()" type="text" class="form-control"
                    placeholder="Piquete de Origem..." :disabled="(radioEscolha === 'brinco')">
                </div>
                <div class="list-group" v-if="piqueteOrigemNome && filteredPiquetesOrigem.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetesOrigem"
                    :key="piquete.id" @click="selecionarPiqueteOrigem(piquete)">
                    {{ piquete.nome }}
                  </button>
                </div>

                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-hashtag"></i></span>
                  <input v-model="piqueteDestinoNome" @input="filtrarPiquetesDestino()" type="text" class="form-control"
                    placeholder="Piquete de Destino...">
                </div>
                <div class="list-group" v-if="piqueteDestinoNome && filteredPiquetesDestino.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetesDestino"
                    :key="piquete.id" @click="selecionarPiqueteDestino(piquete)">
                    {{ piquete.nome }} - {{ piquete.propriedade.nome }}
                  </button>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.motivo" type="text" class="form-control" id="motivo" 
                    placeholder="Motivo">
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('movimentacoes')">Cancelar</button>
                    <button type="button" class="btn btn-success" @click="submitForm">Enviar</button>
                </div>
            </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  data() {
    return {
      activeTab: 'cadastro',  // Aba inicial é 'cadastro'
      animais: [],
      animaisFiltrados: [],
      brinco: '',
      piquetes: [],
      piquetesDaPropriedade: [],
      piqueteOrigemNome: '',
      piqueteDestinoNome: '',
      piqueteId: null,
      filteredPiquetesOrigem: [],
      filteredPiquetesDestino: [],
      radioEscolha: 'brinco',
      formData: {
          animal: [],
          dataMovimentacao: null,
          piqueteOrigem: null,
          piqueteDestino: null,
          motivo: null,
      },
      isAnimalValido: true,
      isDataValida: true,
      isPiqueteOrigemValido: true,
      isPiqueteDestinoValido: true,
      isMotivoKgValido: true,
      animalPlaceholder: 'Brinco do animal',
      dataPlaceholder: 'Data da movimentacao',
      piqueteOrigemPlaceholder: 'Piquete de Origem',
      piqueteDestinoPlaceholder: 'Piquete de Destino',
      motivoPlaceholder: 'Motivo da movimentação',
    };
  },

    mounted() {
    this.buscarAnimaisDaApi();
    this.buscarPiquetesDaApi();
    this.buscarPiquetesDaPropriedade();
  },

  methods: {
    async buscarAnimaisDaApi() {
        try {
            const response = await api.get('http://127.0.0.1:8000/animais/vivos-piquetes' , {
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
        const response = await api.get('http://127.0.0.1:8000/piquetes/piquetes-propriedades');
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarPiquetesDaPropriedade() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes', {
          params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
        });
        this.piquetesDaPropriedade = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    filtrarPiquetesOrigem() {
      this.filteredPiquetesOrigem = this.piquetesDaPropriedade.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteOrigemNome));
    },

    selecionarPiqueteOrigem(piquete) {
      this.piqueteId = piquete.id;
      this.formData.piqueteOrigem = piquete.id;
      this.piqueteOrigemNome = piquete.nome + " - " + piquete.propriedade.nome;
      this.filteredPiquetesOrigem = [];
      this.preencheListaAnimais()
    },


    filtrarPiquetesDestino() {
      this.filteredPiquetesDestino = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteDestinoNome));
    },

    selecionarPiqueteDestino(piquete) {
      this.piqueteDestinoNome = piquete.nome + " - " + piquete.propriedade.nome;
      this.formData.piqueteDestino = piquete.id;
      this.filteredPiquetesDestino = [];
    },
    
    filterAnimais() {
        this.animaisFiltrados = this.animais.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectAnimal(animal) {
      console.log();
        this.formData.animal = [];
        this.brinco = animal.brinco;
        this.formData.piqueteOrigem = animal.piquete.id;
        this.piqueteOrigemNome = animal.piquete.nome
        this.formData.animal.push(animal.id);
        this.animaisFiltrados = [];
    },

    preencheListaAnimais(){
      this.formData.animal = [];
      let listaAnimais;
      listaAnimais = this.animais.filter(animal => animal.piquete.id == this.piqueteId);
      listaAnimais.forEach(animal => {
          this.formData.animal.push(animal.id);
      });
    },

    validarFormulario(){
        //AQUI FALTA FAZER A VALIDAÇÂO. VER PAGINA DE VETERINARIOS
        return true;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'movimentacoes') {
        this.$router.push('/movimentacoes');
      }
    },

    async submitForm() {
      console.log(this.formData);
      if (this.validarFormulario()) {
        try {
          const response = await api.post('http://127.0.0.1:8000/movimentacoes/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.$router.push('/movimentacoes');
          } else {
            alert('Erro ao cadastrar movimentacao. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
    },

    resetForm() {
      this.formData = {
          animal: [],
          dataMovimentacao: null,
          piqueteOrigem: null,
          piqueteDestino: null,
          motivo: null,
      },
      this.isAnimalValido = true,
      this.isDataValida = true,
      this.isPiqueteOrigemValido = true,
      this.isPiqueteDestinoValido = true,
      this.isMotivoKgValido = true,
      this.animalPlaceholder = 'Brinco do animal',
      this.dataPlaceholder = 'Data da movimentacao',
      this.piqueteOrigemPlaceholder = 'Piquete de Origem',
      this.piqueteDestinoPlaceholder = 'Piquete de Destino',
      this.motivoPlaceholder = 'Motivo da movimentação'
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

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

.btn-success {
  background-color: #176d1a;
}

.button-group {
  display: flex;
  gap: 10px;
}

.is-invalid {
  border-color: #dc3545;
}

</style>

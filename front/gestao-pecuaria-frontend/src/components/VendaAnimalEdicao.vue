
<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'vendas' }" id="nav-vet-tab"
          @click="selectTab('vendas')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Lista de Vendas</button>
        <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-vet-tab"
          @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-vet"
          aria-selected="true">Visualização de Vendas</button>
        <button class="nav-link" :class="{ active: activeTab === 'edicao' }" id="nav-edicao-tab"
          @click="selectTab('edicao')" type="button" role="tab" aria-controls="nav-edicao"
          aria-selected="false">Edição de Venda</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'vendas' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'edicao' }" id="nav-edicao" role="tabpanel"
        aria-labelledby="nav-edicao-tab">
        <div class="table-container" id="edicao" tabindex="-1" aria-labelledby="edicaoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="edicaoLabel">Edição de Venda</h1>
          <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da venda" 
                    class="form-control" id="dataVenda" v-model="formData.dataVenda" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input @input="atualizaValorTotalPeloPrecoKg()" v-model="formData.precoKg" type="text" class="form-control" id="precoKg" placeholder="Preço por Kg" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <select v-model="formData.finalidade" class="form-select" id="finalidade" aria-label="Finalidade"
                    placeholder="Selecione o tipo" required>
                    <option disabled value="">Finalidade</option>
                    <option value="Cria">Cria</option>
                    <option value="Recria">Recria</option>
                    <option value="Engorda">Engorda</option>
                    <option value="Abate">Abate</option>
                </select>
                </div>
                <div class="mb-3 input-group">
                    <input v-model="brinco" @input="filterAnimais" type="text" class="form-control" placeholder="Digite o brinco...">
                </div>
                <div class="list-group" v-if="brinco && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action" v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                    {{ animal.brinco }}
                    </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input @input="atualizaValorTotalPeloPeso()" v-model="formData.peso" type="text" class="form-control" id="peso" placeholder="Peso" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-tags"></i></span>
                  <input v-model="formData.valorTotal" type="text" class="form-control" id="valorTotal" placeholder="Valor Total" required>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                  <textarea v-model="formData.observacao" class="form-control" id="observacao"
                    placeholder="Observação"></textarea>
                </div>
                <div class="button-group justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="selectTab('visualizacao')">Cancelar</button>
                    <button type="button" class="btn btn-success" @click="submitForm">Salvar</button>
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
            activeTab: 'edicao', // Começa na aba de edição
            animais: [],
            animaisFiltrados: [],
            brinco: '',
            dataSelecionada: null,
            formData: {
              id: null,
              animal: '',
              dataVenda: '',
              peso: '',
              precoKg: '',
              valorTotal: '',
              finalidade: '',
              observacao: null,
            },
            isAnimalValido: true,
            isDataValida: true,
            isPesoValido: true,
            isprecoKgValido: true,
            isValorTotalValido: true,
            isFinalidadeValida: true,
            animalPlaceholder: 'Brinco do animal',
            dataPlaceholder: 'Data da venda',
            pesoPlaceholder: 'Peso do animal',
            precoKgPlaceholder: 'Preço por KG',
            valorTotalPlaceholder: 'Valor Total',
            finalidadePlaceholder: 'Finalidade',
        };
    },
 
    mounted() {
        const vendaId = this.$route.params.vendaId;
        if (vendaId) {
            this.fetchVenda(vendaId);
        }
    },
    methods: {
    async fetchVenda(id) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/vendas-animais/${id}`);
        const venda = response.data;
        this.formData.id = venda.id;
        this.formData.animal = venda.animal.id;
        this.formData.dataVenda = venda.dataVenda;
        this.formData.peso = venda.peso;
        this.formData.precoKg = venda.precoKg;
        this.formData.valorTotal = venda.valorTotal;
        this.formData.finalidade = venda.finalidade;
        this.formData.observacao = venda.observacao;

        this.brinco = venda.animal.brinco;
        this.dataSelecionada = venda.dataVenda
      } catch (error) {
        console.error('Erro ao carregar dados da venda:', error);
      }
    },
    validarFormulario() {
      return true;
    },

    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'vendas') {
        this.$router.push('/vendas-animais');
      }
      else if(tab === 'visualizacao'){
        this.$router.push({
            name: 'VendaAnimalVisualizacao', 
            params: { dataSelecionada: this.dataSelecionada } 
        })
      }
    },

    cancelarEdicao() {
      this.$router.push('/vendas-animais');
    },

    async submitForm() {
      if (this.validarFormulario()) {
       try {
          const response = await api.patch(`http://127.0.0.1:8000/vendas/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.$router.push('/vendas-animais');
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
    },

    resetForm() {
      this.formData = {
        id: null,
        animal: '',
        dataVenda: '',
        peso: '',
        precoKg: '',
        valorTotal: '',
        finalidade: '',
        observacao: null,
      },
      this.this.this.isAnimalValido = true,
      this.this.isDataValida = true,
      this.isPesoValido =  true,
      this.isprecoKgValido = true,
      this.isValorTotalValido = true,
      this.isFinalidadeValida = true,
      this.animalPlaceholder = 'Brinco do animal',
      this.dataPlaceholder = 'Data da venda',
      this.pesoPlaceholder = 'Peso do animal',
      this.precoKgPlaceholder = 'Preço por KG',
      this.valorTotalPlaceholder = 'Valor Total',
      this.finalidadePlaceholder = 'Finalidade'
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

<template>
<div class="background">
  <h2>Movimentações</h2>
    <div class="d-flex align-items-start table-container flex-column">
      <div class="d-flex align-items-start">
        <h2 class="me-3">Filtros</h2>
        <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
      </div>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario">
        <div class="col-auto d-flex align-items-center">
          <label for="nome" class="form-label me-2">Animal</label>
          <input type="text" class="form-control" id="animal" v-model="filtro.animal">
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataCompra" class="form-label me-2">Data</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação" 
          class="form-control" id="dataMovimentacao" v-model="filtro.dataMovimentacao" required>
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
      <button @click="resetForm()" type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Movimentação</button>
    </div>
      <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data da Movimentação</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(data, index) in datasMovimentacoes" :key="index">
              <td>{{ formatarData(data) }}</td>
              <td>
                <button @click="preencherDetalhesMovimentacaoPorData(data)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                  data-bs-target="#visualizacaoModal"><i class="fas fa-eye"></i></button>
                <button @click="confirmarExclusao(data)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
    </div>
        <!-- Modal de Cadastro de Aplicação -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Movimentação</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
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
                    {{ piquete.nome }} - {{ piquete.propriedade.nome }}
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
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Enviar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Visualização de Inseminações -->
    <div class="modal fade" id="visualizacaoModal" tabindex="-1" aria-labelledby="visualizacaoModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="visualizacaoModalLabel">Detalhes da Movimentação</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Data da Movimentacao:</strong> {{ formatarData(this.dataSelecionada) }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Animal</th>
                  <th scope="col">Piquete de origem</th>
                  <th scope="col">Piquete de destino</th>
                  <th scope="col">Tipo</th>
                  <th scope="col">Motivo</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="movimentacao in this.detalhesMovimentacao" :key="movimentacao.id">
                  <td>{{ movimentacao.animal.brinco}}</td>
                  <td>{{ movimentacao.piqueteOrigem.nome}} - {{ movimentacao.piqueteOrigem.propriedade.nome }}</td>
                  <td>{{ movimentacao.piqueteDestino.nome}} - {{ movimentacao.piqueteDestino.propriedade.nome }}</td>
                  <td>{{ achaTipo(movimentacao)}}</td>
                  <td>{{ movimentacao.motivo}}</td>
                  <td>
                    <button @click="editarMovimentacao(movimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                    <button @click="confirmarExclusaoMovimentacao(movimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#confirmacaoExclusaoAnimalModal"><i class="fas fa-trash-alt"></i></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição de Aplicação -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Movimentação</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
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
                    placeholder="Piquete de Origem...">
                </div>
                <div class="list-group" v-if="piqueteOrigemNome && filteredPiquetesOrigem.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="piquete in filteredPiquetesOrigem"
                    :key="piquete.id" @click="selecionarPiqueteOrigem(piquete)">
                    {{ piquete.nome }} - {{ piquete.propriedade.nome }}
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
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Salvar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão da data -->
      <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
        aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Tem certeza de que deseja excluir esta Movimentação?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarMovimentacaoPorData">Excluir</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de Confirmação de Exclusão do animal da movimentação -->
      <div class="modal fade" id="confirmacaoExclusaoAnimalModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoAnimalModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoAnimalModalLabel">Confirmação de Exclusão de Movimentação do Animal</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir este animal da Movimentação?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarMovimentacao">Excluir</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
</template>

<script>
import api from '/src/interceptadorAxios'

export default {
  name: 'TelaMovimentcoes',
  data() {
    return {
        animais: [],
        animaisFiltrados: [],
        brinco: '',
        movimentacoes: [],
        datasMovimentacoes: [],
        dataSelecionada: null,
        detalhesMovimentacao: [],
        movimentacaoParaExcluir: null,
        dataParaExclusao: null,
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
      mostrarFormulario: false,
      filtro: {
        animal: [],
        dataMovimentacao: '',
      },
      modalTitle: 'Cadastro de Movimentacao',
    }

  },
  mounted() {
    this.buscarAnimaisDaApi();
    this.buscarMovimentacoesDaApi();
    this.buscarPiquetesDaApi();
    this.buscarPiquetesDaPropriedade();
  },
  methods: {
    
    async preencherdatasMovimentacoes(){
      const datasSet = new Set();
      this.movimentacoes.forEach(movimentacao => {
        datasSet.add(movimentacao.dataMovimentacao);
      });
      this.datasMovimentacoes = Array.from(datasSet).sort((b, a) => new Date(a) - new Date(b));
    },

    async preencherDetalhesMovimentacaoPorData(data){
      this.detalhesMovimentacao = []
      this.movimentacoes.forEach(movimentacao => {
        if(data === movimentacao.dataMovimentacao){
          this.detalhesMovimentacao.push(movimentacao);
        }
      });
      this.dataSelecionada = data;
    },

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

    filtrarPiquetesDestino() {
      this.filteredPiquetesDestino = this.piquetes.filter(piquete => piquete.nome.toLowerCase().includes(this.piqueteDestinoNome));
    },

    selecionarPiqueteOrigem(piquete) {
      this.piqueteId = piquete.id;
      this.formData.piqueteOrigem = piquete.id;
      this.piqueteOrigemNome = piquete.nome + " - " + piquete.propriedade.nome;
      this.filteredPiquetesOrigem = [];
      this.preencheListaAnimais()
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
        this.formData.animal = [];
        this.brinco = animal.brinco;
        this.formData.piqueteOrigem = animal.piquete.id;
        this.piqueteOrigemNome = animal.piquete.nome
        this.formData.animal.push(animal.id);
        this.animaisFiltrados = [];
    },
    


    async buscarMovimentacoesDaApi(){
        try {
            const response = await api.get('http://127.0.0.1:8000/movimentacoes/' , {
              params: {
                propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
            },
            });
            this.movimentacoes = response.data;
            this.preencherdatasMovimentacoes();
        } catch (error) {
        console.error('Erro ao buscar aplicações de produtos da API:', error);
        }
    },

    achaTipo(movimentacao){ 
      if(movimentacao.piqueteOrigem.propriedade.id == localStorage.getItem('propriedadeSelecionada')
      && movimentacao.piqueteDestino.propriedade.id == localStorage.getItem('propriedadeSelecionada')){
        return 'Interna'
      }
      else if(movimentacao.piqueteOrigem.propriedade.id == localStorage.getItem('propriedadeSelecionada')){
        return 'Saída'
      }
      else{
        return 'Entrada'
      }
    },

    editarMovimentacao(movimentacao) {
      this.modalTitle = 'Editar Aplicacao';
      this.formData = {
        id: movimentacao.id,
        animal: movimentacao.animal.id,
        dataMovimentacao: movimentacao.dataMovimentacao,
        piqueteOrigem: movimentacao.piqueteOrigem.id,
        piqueteDestino: movimentacao.piqueteDestino.id,
        motivo: movimentacao.motivo,
      };

      this.piqueteOrigemNome = movimentacao.piqueteOrigem.nome
      this.piqueteDestinoNome = movimentacao.piqueteDestino.nome
      this.brinco = movimentacao.animal.brinco;
    },

    preencheListaAnimais(){
      this.formData.animal = [];
      let listaAnimais;
      listaAnimais = this.animais.filter(animal => animal.piquete.id == this.piqueteId);
      listaAnimais.forEach(animal => {
          this.formData.animal.push(animal.id);
      });
    },

    resetForm() {
      this.formData = {
        id: null,
        animal: [],
        dataMovimentacao: '',
        piqueteOrigem: '',
        piqueteDestino: '',
        motivo: null,
      };
      this.brinco = '';
      this.piqueteOrigemNome = '';
      this.piqueteDestinoNome = '';
      this.modalTitle = 'Cadastro de Movimentacao';
    },

    fecharModal(modalId) {
      var closeButton = document.getElementById(modalId).querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Botão de fechar não encontrado no modal:', modalId);
      }
    },

    async submitForm() {
      
      if (this.modalTitle === 'Cadastro de Movimentacao') {
        try {
          const response = await api.post('http://127.0.0.1:8000/movimentacoes/', this.formData , {
        });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarMovimentacoesDaApi();
            this.fecharModal("cadastroModal");
          } else {
            alert('Erro ao cadastrar aplicação de produto. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/movimentacoes/${this.formData.id}/`, this.formData , {
        });

          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarMovimentacoesDaApi();
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

    confirmarExclusao(data) {
      this.dataParaExclusao = data;
    },

    confirmarExclusaoMovimentacao(movimentacao) {
      this.movimentacaoParaExcluir = movimentacao;
    },

    async apagarMovimentacaoPorData() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/movimentacoes/datas/${this.dataParaExclusao}/`, {
        });

        if (response.status === 204) {
          alert('Aplicação excluída com sucesso!');
          this.dataParaExclusao = null;
          this.buscarMovimentacoesDaApi();
        } else {
          alert('Erro ao excluir aplicação. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoModal');
    },
    
    async apagarMovimentacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/movimentacoes/${this.movimentacaoParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Aplicação excluído com sucesso!');
          this.detalhesMovimentacao = this.detalhesMovimentacao.filter(animal => animal.id !== this.movimentacaoParaExcluir.id);
          this.movimentacaoParaExcluir = null;
          this.buscarMovimentacoesDaApi();
        } else {
          alert('Erro ao excluir a aplicação. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoAnimalModal');
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
      this.filtro = {
        animal: '',
        dataMovimentacao: '',
      };
    },
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.background {
  background-color:  #f0f0f0; /* Um tom mais escuro que o branco */
  min-height: 100vh; /* Garante que o fundo cubra toda a altura da tela */
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

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a; /* Adiciona uma borda verde na parte inferior */
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

</style>
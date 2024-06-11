<template>
  <div>
    <div class="table-container">
      <h2>Inseminações</h2>
      <form class="row g-3 align-items-center" v-show="mostrarFormulario" @submit.prevent="submitForm">
        <div class="col-auto d-flex align-items-center">
          <label for="animal" class="form-label me-2">Animal</label>
          <input type="text" class="form-control" id="animal" v-model="formData.animal" required>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="dataInseminacao" class="form-label me-2">Data de Inseminação</label>
          <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da inseminação" 
          class="form-control" id="dataInseminacao" v-model="formData.dataInseminacao" required>
        </div>
        <div class="col-auto d-flex align-items-center">
          <label for="identificadorTouro" class="form-label me-2">Identificador do Touro</label>
          <input type="text" class="form-control" id="identificadorTouro" v-model="formData.identificadorTouro"
            required>
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary me-2" type="button" @click="limparFormulario">Limpar</button>
          <button class="btn btn-success" type="submit">Salvar</button>
        </div>
      </form>
    </div>
    
    <div>
      <div class="table-container">
        <div class="button-container">
          <button @click="resetForm(); preencherListaFemeas()" type="button" class="btn btn-success"
            data-bs-toggle="modal" data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Adicionar</button>
        </div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Data Inseminação</th>
              <th scope="col">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(data, index) in datasInseminacoes" :key="index">
              <td>{{ formatarData(data) }}</td>
              <td>
                <button @click="preencherDetalhesInseminacaoPorData(data)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                  data-bs-target="#visualizacaoModal"><i class="fas fa-eye"></i></button>
                <button @click="confirmarExclusao(data)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                  data-bs-target="#confirmacaoExclusaoModal"><i class="fas fa-trash-alt"></i></button>
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
              <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Inseminacoes</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                  <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da inseminação" 
                  class="form-control" id="dataInseminacaoCadastro" v-model="formData.dataInseminacao" required>
                </div>
                <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="nomeVet" @input="filterVeterinario" type="text" class="form-control"
                  placeholder="Digite o Veterinario">
                </div>
                <div class="list-group" v-if="nomeVet && veterinariosFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action"
                  v-for="veterinario in veterinariosFiltrados" :key="veterinario.id" @click="selectVeterinario(veterinario)">
                  {{ veterinario.nome }}
                </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                  <input v-model="formData.identificadorTouro" type="text" class="form-control" id="identificadorTouro"
                    placeholder="Indentificador Touro" required>
                </div>
                <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus"></i></span>
                <input v-model="brinco" @input="filterFemeas()" type="text" class="form-control"
                  placeholder="Digite o animal">
                </div>
                <div class="list-group" v-if="brinco && femeasFiltradas.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                    :key="animal.id" @click="selectMae(animal)">
                    {{ animal.brinco }}
                  </button>
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
            <h1 class="modal-title fs-5" id="visualizacaoModalLabel">Detalhes da Inseminação</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Data da Inseminação:</strong> {{ formatarData(this.dataSelecionada) }}</p>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Animal</th>
                  <th scope="col">Veterinario</th>
                  <th scope="col">Touro</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="inseminacao in this.detalhesInseminacao" :key="inseminacao.id">
                  <td>{{ inseminacao.animal.brinco}}</td>
                  <td>{{ inseminacao.veterinario.nome}}</td>
                  <td>{{ inseminacao.identificadorTouro}}</td>
                  <td>
                    <button @click="editarInseminacao(inseminacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                    <button @click="confirmarExclusaoInsemincao(inseminacao)" class="btn-acoes btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#confirmacaoExclusaoAnimalModal"><i class="fas fa-trash-alt"></i></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

      <!-- Modal de Edição -->
      <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Inseminacoes</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                  <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da inseminação" 
                  class="form-control" id="dataInseminacaoCadastro" v-model="formData.dataInseminacao" required>
                </div>
                <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="nomeVet" @input="filterVeterinario" type="text" class="form-control"
                  placeholder="Digite o Veterinario">
                </div>
                <div class="list-group" v-if="nomeVet && veterinariosFiltrados.length">
                <button type="button" class="list-group-item list-group-item-action"
                  v-for="veterinario in veterinariosFiltrados" :key="veterinario.id" @click="selectVeterinario(veterinario)">
                  {{ veterinario.nome }}
                </button>
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                  <input v-model="formData.identificadorTouro" type="text" class="form-control" id="identificadorTouro"
                    placeholder="Indentificador Touro" required>
                </div>
                <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus"></i></span>
                <input v-model="brinco" @input="filterFemeas()" type="text" class="form-control"
                  placeholder="Digite o animal">
                </div>
                <div class="list-group" v-if="brinco && femeasFiltradas.length">
                  <button type="button" class="list-group-item list-group-item-action" v-for="animal in femeasFiltradas"
                    :key="animal.id" @click="selectMae(animal)">
                    {{ animal.brinco }}
                  </button>
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
              Tem certeza de que deseja excluir esta inseminação?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="apagarInseminacaoPorData">Excluir</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de Confirmação de Exclusão do animal da Inseminacao -->
      <div class="modal fade" id="confirmacaoExclusaoAnimalModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoAnimalModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoAnimalModalLabel">Confirmação de Exclusão de Animal</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir este animal da inseminação?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarInseminacao">Excluir</button>
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
  name: 'TelaInseminacoes',
  data() {
    return {
      veterinarios: [],
      listaFemeas: [],
      femeasFiltradas: [],
      inseminacoes: [],
      nomeVet: '',
      brinco: '',
      veterinariosFiltrados: [],
      mostrarFormulario: false,
      detalhesInseminacao: [],
      inseminacaoParaExcluir: null,
      dataParaExclusao: null,
      datasInseminacoes: [], 
      dataSelecionada: null, 
      formData: {
        id: null,
        dataInseminacao: '',
        veterinario: '',
        animal: '',
        identificadorTouro: '',
      },
      filtro: {

        dataInseminacao: '',
        animal: '',
        identificadorTouro: '',
      },
      modalTitle: 'Cadastro de Animal',
    }
  },
  async mounted() {
    this.buscarFemeasVivasDaApi();
    this.buscarVeterinariossDaApi();
    this.buscarInseminacoesDaApi();
  },

  methods: {
    async buscarInseminacoesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/inseminacoes/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.inseminacoes = response.data;
        this.preencherDatasInseminacoes();
      } catch (error) {
        console.error('Erro ao buscar inseminacoes da API:', error);
      }
    },

    async buscarFemeasVivasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/femeas/vivas', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.animais = response.data;
      } catch (error) {
        console.error('Erro ao buscar inseminacoes da API:', error);
      }
    },

    async buscarVeterinariossDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/veterinarios/', {
        });
        this.veterinarios = response.data;
      } catch (error) {
        console.error('Erro ao buscar veterinarios da API:', error);
      }
    },
    filterVeterinario() {
      this.veterinariosFiltrados = this.veterinarios.filter(veterinario => veterinario.nome.toLowerCase().includes(this.nomeVet));
      console.log(this.veterinariosFiltrados);
    },
    selectVeterinario(veterinario) {
      this.nomeVet = veterinario.nome;
      this.formData.veterinario = veterinario.id;
      this.veterinariosFiltrados = [];
    },
    
    editarInseminacao(inseminacao) {
      this.modalTitle = 'Editar Inseminação';
      this.formData = {
        id: inseminacao.id,
        dataInseminacao: inseminacao.dataInseminacao,
        veterinario: inseminacao.veterinario.id,
        animal: inseminacao.animal.id,
        identificadorTouro: inseminacao.identificadorTouro,
      };
      this.nomeVet = inseminacao.veterinario.nome;
      this.brinco = inseminacao.animal.brinco
    },

    resetForm() {
      this.formData = {
        id: null,
        dataInseminacao: this.formData.dataInseminacao,
        veterinario: this.formData.veterinario,
        identificadorTouro: this.formData.identificadorTouro,
        animal: '',
      };
      this.brinco = '';
      this.modalTitle = 'Cadastro de Inseminação';
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
      if (this.modalTitle === 'Cadastro de Inseminação') {
        try {
          const response = await api.post(`http://127.0.0.1:8000/inseminacoes/`, this.formData, {});
          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarInseminacoesDaApi()
          } else {
            alert('Erro ao cadastrar inseminação. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }

      } else {
        try {
          const response = await api.patch(`http://127.0.0.1:8000/inseminacoes/${this.formData.id}/`, this.formData, {});
          if (response.status === 200) {
            alert('Alterações salvas com sucesso!');
            this.resetForm();
            this.buscarInseminacoesDaApi();
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

    confirmarExclusaoInsemincao(inseminacao) {
      this.inseminacaoParaExcluir = inseminacao;
    },

    async apagarInseminacaoPorData() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/inseminacoes/datas/${this.dataParaExclusao}/`, {
        });

        if (response.status === 204) {
          alert('Inseminação excluída com sucesso!');
          this.dataParaExclusao = null;
        } else {
          alert('Erro ao excluir inseminação. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.buscarInseminacoesDaApi();
      this.fecharModal('confirmacaoExclusaoModal');
    },

    async apagarInseminacao() {
      try {
        const response = await api.delete(`http://127.0.0.1:8000/inseminacoes/${this.inseminacaoParaExcluir.id}/`);

        if (response.status === 204) {
          alert('Inseminção excluído com sucesso!');
          this.detalhesInseminacao = this.detalhesInseminacao.filter(animal => animal.id !== this.inseminacaoParaExcluir.id);
          this.inseminacaoParaExcluir = null;
          this.buscarInseminacoesDaApi();
        } else {
          alert('Erro ao excluir a inseminação. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
      this.fecharModal('confirmacaoExclusaoAnimalModal');
    },

    async preencherListaFemeas() {
      const response = await api.get(`http://127.0.0.1:8000/animais/femeas/vivas`, {
        params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
      });
      this.listaFemeas = response.data;
    },

    filterFemeas() {
      this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.brinco));
    },

    selectMae(animal) {
      this.formData.animal = animal.id;
      this.brinco = animal.brinco;
      this.femeasFiltradas = [];
    },

    async preencherDatasInseminacoes(){
      const datasSet = new Set();
      this.inseminacoes.forEach(inseminacao => {
        datasSet.add(inseminacao.dataInseminacao);
      });
      this.datasInseminacoes = Array.from(datasSet).sort((b, a) => new Date(a) - new Date(b));
    },

    async preencherDetalhesInseminacaoPorData(data){
      this.detalhesInseminacao = []
      this.inseminacoes.forEach(inseminacao => {
        if(data === inseminacao.dataInseminacao){
          this.detalhesInseminacao.push(inseminacao);
        }
      });
      this.dataSelecionada = data;
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
      this.filtro.brinco = '';
      this.filtro.dataInseminacao = '';
      this.filtro.identificadorTouro = '';
    },
    toggleFormulario() {
      this.mostrarFormulario = !this.mostrarFormulario;
    },



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
  border-bottom: 2px solid #4CAF50;
  /* Adiciona uma borda verde na parte inferior */
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

.status-vivo {
  background-color: #d4edda;
  /* Verde claro para 'vivo' */
}

.status-morto {
  background-color: #f8d7da;
  /* Vermelho claro para 'morto' */
}

.status-doente {
  background-color: #fff3cd;
  /* Amarelo claro para 'doente' */
}
</style>
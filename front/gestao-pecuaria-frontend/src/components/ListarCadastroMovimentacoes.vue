  <template>
    <div class="background">
      <h2>Cadastro de Movimentações</h2>
      <div class="d-flex align-items-start table-container flex-column">
        <div class="d-flex align-items-start">
          <h2 class="me-3">Filtros</h2>
          <button class="btn-acoes btn-sm" @click="toggleFormulario"><i class="fas fa-chevron-down"></i></button>
        </div>
        <form class="row g-3 align-items-center" v-show="mostrarFormulario">
          <div class="col-auto d-flex align-items-center">
            <label for="animal" class="form-label me-2">Animal</label>
            <input type="text" class="form-control" id="animal" v-model="filtro.animal">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="produto" class="form-label me-2">Produto</label>
            <input type="text" class="form-control" id="produto" v-model="filtro.produto">
          </div>
          <div class="col-auto d-flex align-items-center">
            <label for="dataAplicacao" class="form-label me-2">Data</label>
            <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" placeholder="Data da aplicação"
              class="form-control" id="dataAplicacao" v-model="filtro.dataAplicacao" required>
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
              data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar Movimentações</button>
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col">Animal</th>
                <th scope="col">Piquete Origem</th>
                <th scope="col">Piquete Destino</th>
                <th scope="col">Data</th>
                <th scope="col">Motivo</th>
                <th scope="col">Ações</th>
              </tr>
            </thead>
            <tbody>




            </tbody>
          </table>
        </div>
        <!-- Modal de Cadastro de Movimentação -->
        <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Movimentações</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="submitForm">
                  <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                      placeholder="Data da movimentação" class="form-control" id="dataAplicacaoCadastro"
                      v-model="formData.dataAplicacao" required>
                  </div>

                  <div class="mb-3 input-group">
                    <input v-model="brinco" @input="filtrarAnimais" type="text" class="form-control"
                      placeholder="Digite o brinco...">
                  </div>
                  <div class="list-group" v-if="brinco && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimal(animal)">
                      {{ animal.brinco }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <input v-model="piqueteOrigem" @input="filtrarPiquetes" type="text" class="form-control"
                      placeholder="Digite o piquete de origem...">
                  </div>
                  <div class="list-group" v-if="piqueteOrigem && piquetesFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="piquete in piquetesFiltrados" :key="piquete.id" @click="selectPiqueteOrigem(piquete)">
                      {{ piquete.nome }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <input v-model="piqueteDestino" @input="filtrarPiquetes" type="text" class="form-control"
                      placeholder="Digite o piquete de destino...">
                  </div>
                  <div class="list-group" v-if="piqueteDestino && piquetesFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="piquete in piquetesFiltrados" :key="piquete.id" @click="selectPiqueteDestino(piquete)">
                      {{ piquete.nome }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="formData.motivo" type="text" class="form-control" id="motivo" placeholder="Motivo"
                      required>
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

        <!-- Modal de Visualização de Movimentações -->
        <div class="modal fade" id="visualizacaoModal" tabindex="-1" aria-labelledby="visualizacaoModalLabel"
          aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="visualizacaoModalLabel">Detalhes da Movimentação</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <p><strong>Data da Movimentação:</strong> {{ formatarData(this.dataSelecionada) }}</p>
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th scope="col">Animal</th>
                      <th scope="col">Piquete Origem</th>
                      <th scope="col">Piquete Destino</th>
                      <th scope="col">Motivo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="movimentacao in this.detalhesMovimentacao" :key="movimentacao.id">
                      <td>{{ movimentacao.animal.brinco }}</td>
                      <td>{{ movimentacao.piqueteOrigem.nome }}</td>
                      <td>{{ movimentacao.piqueteDestino.nome }}</td>
                      <td>{{ movimentacao.motivo }}</td>
                      <td>
                        <button @click="editarMovimentacao(movimentacao)" class="btn-acoes btn-sm" data-bs-toggle="modal"
                          data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
                        <button @click="confirmarExclusaoMovimentacao(movimentacao)" class="btn-acoes btn-sm"
                          data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoAnimalModal"><i
                            class="fas fa-trash-alt"></i></button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal de Edição de Movimentação -->
        <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="edicaoModalLabel">Edição de Movimentações</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="atualizarMovimentacao">
                  <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                      placeholder="Data da movimentação" class="form-control" id="dataMovimentacaoEdicao"
                      v-model="movimentacaoSelecionada.dataAplicacao" required>
                  </div>
                  <div class="mb-3 input-group">
                    <input v-model="brincoEdicao" @input="filtrarAnimais" type="text" class="form-control"
                      placeholder="Digite o brinco...">
                  </div>
                  <div class="list-group" v-if="brincoEdicao && animaisFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="animal in animaisFiltrados" :key="animal.id" @click="selectAnimalEdicao(animal)">
                      {{ animal.brinco }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <input v-model="piqueteOrigemEdicao" @input="filtrarPiquetes" type="text" class="form-control"
                      placeholder="Digite o piquete de origem...">
                  </div>
                  <div class="list-group" v-if="piqueteOrigemEdicao && piquetesFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="piquete in piquetesFiltrados" :key="piquete.id" @click="selectPiqueteOrigemEdicao(piquete)">
                      {{ piquete.nome }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <input v-model="piqueteDestinoEdicao" @input="filtrarPiquetes" type="text" class="form-control"
                      placeholder="Digite o piquete de destino...">
                  </div>
                  <div class="list-group" v-if="piqueteDestinoEdicao && piquetesFiltrados.length">
                    <button type="button" class="list-group-item list-group-item-action"
                      v-for="piquete in piquetesFiltrados" :key="piquete.id" @click="selectPiqueteDestinoEdicao(piquete)">
                      {{ piquete.nome }}
                    </button>
                  </div>
                  <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-tags"></i></span>
                    <input v-model="movimentacaoSelecionada.motivo" type="text" class="form-control" id="motivo"
                      placeholder="Motivo" required>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary" @click="atualizarMovimentacao">Atualizar</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal de Confirmação de Exclusão de Movimentação -->
        <div class="modal fade" id="confirmacaoExclusaoAnimalModal" tabindex="-1"
          aria-labelledby="confirmacaoExclusaoAnimalModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="confirmacaoExclusaoAnimalModalLabel">Confirmação de Exclusão</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                Tem certeza de que deseja excluir esta movimentação?
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-danger" @click="excluirMovimentacao">Excluir</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>





  <script>
  import axios from 'axios';
  import api from '/src/interceptadorAxios'

  export default {
    name: 'TelaAplicacoesProdutos',
    data() {
      return {
        animais: [],
        animaisFiltrados: [],
        brinco: '',
        movimentacoes: [],
        produtos: [],
        produtosFiltrados: [],
        nomeProduto: '',
        datasMovimentacoes: [],
        dataSelecionada: null,
        detalhesMovimentacao: [],
        movimentacaoParaExcluir: null,
        dataParaExclusao: null,
        camposHabilitadosAnimal: false,
        camposHabilitadosPiquete: false,
        piquetes: [],
        piquete: '',
        piqueteId: null,
        filteredPiquetes: [],
        radioEscolha: 'brinco',
        formData: {
          id: null,
          animal: '',
          piqueteOrigem: '',
          piqueteDestino: '',
          dataAplicacao: '',
          motivo: '',
        },
        mostrarFormulario: false,
        filtro: {
          animal: '',
          produto: '',
          dataAplicacao: '',
        },
        modalTitle: 'Cadastro de Movimentações',
      }
    },
    mounted() {
      this.buscarMovimentacoesDaApi();
      this.buscarAnimaisDaApi();
      this.buscarPiquetesDaApi();
    },
    methods: {

      async preencherDatasMovimentacao(){
        const datasSet = new Set();
        this.movimentacoes.forEach(movimentacao => {
          datasSet.add(movimentacao.dataAplicacao);
        });
        this.datasMovimentacoes = Array.from(datasSet).sort((b, a) => new Date(a) - new Date(b));
      },

      async preencherDetalhesMovimentacaoPorData(data){
        this.detalhesmovimentacao = []
        this.movimentacoes.forEach(movimentacao => {
          if(data === movimentacao.dataAplicacao){
            this.detalhesmovimentacao.push(movimentacao);
          }
        });
        this.dataSelecionada = data;
      },

      async buscarAplicacoesDaApi(){
          try {
              const response = await api.get('http://127.0.0.1:8000/movimentacoes/' , {
              params: {
                  propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
              },
              });
              this.movimentacoes = response.data;
              this.preencherDatasMovimentacao();
          } catch (error) {
          console.error('Erro ao buscar movimentacoes de produtos da API:', error);
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

      async buscarAnimaisDaApi() {
          try {
              const response = await api.get('http://127.0.0.1:8000/animais/vivos' , {
              params: {
                  propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
              },
              });
              this.animais = response.data;
          } catch (error) {
              console.error('Erro ao buscar animais da API:', error);
          }
      },


      async cadastrarMovimentacao() {
        try {
          const response = await axios.post('http://localhost:3000/movimentacoes', this.formData);
          if (response.status === 201) {
            this.fecharModal();
            this.resetForm();
            this.buscarMovimentacoes();
            alert('Movimentação cadastrada com sucesso!');
          } else {
            alert('Erro ao cadastrar movimentação.');
          }
        } catch (error) {
          console.error('Erro ao cadastrar movimentação:', error);
          alert('Erro ao cadastrar movimentação. Verifique o console para mais detalhes.');
        }
      },

      async editarMovimentacao() {
        try {
          const response = await axios.put(`http://localhost:3000/movimentacoes/${this.formData.id}`, this.formData);
          if (response.status === 200) {
            this.fecharModal();
            this.resetForm();
            this.buscarMovimentacoes();
            alert('Movimentação atualizada com sucesso!');
          } else {
            alert('Erro ao atualizar movimentação.');
          }
        } catch (error) {
          console.error('Erro ao atualizar movimentação:', error);
          alert('Erro ao atualizar movimentação. Verifique o console para mais detalhes.');
        }
      },

      async confirmarExclusaoMovimentacao(movimentacao) {
        this.movimentacaoSelecionada = movimentacao;
        this.showModal = true;
        this.modalTitle = 'Confirmação de Exclusão';
      },

      async excluirMovimentacao() {
        try {
          const response = await axios.delete(`http://localhost:3000/movimentacoes/${this.movimentacaoSelecionada.id}`);
          if (response.status === 200) {
            this.fecharModal();
            this.buscarMovimentacoes();
            alert('Movimentação excluída com sucesso!');
          } else {
            alert('Erro ao excluir movimentação.');
          }
        } catch (error) {
          console.error('Erro ao excluir movimentação:', error);
          alert('Erro ao excluir movimentação. Verifique o console para mais detalhes.');
        }
      },

      resetForm() {
        this.formData = {
          id: null,
          animalId: null,
          produtoId: null,
          data: '',
          tipoMovimentacao: '',
          detalhes: '',
        };
      },

      fecharModal() {
        this.showModal = false;
        this.modalTitle = '';
      },

      formatarData(data) {
        const date = new Date(data);
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        return date.toLocaleDateString('pt-BR', options);
      },
    },
  };
  </script>
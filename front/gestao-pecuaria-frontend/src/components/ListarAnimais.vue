<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar</button>
    </div>
    <h2>Lista de Animais</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Brinco</th>
            <th scope="col">Data Nascimento</th>
            <th scope="col">Sexo</th>
            <th scope="col">Raça</th>
            <th scope="col">Brinco Pai</th>
            <th scope="col">Brinco Mãe</th>
            <th scope="col">Observações</th>
            <th scope="col">Lote</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(animal, index) in animais" :key="index">
            <td>{{ animal.brinco }}</td>
            <td>{{ animal.dataNascimento }}</td>
            <td>{{ animal.sexo }}</td>
            <td>{{ animal.racaPredominante }}</td>
            <td>{{ animal.brincoPai }}</td>
            <td>{{ animal.brincoMae }}</td>
            <td>{{ animal.racaObservacao }}</td>
            <td>{{ animal.lote }}</td>
            <td>
              <button @click="editarAnimal(animal)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button @click="confirmarExclusao(animal)" class="btn btn-danger btn-sm" data-bs-toggle="modal"
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
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de animal</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3 input-group">
              <span class="input-group-text"><i class="fas fa-tag"></i></span>
              <select v-model="formData.lote" class="form-select" id="lote" aria-label="Lote"
                placeholder="Selecione o lote" required>
                <option disabled selected>Selecione o lote</option>
                <option v-for="lote in lotes" :key="lote.id" :value="lote.id">{{ lote.nome }}</option>
              </select>
            </div>
            <hr>
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="formData.brinco" type="text" class="form-control" id="brinco"
                  placeholder="Número do Brinco" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                <input v-model="formData.dataNascimento" type="date" class="form-control" id="dataNascimento"
                  placeholder="Data de Nascimento" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus-mars"></i></span>
                <select v-model="formData.sexo" class="form-select" id="sexo" aria-label="Sexo" required
                  placeholder="Selecione o sexo">
                  <option disabled selected>Selecione o sexo</option>
                  <option value="macho">Macho</option>
                  <option value="femea">Fêmea</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-horse"></i></span>
                <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante"
                  aria-label="Raça Predominante" required>
                  <option disabled selected>Selecione a raça predominante</option>
                  <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacao"
                  placeholder="Observações sobre a Raça"></textarea>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                <input v-model="formData.brincoPai" type="text" class="form-control" id="brincoPai"
                  placeholder="Número do Brinco do Pai">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                <input v-model="formData.brincoMae" type="text" class="form-control" id="brincoMae"
                  placeholder="Número do Brinco da Mãe">
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

    <!-- Modal de Edição -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar animal</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                <input v-model="formData.brinco" type="text" class="form-control" id="brincoEditar"
                  placeholder="Número do Brinco" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                <input v-model="formData.dataNascimento" type="date" class="form-control" id="dataNascimentoEditar"
                  placeholder="Data de Nascimento" required>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-venus-mars"></i></span>
                <select v-model="formData.sexo" class="form-select" id="sexoEditar">
                  <option disabled value="">Selecione o sexo</option>
                  <option v-for="opcao in ['macho', 'femea']" :key="opcao" :value="opcao"
                    v-bind:selected="formData.sexo === opcao">{{ opcao }}</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-horse"></i></span>
                <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante"
                  aria-label="Raça Predominante" required>
                  <option selected>{{ formData.racaPredominante }}</option>
                  <option v-for="raca in racas" :key="raca.nome" :value="raca.nome">{{ raca.nome }}</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacaoEditar"
                  placeholder="Observações sobre a Raça"></textarea>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                <select v-model="formData.lote" class="form-select" id="lote" aria-label="Lote" required>
                  <option disabled selected>Selecione o lote</option>
                  <option v-for="lote in lotes" :key="lote.id" :value="lote.id">{{ lote.nome }}</option>
                </select>
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                <input v-model="formData.brincoPai" type="text" class="form-control" id="brincoPaiEditar"
                  placeholder="Número do Brinco do Pai">
              </div>
              <div class="mb-3 input-group">
                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                <input v-model="formData.brincoMae" type="text" class="form-control" id="brincoMaeEditar"
                  placeholder="Número do Brinco da Mãe">
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
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  name: 'TelaAnimais',
  data() {
    return {
      animais: [],
      racas: [],
      lotes: [],
      formData: {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: '',
        racaObservacao: '',
        lote: '',
        brincoPai: '',
        brincoMae: ''
      },
      modalTitle: 'Cadastro de Animal',
    }
  },
  async mounted() {
    this.buscarAnimaisDaApi();
    this.buscarRacasDaApi();
    this.buscarLotesDaApi();
  },

  methods: {
    async buscarLotesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/lotes/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.lotes = response.data;
      } catch (error) {
        console.error('Erro ao buscar lotes da API:', error);
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
        racaPredominante: animal.racaPredominante,
        racaObservacao: animal.racaObservacao,
        lote: animal.lote
      };
    },

    resetForm() {
      this.formData = {
        id: null,
        brinco: '',
        dataNascimento: '',
        sexo: '',
        racaPredominante: '',
        racaObservacao: '',
        lote: this.formData.lote
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
      // Verifica se os animais pai e mãe existem no banco de dados
      const paiExists = await this.checkAnimalExists(this.formData.brincoPai);
      const maeExists = await this.checkAnimalExists(this.formData.brincoMae);

      // Verifica se o animal pai é do sexo masculino e a mãe é do sexo feminino
      const paiIsMale = await this.checkAnimalSex(this.formData.brincoPai, 'macho');
      const maeIsFemale = await this.checkAnimalSex(this.formData.brincoMae, 'femea');

      if (!paiExists || !maeExists) {
        const confirmCadastro = confirm('Atenção: Um ou ambos dos pais não estão cadastrados. Deseja continuar?');
        if (!confirmCadastro) return; // Cancela o cadastro
      }

      if (!paiIsMale || !maeIsFemale) {
        alert('O animal pai deve ser do sexo masculino e a mãe do sexo feminino.');
        return; // Cancela o cadastro
      }
      if (this.modalTitle === 'Cadastro de Animal') {
        try {
          const response = await api.post(`http://127.0.0.1:8000/animais/`, this.formData, {
          });

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
            this.resetForm();
            this.buscarAnimaisDaApi();
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
          } else {
            alert('Erro ao salvar alterações. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
        this.fecharModal("edicaoModal");
      }
    },
    async checkAnimalExists(brinco) {
      // Verificar se o brinco já existe na lista de animais
      return this.animais.some(animal => animal.brinco === brinco);
    },

    async checkAnimalSex(brinco, expectedSex) {
      // Encontrar o animal na lista de animais pelo brinco e verificar o sexo
      const animal = this.animais.find(animal => animal.brinco === brinco);
      if (animal) {
        return animal.sexo === expectedSex;
      } else {
        // Se o animal não for encontrado, retornar false
        return false;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.table-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>

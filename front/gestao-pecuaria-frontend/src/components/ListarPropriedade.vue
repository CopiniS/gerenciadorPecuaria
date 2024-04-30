<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <button @click="resetForm()" type="button" class="btn btn-primary" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Cadastrar</button>
    </div>
    <h2>Lista de Propriedades</h2>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Endereço</th>
            <th scope="col">Estado</th>
            <th scope="col">Cidade</th>
            <th scope="col">Latitude</th>
            <th scope="col">Longitude</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(propriedade, index) in propriedades" :key="index">
            <td>{{ propriedade.nome }}</td>
            <td>{{ propriedade.endereco }}</td>
            <td>{{ propriedade.estado }}</td>
            <td>{{ propriedade.cidade }}</td>
            <td>{{ propriedade.latitude }}</td>
            <td>{{ propriedade.longitude }}</td>
            <td>
              <button @click="editarPropriedade(propriedade)" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo"><i class="fas fa-edit"></i></button>
              <button class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoModal"><i
                  class="fas fa-trash-alt"></i></button>

            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <!-- Modal de Cadastro-->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Propriedade</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="nome" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nome">
              </div>
              <div class="mb-3">
                <label for="endereco" class="col-form-label">Endereço:</label>
                <input v-model="formData.endereco" type="text" class="form-control" id="endereco">
              </div>
              <div class="mb-3">
                <label for="estado" class="col-form-label">Estado:</label>
                <select v-model="formData.estado" class="form-select" id="estado" required @change="buscarCidadesPorEstado($event.target.value)">
                  <option value="" disabled selected>Selecione o estado</option>
                  <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="cidade" class="col-form-label">Cidade:</label>
                <select v-model="formData.cidade" class="form-select" id="cidade" required>
                  <option value="" disabled selected>Selecione a cidade</option>
                  <option v-for="cidade in cidades" :key="cidade.id" :value="cidade.nome">{{ cidade.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="latitude" class="col-form-label">Latitude:</label>
                <input v-model="formData.latitude" type="text" class="form-control" id="latitude">
              </div>
              <div class="mb-3">
                <label for="longitude" class="col-form-label">Longitude:</label>
                <input v-model="formData.longitude" type="text" class="form-control" id="longitude">
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
            <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar Propriedade</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="nomeEditar" class="col-form-label">Nome:</label>
                <input v-model="formData.nome" type="text" class="form-control" id="nomeEditar">
              </div>
              <div class="mb-3">
                <label for="enderecoEditar" class="col-form-label">Endereço:</label>
                <input v-model="formData.endereco" type="text" class="form-control" id="enderecoEditar">
              </div>
              <div class="mb-3">
                <label for="estadoEditar" class="col-form-label">Estado:</label>
                <select v-model="formData.estado" class="form-select" id="estadoEditar" required
                  @change="buscarCidadesPorEstado($event.target.value)">
                  <option value="" disabled>Selecione o estado</option>
                  <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="cidadeEditar" class="col-form-label">Cidade:</label>
                <select v-model="formData.cidade" class="form-select" id="cidadeEditar" required>
                  <option value="" disabled>Selecione a cidade</option>
                  <option v-for="cidade in cidades" :key="cidade.id" :value="cidade.nome">{{ cidade.nome }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="latitudeEditar" class="col-form-label">Latitude:</label>
                <input v-model="formData.latitude" type="text" class="form-control" id="latitudeEditar">
              </div>
              <div class="mb-3">
                <label for="longitudeEditar" class="col-form-label">Longitude:</label>
                <input v-model="formData.longitude" type="text" class="form-control" id="longitudeEditar">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitFormEdicao">Salvar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza de que deseja excluir esta propriedade?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="apagarPropriedade(propriedade)">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'ListarPropriedade',
  data() {
    return {
      propriedades: [],
      cidades: [],
      estados: [],
      formData: {
        id: null,
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
        produtor: []
      }
    }
    
  },
  mounted() {
    this.buscarPropriedadesDaApi();
    this.buscarEstadosDaApi();
  },
  methods: {

    async buscarCidadesPorEstado(estadoId) {
      try {
        const response = await axios.get(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`);
        this.cidades = response.data;
      } catch (error) {
        console.error('Erro ao buscar cidades da API:', error);
      }
      this.encontrarNomeDoEstadoPeloId(estadoId)
    },

    async encontrarNomeDoEstadoPeloId(estadoId) {
      let estadoSelecionado;
      console.log('tamanho da lista de estados: ', this.estados.length);
      console.log('id do estado: ', estadoId);
      for (let i = 0; i < this.estados.length; i++) {
        console.log('lista de ids dos estados' , this.estados[i].id , '  nome: ' , this.estados[i].nome);
        if (this.estados[i].id == estadoId) {
          estadoSelecionado = this.estados[i];
          break;
        }
      }
      if (estadoSelecionado) {
        this.formData.estado = estadoSelecionado.nome;
      } else {
        console.error('Estado não encontrado.');
        // Defina um valor padrão ou trate o erro conforme necessário
      }
    },

    async buscarEstadosDaApi() {
      try {
        const response = await axios.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome');
        this.estados = response.data;
      } catch (error) {
        console.error('Erro ao buscar cidades da API:', error);
      }
    },

    async buscarPropriedadesDaApi() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/propriedades/');
        this.propriedades = response.data;
      } catch (error) {
        console.error('Erro ao buscar propriedades da API:', error);
      }
    },
    async editarPropriedade(propriedade) {
      this.formData = {
        id: propriedade.id,
        nome: propriedade.nome,
        endereco: propriedade.endereco,
        estado: propriedade.estado,
        cidade: propriedade.cidade,
        latitude: propriedade.latitude,
        longitude: propriedade.longitude,
      };
    },

    resetForm() {
      this.formData = {
        id: '',
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
      };
    },
    async apagarPropriedade(propriedade) {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/propriedades/${propriedade.id}/`);
        if (response.status === 204) {
          alert('Propriedade apagada com sucesso!');
          this.buscarPropriedadesDaApi();
        } else {
          alert('Erro ao apagar propriedade. Tente novamente mais tarde.');
        }

      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },

    async submitFormEdicao() {
      try {
        const response = await axios.put(`http://127.0.0.1:8000/propriedades/${this.formData.id}/`, this.formData);

        if (response.status === 200) {
          alert('Alterações salvas com sucesso!');
          this.buscarPropriedadesDaApi();
        } else {
          alert('Erro ao salvar alterações. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    async submitForm() {
      try {
        const dadosPropriedade = {
          nome: this.formData.nome,
          endereco: this.formData.endereco,
          estado: this.formData.estado,
          cidade: this.formData.cidade,
          latitude: parseFloat(this.formData.latitude),
          longitude: parseFloat(this.formData.longitude),
          produtor: 0
        }
        const response = await axios.post(`http://127.0.0.1:8000/propriedades/`, dadosPropriedade);

        if (response.status === 201) {
          alert('Cadastro realizado com sucesso!');
          this.resetForm();
          this.buscarPropriedadesDaApi();
        } else {
          alert('Erro ao cadastrar propriedade. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    }
  }
};
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.table-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>

<template>
  <div>
    <h2>Edição de Propriedade</h2>
    <div class="form-container">
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
      <div class="d-flex justify-content-between align-items-center">
        <button @click="trocarPropriedade" type="button" class="btn btn-secondary">Trocar Propriedade</button>
        <button @click="apagarPropriedade" type="button" class="btn btn-danger">Excluir Propriedade</button>
        <button type="submit" class="btn btn-primary">Salvar Alterações</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  name: 'EditarPropriedade',
  data() {
    return {
      cidades: [],
      estados: [],
      propriedade: null,
      formData: {
        id: null,
        nome: '',
        endereco: '',
        estado: '',
        cidade: '',
        latitude: '',
        longitude: '',
      }
    }
  },
  mounted() {
    const propriedadeSelecionada = localStorage.getItem('propriedadeSelecionada');
    if (propriedadeSelecionada) {
      this.buscarPropriedadeDaApi(propriedadeSelecionada);
    }
  },
  methods: {
    async buscarPropriedadeDaApi(propriedadeId) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/propriedades/${propriedadeId}/`);
        this.propriedade = response.data;
        this.formData = {
          id: this.propriedade.id,
          nome: this.propriedade.nome,
          endereco: this.propriedade.endereco,
          estado: this.propriedade.estado,
          cidade: this.propriedade.cidade,
          latitude: this.propriedade.latitude,
          longitude: this.propriedade.longitude,
        };
      } catch (error) {
        console.error('Erro ao buscar propriedade da API:', error);
      }
    },

    async apagarPropriedade() {
      if (!this.propriedade) return;
      try {
        const response = await api.delete(`http://127.0.0.1:8000/propriedades/${this.propriedade.id}/`);
        if (response.status === 204) {
          alert('Propriedade apagada com sucesso!');
          localStorage.removeItem('propriedadeSelecionada');
          this.$router.push('/propriedades');
        } else {
          alert('Erro ao apagar propriedade. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },

    trocarPropriedade() {
      // Redirecionar para a página onde o usuário pode selecionar outra propriedade
      this.$router.push('/propriedades');
    },
  }
};
</script>

<style>
.form-container {
  margin-left: 20px;
  margin-right: 20px;
}
</style>

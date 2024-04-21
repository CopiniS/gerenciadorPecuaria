<template>
  <div class="form-container">
    <form id="formPropriedade">
      <div class="row">
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="nomePropriedade" class="form-label me-2">Nome:</label>
            <input type="text" class="form-control" id="nomePropriedade" placeholder="Nome" required>
          </div>
        </div>
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="produtor" class="form-label me-2">Produtor:</label>
            <select class="form-select" id="produtor" required>
              <option value="" disabled selected>Selecione um produtor</option>
            <option v-for="produtor in produtores" :key="produtor.id" :value="produtor.id">{{ produtor.nome }}</option>
            </select>
          </div>
        </div>
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="endereco" class="form-label me-2">Endereço:</label>
            <input type="text" class="form-control" id="endereco" placeholder="Endereço" required>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="cidade" class="form-label me-2">Cidade:</label>
            <input type="text" class="form-control" id="cidade" placeholder="Cidade" required>
          </div>
        </div>
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="estado" class="form-label me-2">Estado:</label>
            <select class="form-select" id="estado" required>
              <option value="" disabled selected>Selecione o estado</option>
            <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
            </select>
          </div>
        </div>
        <div class="col-md-2">
          <div class="mb-3 d-flex align-items-center">
            <label for="latitude" class="form-label me-2">Latitude:</label>
            <input type="text" class="form-control" id="latitude" placeholder="Latitude" required>
          </div>
        </div>
        <div class="col-md-2">
          <div class="mb-3 d-flex align-items-center">
            <label for="longitude" class="form-label me-2">Longitude:</label>
            <input type="text" class="form-control" id="longitude" placeholder="Longitude" required>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Cadastrar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CadastroPropriedade',

  data() {
    return {
      estados: [],
      produtores: [],
    };
  },

  mounted() {
    this.getEstados();
    this.getProdutores();
    this.setupFormSubmitListener();
  },

  methods: {
    async getEstados() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/estado/');
        this.estados = response.data;
      } catch (error) {
        console.error('Erro ao buscar estados:', error);
        alert('Erro ao buscar estados. Verifique o console para mais detalhes.');
      }
    },
    async getProdutores() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/produtores/');
        this.produtores = response.data;
      } catch (error) {
        console.error('Erro ao buscar produtores:', error);
        alert('Erro ao buscar produtores. Verifique o console para mais detalhes.');
      }
    },
    async setupFormSubmitListener() {
      document.getElementById('formPropriedade').addEventListener('submit', async (event) => {
        event.preventDefault();

        const dadosPropriedade = {
          nome: document.getElementById('nomePropriedade').value,
          endereco: document.getElementById('enderecoPropriedade').value,
          produtor: document.getElementById('produtor').value,
          estado: document.getElementById('estadoCidade').value,
          cidade: document.getElementById('cidade').value,
          latitude: document.getElementById('latitude').value,
          longitude: document.getElementById('longitude').value,
        };

        try {
          const response = await axios.post('http://127.0.0.1:8000/propriedades/', dadosPropriedade);

          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
          } else {
            alert('Erro ao cadastrar propriedade. Tente novamente mais tarde.');
          }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      });
    },
  },
};
</script>


<style scoped>
.form-container {
  display: flex;
  justify-content: center; 
  height: 35vh; 
  margin-top: 0px;
  margin-bottom: 10px;
}

#formPropriedade {
  width: 100%; 
  max-width: 1500px; 
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
  background-color: white; 
}
</style>

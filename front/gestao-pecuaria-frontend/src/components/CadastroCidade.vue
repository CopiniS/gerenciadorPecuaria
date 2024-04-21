<template>
  <div class="form-container">
    <form id="formCidade">
      <div class="row justify-content-center"> 
        <div class="col-md-8"> 
          <div class="mb-3 row">
            <label for="nomeCidade" class="col-sm-3 col-form-label">Nome</label> 
            <div class="col-sm-9">
              <input type="text" class="form-control" id="nomeCidade" placeholder="Digite o nome da cidade" required>
            </div>
          </div>
          <div class="mb-3 row">
            <label for="estadoCidade" class="col-sm-3 col-form-label">Estado</label> 
            <div class="col-sm-9">
              <select class="form-select" id="estadoCidade" required>
                <option value="" disabled selected>Selecione o estado</option>
                <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome }}</option>
              </select>
            </div>
          </div>
          <div class="text-center"> <!-- Centraliza o botão -->
            <button type="submit" class="btn btn-primary">Cadastrar</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

  
  <script>
import axios from 'axios';

export default {
  name: 'CadastroCidade',
  data() {
    return {
      estados: []
    };
  },
  mounted() {
    this.getEstados();
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
    setupFormSubmitListener() {
      document.getElementById('formCidade').addEventListener('submit', async (event) => {
        event.preventDefault();

        const dadosCidade = {
          nome: document.getElementById('nomeCidade').value,
          estado: document.getElementById('estadoCidade').value,
        };

        try {
          const response = await axios.post('http://127.0.0.1:8000/cidades/', dadosCidade);

          if (response.status === 201) {
            alert('Cadastro de cidade realizado com sucesso!');
          } else {
            alert('Erro ao cadastrar cidade. Tente novamente mais tarde.');
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
    height: 30vh; 
    margin-top: 0px;
    margin-bottom: 10px;
  }
  
  #formCidade {
    width: 100%; 
    max-width: 1500px; 
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
    background-color: white; 
  }
  </style>
  
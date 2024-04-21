<template>
  <div class="form-container">
    <form id="animalForm">
      <div class="row">
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="brinco" class="form-label me-2">Brinco:</label>
            <input type="text" class="form-control" id="brinco" placeholder="Digite o brinco do animal" required>
          </div>
        </div>
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="dataNascimento" class="form-label me-2">Data de Nascimento:</label>
            <input type="date" class="form-control" id="dataNascimento" required>
          </div>
        </div>
        <div class="col-md-4">
          <div class="mb-3 d-flex align-items-center">
            <label for="sexo" class="form-label me-2">Sexo:</label>
            <select class="form-select" id="sexo" required>
              <option value="M">Macho</option>
              <option value="F">Fêmea</option>
            </select>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="mb-3 d-flex align-items-center">
            <label for="racaPredominante" class="form-label me-2">Raça Predominante:</label>
            <input type="text" class="form-control" id="racaPredominante" placeholder="Digite a raça predominante" required>
          </div>
        </div>
        <div class="col-md-6">
          <div class="mb-3 d-flex align-items-center">
            <label for="racaObservacao" class="form-label me-2">Observação da Raça:</label>
            <input type="text" class="form-control" id="racaObservacao" placeholder="Observações sobre a raça">
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
  name: 'CadastroAnimal',

  mounted() {
    this.setupFormSubmitListener();
  },

  methods: {
    async setupFormSubmitListener() {
      document.getElementById('animalForm').addEventListener('submit', async (event) => {
        event.preventDefault();

        const dadosAnimal = {
          brinco: document.getElementById('brinco').value,
          dataNascimento: document.getElementById('dataNascimento').value,
          sexo: document.getElementById('sexo').value,
          racaPredominante: document.getElementById('racaPredominante').value,
          racaObservacao: document.getElementById('racaObservacao').value,
        };

        try {
          const response = await axios.post('http://127.0.0.1:8000/animais/', dadosAnimal);

          console.log(response)
          if (response.status === 201) {
            alert('Cadastro realizado com sucesso!');
          } else {
            alert('Erro ao cadastrar animal. Tente novamente mais tarde.');
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

#animalForm {
  width: 100%; 
  max-width: 1500px; 
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
  background-color: white; 
}
</style>

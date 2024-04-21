<template>
    <div class="form-container">
      <form id="formRaca">
        <div class="mb-3">
          <label for="nomeRaca" class="form-label">Nome</label>
          <input type="text" class="form-control" id="nomeRaca" placeholder="Digite o nome da raça" required>
        </div>
        <button type="submit" class="btn btn-primary">Cadastrar</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CadastroRaca',
  
    mounted() {
      this.setupFormSubmitListener();
    },
  
    methods: {
      setupFormSubmitListener() {
        document.getElementById('formRaca').addEventListener('submit', async (event) => {
          event.preventDefault();
  
          const dadosRaca = {
            nome: document.getElementById('nomeRaca').value,
          };
  
          try {
            const response = await axios.post('http://127.0.0.1:8000/racas/', dadosRaca);
  
            if (response.status === 201) {
              alert('Cadastro de raça realizado com sucesso!');
            } else {
              alert('Erro ao cadastrar raça. Tente novamente mais tarde.');
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
  
  #formRaca {
    width: 100%; 
    max-width: 1500px; 
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
    background-color: white;  
  }
  </style>
  
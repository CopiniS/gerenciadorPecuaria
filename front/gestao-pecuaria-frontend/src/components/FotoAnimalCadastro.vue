<template>
    <div class="background">
    <LoadSpinner :isLoading="loadingSubmit || loadingInicial" />
      <nav>
        <div class="nav nav-tabs" id="nav-tab" role="tablist">
          <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
          @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais"
          aria-selected="true">Lista de Animais</button>
          <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-visualizacao-tab"
            @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-visualizacao" 
            aria-selected="true">Visualização do Animal</button>
          <button class="nav-link" :class="{ active: activeTab === 'cadastro' }" id="nav-cadastro-tab" @click="selectTab('cadastro')" 
          type="button" role="tab" aria-controls="nav-cadastro" aria-selected="false">Cadastro de Foto</button>
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacoes' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
        </div>
        <div class="tab-pane fade show active" id="nav-cadastro" role="tabpanel" aria-labelledby="nav-cadastro-tab">
          <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
            <h1 class="title fs-5" id="cadastroLabel">Cadastro de Foto</h1>
            <h2 class="title fs-5" id="cadastroLabel">Animal: {{ brinco }}</h2>
  
              <form @submit.prevent="submitForm" class="form-foto">
                  <div class="mb-3 input-group mb-3-foto">
                      <span class="input-group-text" title="Data da Foto"><i class="fas fa-calendar-alt"></i></span>
                      <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                          :placeholder="dataPlaceholder" class="form-control" id="dataFoto" autocomplete="off"
                          v-model="formData.dataFoto" :class="{ 'is-invalid': !isDataValida }" title="Data da Foto">
                  </div>
                  <div class="mb-3 input-group mb-3-foto">
                      <span class="input-group-text" title="Observações da Foto"><i class="fas fa-sticky-note"></i></span>
                      <input v-model="formData.observacao" class="form-control" type="text" id="observacao"
                          placeholder="Observação" title="Observações da Foto" autocomplete="off" />
                  </div>
                  <div class="mb-3 input-group mb-3-foto justify-content-center">
                      <div class="boxSelect">
                          <input type="file" id="fileInput" @change="apresentarImagem" accept="image/*" />
                          <label for="fileInput" class="upload-label" v-if="!resizedImage">
                              Adicionar Foto
                          </label>
                          <img v-if="resizedImage" :src="resizedImage" alt="Resized Image" />
                      </div>
                  </div> 
                  <div class="button-group justify-content-end">
                      <button type="button" class="btn btn-secondary" @click="selectTab('visualizacao')">Cancelar</button>
                      <button type="submit" class="btn btn-success">Enviar</button>
                  </div>
              </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '/src/interceptadorAxios';
  import LoadSpinner from './LoadSpiner.vue';

  
  export default {

      components: {
          LoadSpinner,
      },

      data() {
          return {
          activeTab: 'cadastro',  // Aba inicial é 'cadastro'
          contadorObservacoes: 0,
          brinco: null,
          resizedImage: null,
          loadingSubmit: false,
          loadingInicial: true,
          formData: {
              id: null,
              foto: null,
              dataFoto: '',
              observacao: '',
              animal: null,
          },
          isFotoValida: true,
          isDataValida: true,
          fotoPlaceholder: 'Foto do animal*',
          dataPlaceholder: 'Data da Foto*',
          };
      },
  
      mounted(){
          const animalId = this.$route.params.animalId;
          if (animalId) {
          this.fetchAnimal(animalId);
          }
      },
  
      methods: {
  //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
      async fetchAnimal(animalId) {
        try {
          const response = await api.get(`http://127.0.0.1:8000/animais/animal/${animalId}/`);
          const animal = response.data;
          this.formData.animal = animal[0].id;
          this.brinco = animal[0].brinco;
          this.loadingInicial = false;
          
        } catch (error) {
          console.error('Erro ao buscar animal da API:', error);
        }
      },
      
      async submitForm() {
        if (this.verificaVazio()) {
            this.loadingSubmit = true;
          try {
              const response = await api.post('http://127.0.0.1:8000/fotos-animais/', this.formData , {
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
          });
              if (response.status === 201) {
                  this.loadingSubmit = false;
                  setTimeout(() => {
                    alert('Cadastro realizado com sucesso!');
                    this.selectTab('visualizacao');
                  }, 100)
              } else {
                    this.loadingSubmit = false;
                    alert('Erro ao cadastrar aplicacao. Tente novamente mais tarde.');
              }
          } catch (error) {
            this.loadingSubmit = false;
            console.error('Erro ao enviar requisição:', error);
            alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
          }
        } 
      },
  
  
  //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------
      verificaVazio(){
          //DATA DA FOTO
          if(this.formData.dataFoto != null){
              if(this.formData.dataFoto.trim() != ''){
              this.isDataValida = true;
              this.dataPlaceholder = 'Data da Foto';
              }
              else{
              this.isDataValida = false;
              this.dataPlaceholder = 'Data da Foto é um Campo Obrigatório';
              }
          }
          else{
              this.isDataValida = false;
              this.dataPlaceholder = 'Data da Foto é um Campo Obrigatório';
          }
  
          //FOTO
          if(this.formData.foto != null){
              this.isFotoValida = true;
              this.fotoPlaceholder = 'Foto do Animal';
              }
          else{
              this.isFotoValida = false;
              this.fotoPlaceholder = 'Foto do Animal é um Campo Obrigatório';
          }
  
          //OBSERVAÇÃo
          if(this.formData.observacao != null && this.formData.observacao.trim() == ''){
              this.formData.observacao = null;
          }
  
          return (
              this.isDataValida &&
              this.isFotoValida
          );
          },
  
  
  //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
      selectTab(tab) {
        this.activeTab = tab;
        if (tab === 'animais') {
          this.$router.push('/animais');
        }
        else if(tab==='visualizacao'){
          this.$router.push({
              name: 'VizualizarAnimal', 
              params: { animalId: this.formData.animal } 
          })
        }
      },
  
      apresentarImagem(event) {
          const file = event.target.files[0];
          if (file) {
              this.formData.foto = file;
  
              const reader = new FileReader();
              reader.onload = (e) => {
                  this.resizedImage = e.target.result;
              };
              reader.readAsDataURL(file);
          }
      },
    },
  };
  </script>
  
  <style scoped>
  .background {
      background-color: #ededef;
      /* Um tom mais escuro que o branco */
      min-height: 100vh;
      /* Garante que o fundo cubra toda a altura da tela */
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
  
  .table-container table thead tr th {
      border-bottom: 2px solid #4CAF50;
      /* Adiciona uma borda verde na parte inferior */
      background-color: #f0f0f0;
  }
  
  .animal-view {
      padding: 20px;
  }
  
  .actions {
      margin-top: 20px;
      margin-bottom: 20px;
  }
  
  .actions button {
      margin-right: 10px;
      margin-top: 5px;
      margin-bottom: 5px;
  }
  
  .actions .btn {
      width: 200px;
  }
  
  table {
      width: 100%;
      border-collapse: collapse;
  }
  
  th,
  td {
      border: 1px solid #ddd;
      padding: 8px;
  }
  
  th {
      background-color: #f2f2f2;
  }
  
  .boxSelect {
      width: 90%;
      max-width: 900px;
      height: 500px;
      border: 2px dashed #ccc;
      border-radius: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f8f8f8;
      position: relative;
  }
  
  .boxSelect img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 20px;
  }
  
  .upload-label {
      position: absolute;
      color: #4CAF50;
      font-size: 18px;
      cursor: pointer;
      text-align: center;
  }
  
  .upload-label:hover {
      text-decoration: underline;
  }
  
  input[type="file"] {
      display: none;
  }
  
  .modal-body-cadastro {
      justify-content: center;
      margin-top: 20px;
  }
  
  .modal-body-visu {
      display: flex;
      justify-content: center;
  }
  
  .content {
      width: 100%;
      background-color: #4CAF50;
  }
  
  .content img {
      width: 100%;
      height: 500px;
      object-fit: cover;
      border-radius: 20px;
  }
  
  h2 {
      display: block;
      font-size: 20px;
  }
  
  .mb-3-foto {
      width: 90%;
  }
  
  .form-foto {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
  }
  
  .input-imagem {
      display: flex;
      justify-content: center;
      margin-bottom: 0;
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
  
  .nav-link.active {
      background-color: #d0d0d0 !important;
      /* Cor um pouco mais escura quando a aba está ativa */
  }
  </style>
  
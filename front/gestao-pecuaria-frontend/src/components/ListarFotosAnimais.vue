<template>
  <div>
    <button type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#cadastroModal" data-bs-whatever="@mdo">cadastro foto</button>
    <button type="button" class="btn btn-success" data-bs-toggle="modal"
        data-bs-target="#visuModal" data-bs-whatever="@mdo">visu foto</button>
    
    <!-- Modal de Cadastro de foto -->
    <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Fotos</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body-cadastro">
            <form>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                    <input v-model="formData.dataFoto" type="date" class="form-control" id="dataFoto" required>
                </div>
                <div class="mb-3 input-group">
                    <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                    <textarea v-model="formData.observacao" class="form-control" id="observacao" placeholder="Observação"></textarea>
                </div>
                <div class="mb-3 input-group">
                  <input type="file" @change="apresentarImagem" accept="image/*" />
                </div>
            </form>
            <div class="input-imagem">
                <div class="boxSelect">
                  <img v-if="resizedImage" :src="resizedImage" alt="Resized Image" />
                </div>
            </div>
          </div>
          <div class="modal-footer">
            <button v-if="resizedImage" @click="salvarImagem" class="btn btn-primary">Salvar Imagem</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Visualização de foto -->
    <div class="modal fade" id="visuModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="cadastroModalLabel">Animal: yyyy</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body-visu">
              <div class="slide">
                <div class="slider">
                  <div class="content" v-for="(foto, index) in fotos" :key="index">
                    <h2>{{ foto.dataFoto }}</h2>
                    <img :src="getImagePath(foto.foto)">
                    <h2>Observação:</h2>
                    <p>{{ foto.observacao }}</p>
                  </div>
                </div>
                  <button id="voltaSlide" @click="controlaSlide('voltaSlide')">&#9664;</button>
                  <button id="passaSlide" @click="controlaSlide('passaSlide')">&#9654;</button>
              </div>
          </div>
          <div class="modal-footer">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  data() {
    return {
      slider: null,
      width: 0,
      resizedImage: null,
      fotos: [],
      formData: {
        id: null,
        foto: null,
        dataFoto: '',
        observacao: '',
        animal: 2,
      }
    };
  },

  mounted() {
    this.slider = document.querySelector('.slider');
    this.width = window.getComputedStyle(this.slider).width;
    this.buscarFotos();
  },

  methods: {
    
    controlaSlide(id){
      switch (id) {
        case 'voltaSlide':
          return this.slider.scrollLeft -= parseInt(this.width);

        case 'passaSlide':
          return this.slider.scrollLeft += parseInt(this.width);

        default:
          break;
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

    async buscarFotos(){
        try {
            const response = await api.get('http://127.0.0.1:8000/fotos-animais/', {
            params: {
                animalSelecionado: this.formData.animal
            },
            });
            this.fotos = response.data;
            this.fotos = this.fotos.sort((a, b) => new Date(b.dataFoto) - new Date(a.dataFoto));
            console.log(this.fotos)
        } catch (error) {
            console.error('Erro ao buscar fotos da API:', error);
        }
    },

    getImagePath(nomeArquivo){
      return `http://127.0.0.1:8000${nomeArquivo}`;
    },

    async salvarImagem() {

      if (this.formData.foto) {
        try {
          const response = await api.post('http://127.0.0.1:8000/fotos-animais/', this.formData, {
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
          });

          if (response.status === 201) {
              alert('Cadastro realizado com sucesso!');
              this.buscarFotos();
              this.resetForm();
          } else {
              alert('Erro ao cadastrar a foto do animal. Tente novamente mais tarde.');
          }
          } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      }
      else{
        alert('Nenhuma imagem encontrada.');
      }    
    },

    async resetForm(){
      this.resizedImage = null;
      this.formData = {
        id: null,
        foto: null,
        dataFoto: '',
        observacao: '',
        animal: 2,
      }
    },
  },
};
</script>

<style scoped>
.boxSelect {
  width: 900px;
  height: 500px;
  border: 1px solid black;
  border-radius: 20px;
  margin-bottom: 20px;
}

.boxSelect img {
  width: 900px;
  height: 500px;
  object-fit: cover;
  border-radius: 20px;
}

.modal-body-cadastro {
  justify-content: center;
  margin-top: 20px;
}

.modal-body-visu {
  display: flex;
  justify-content: center;
}

.slide {
  position: relative;
}

.slider {
  display: flex;
  overflow-x: hidden;
  width: 900px;
  border-radius: 20px;
}

.slide button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background-color: cornflowerblue;
  color: beige;
  position: absolute;
  top: 50%;
}

.slide button:hover {
  background-color: rgb(51, 93, 170);
}

.slide button:first-of-type {
  left: 0;
  transform: translate(-50%, -50%);
}
.slide button:last-of-type {
  right: 0;
  transform: translate(50%, -50%);
}


.content img {
  width: 900px;
  height: 500px;
  object-fit: cover;
  display: flex;
  border-radius: 20px;
}

h2{
  display: block;
  font-size: 20px;
}

.mb-3 {
  width: 900px;
}

form {
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
</style>

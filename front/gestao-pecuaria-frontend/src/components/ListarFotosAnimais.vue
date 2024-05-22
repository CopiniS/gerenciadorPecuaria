<template>
  <div>
    <label class="picture" for="picture__input" tabindex="0">
      <span class="picture__image" v-html="pictureImageContent"></span>
    </label>
    <input type="file" name="picture__input" id="picture__input" @change="onFileChange">
    <button v-if="fileSelected" @click="uploadImage">Upload Image</button>
  </div>
</template>

<script>
    import axios from 'axios';

    export default {
    data() {
        return {
        pictureImageTxt: "Choose an image",
        pictureImageContent: "Choose an image",
        fileSelected: false,
        file: null
        };
    },
    methods: {
        onFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            this.file = file; // Armazenar o arquivo selecionado
            this.fileSelected = true; // Atualizar o estado para mostrar o botão de upload

            const reader = new FileReader();
            reader.onload = (e) => {
            const img = `<img src="${e.target.result}" class="picture__img" />`;
            this.pictureImageContent = img;
            };
            reader.readAsDataURL(file);
        } else {
            this.pictureImageContent = this.pictureImageTxt;
            this.fileSelected = false;
            this.file = null;
        }
        },
        uploadImage() {
        if (this.file) {
            const formData = new FormData();
            formData.append('foto', this.file);
            formData.append('animal', '1');  // Substitua '1' pelo ID real do animal
            formData.append('dataFoto', new Date().toISOString().slice(0, 10)); // Data atual
            formData.append('observacao', 'Observação de exemplo');

            console.log('foto: ' , this.file)
            console.log('dataFoto: ' , new Date().toISOString().slice(0, 10))

            axios.post('http://127.0.0.1:8000/fotos-animais/', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                console.log('Imagem enviada com sucesso:', response.data);
                // Resetar o estado após o upload
                this.pictureImageContent = this.pictureImageTxt;
                this.fileSelected = false;
                this.file = null;
            })
            .catch(error => {
                console.error('Erro ao enviar a imagem:', error);
            });
        }
        }
    }
    };
</script>

<style scoped>
    #picture__input {
    display: none;
    }

    .picture {
    width: 400px;
    aspect-ratio: 16/9;
    background: #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #aaa;
    border: 2px dashed currentcolor;
    cursor: pointer;
    font-family: sans-serif;
    transition: color 300ms ease-in-out, background 300ms ease-in-out;
    outline: none;
    overflow: hidden;
    }

    .picture:hover {
    color: #777;
    background: #ccc;
    }

    .picture:active {
    border-color: turquoise;
    color: turquoise;
    background: #eee;
    }

    .picture:focus {
    color: #777;
    background: #ccc;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }

    .picture__img {
    max-width: 100%;
    }

</style>
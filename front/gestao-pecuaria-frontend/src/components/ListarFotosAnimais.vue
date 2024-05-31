<template>
    <div>
        <h2>Lista de Animais</h2>
        <div class="table-container">
            <table class="table table-bordered">
                <thead >
                    <tr>
                        <th scope="col">Brinco</th>
                        <th scope="col">Data Nascimento</th>
                        <th scope="col">Sexo</th>
                        <th scope="col">Raça</th>
                        <th scope="col">Brinco Pai</th>
                        <th scope="col">Brinco Mãe</th>
                        <th scope="col">Observações</th>
                        <th scope="col">Piquete</th>
                        <th scope="col">status</th>
                        <th scope="col"></th>
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
                        <td>{{ animal.piquete }}</td>
                        <td>{{ animal.status }}</td>
                        <td>
                            <div class="button-container">
                                <button @click="selecionaAnimal(animal)" type="button" class="btn btn-success" data-bs-toggle="modal"
                                data-bs-target="#cadastroModal" data-bs-whatever="@mdo">Adicionar Foto</button>
                            </div>
                            <div class="button-container">
                                <button @click="selecionaAnimal(animal); filterFotos(animal)" type="button" class="btn btn-success" data-bs-toggle="modal"
                                data-bs-target="#visuModal" data-bs-whatever="@mdo">Visualizar Foto</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!-- Modal de Cadastro de imagem -->
        <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de foto do animal</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3 input-group">
                            <label class="picture" for="picture__input" tabindex="0">
                            <span class="picture__image" v-html="pictureImageContent"></span>
                            </label>
                            <input type="file" name="picture__input" id="picture__input" @change="onFileChange">
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                            <input v-model="formData.dataFoto" type="date" class="form-control" id="dataFoto"
                            placeholder="Data da foto" required>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                            <textarea v-model="formData.observacao" class="form-control" id="observacao"
                            placeholder="Observação"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" @click="uploadImage">Enviar</button>
                    </div>
                </div>
            </div>
        </div>
         <!-- Modal de visualização de fotos -->
        <div class="modal fade" id="visuModal" tabindex="-1" aria-labelledby="visuModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="cadastroModalLabel">fotos do animal</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="slider">
                            <div v-for="(foto, index) in fotosFiltradas" :key="index">
                            <img :src="getImagePath(foto.foto)">
                            </div>
                            <button @click="prev">Anterior</button>
                            <button @click="next">Próximo</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import axios from 'axios';
    import api from '/src/interceptadorAxios';

    export default {
    data() {
        return {
        pictureImageTxt: "Choose an image",
        pictureImageContent: "Choose an image",
        fileSelected: false,
        animais: [],
        fotos: [],
        fotosFiltradas: [],
        formData: {
            foto: null,
            animal: null,
            dataFoto: '',
            observacao: '',
        },
        };
    },

    async mounted() {
        this.buscarAnimaisDaApi();
        this.buscarFotos();
    },

    methods: {
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

        async buscarFotos(){
            try {
                const response = await api.get('http://127.0.0.1:8000/fotos-animais/', {
                params: {
                    propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
                },
                });
                this.fotos = response.data;
            } catch (error) {
                console.error('Erro ao buscar fotos da API:', error);
            }
        },

        async filterFotos(animal){
            this.fotosFiltradas = [];
            this.fotos.forEach(foto => {
                console.log('nome foto ', foto.foto);
                if(foto.animal === animal.id){
                    this.fotosFiltradas.push(foto);
                }
            });
            console.log('fotos: ', this.fotosFiltradas);
        },

        getImagePath(nomeArquivo){
            return `http://127.0.0.1:8000${nomeArquivo}`;
        },

        async selecionaAnimal(animal){
            this.formData.animal = animal.id;
        },

        onFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            this.formData.foto = file; // Armazenar o arquivo selecionado
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
            this.formData.foto = null;
        }
        },
        async uploadImage() {
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
            this.pictureImageContent = this.pictureImageTxt;
            this.fileSelected = false;
            this.file = null;
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

    img {
    width: 50px;
    height: 50px;
    }

</style>
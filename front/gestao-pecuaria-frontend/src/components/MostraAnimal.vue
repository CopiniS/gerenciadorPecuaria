<template>
<div>
    <div class="animal-view">
        <h1>Detalhes do Animal</h1>
        <table class="table table-bordered">
        <thead >
          <tr>
            <th scope="col">Brinco</th>
            <th scope="col">Data Nascimento</th>
            <th scope="col">Sexo</th>
            <th scope="col">Raça</th>
            <th scope="col">Brinco Pai</th>
            <th scope="col">Brinco Mãe</th>
            <th scope="col">Raça de Observação</th>
            <th scope="col">Piquete</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="(animal, index) in animais" :key="index">
                <td>{{ animal.brinco }}</td>
                <td>{{ animal.dataNascimento }}</td>
                <td>{{ animal.sexo }}</td>
                <td>{{ animal.racaPredominante.nome }}</td>
                <td>{{ animal.brincoPai }}</td>
                <td>{{ animal.brincoMae }}</td>
                <td>{{ animal.racaObservacao }}</td>
                <td>{{ animal.piquete.nome }}</td>
                <td>{{ animal.status }}</td>
            </tr>
        </tbody>
        </table>
        <div class="actions">
            <button @click="abrirModalOcorrencia(animal)" class="btn btn-success" data-bs-toggle="modal"
                data-bs-target="#ocorrenciaModal">Incluir Ocorrência</button>
            <button @click="editarAnimal(animal); preencheListas()" class="btn btn-success" data-bs-toggle="modal"
                data-bs-target="#edicaoModal" data-bs-whatever="@mdo">Editar</button>
            <button @click="editarAnimal(animal)" class="btn btn-success" data-bs-toggle="modal"
                data-bs-target="#confirmacaoExclusaoModal">Excluir</button>
            <button @click="addPhoto" class="btn btn-success" data-bs-toggle="modal"
                data-bs-target="#cadastroModal">Adicionar Foto</button>
            <button @click="viewPhotos" class="btn btn-success" data-bs-toggle="modal"
                data-bs-target="#visuModal">Visualizar Fotos</button>

        </div>
    </div>

    <!-- Modal de Edição -->
    <div class="modal fade" id="edicaoModal" tabindex="-1" aria-labelledby="edicaoModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="edicaoModalLabel">Editar animal</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                            <input v-model="formData.brinco" type="text" class="form-control" id="brincoEditar"
                                placeholder="Número do Brinco" required>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                            <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                placeholder="Data de nascimento" class="form-control" id="dataNascimentoEdicao"
                                v-model="formData.dataNascimento" required>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-venus-mars"></i></span>
                            <select v-model="formData.sexo" class="form-select" id="sexoEditar">
                                <option disabled value="">Selecione o sexo</option>
                                <option v-for="opcao in ['macho', 'femea']" :key="opcao" :value="opcao"
                                    v-bind:selected="formData.sexo === opcao">{{ opcao }}</option>
                            </select>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-horse"></i></span>
                            <select v-model="formData.racaPredominante" class="form-select" id="racaPredominante"
                                aria-label="Raça Predominante" required>
                                <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }} </option>
                            </select>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                            <textarea v-model="formData.racaObservacao" class="form-control" id="racaObservacaoEditar"
                                placeholder="Observações sobre a Raça"></textarea>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-tag"></i></span>
                            <select v-model="formData.piquete" class="form-select" id="piquete" aria-label="Piquete"
                                required>
                                <option disabled selected>Selecione o piquete</option>
                                <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{
                    piquete.nome }}</option>
                            </select>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-mars"></i></span>
                            <input v-model="formData.brincoPai" @input="filterMachos()" type="text" class="form-control"
                                placeholder="Digite o brinco do Pai...">
                        </div>
                        <div class="list-group" v-if="formData.brincoPai && machosFiltrados.length">
                            <button type="button" class="list-group-item list-group-item-action"
                                v-for="animal in machosFiltrados" :key="animal.id" @click="selectPai(animal)">
                                {{ animal.brinco }}
                            </button>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-venus"></i></span>
                            <input v-model="formData.brincoMae" @input="filterFemeas()" type="text" class="form-control"
                                placeholder="Digite o brinco da Mãe...">
                        </div>
                        <div class="list-group" v-if="formData.brincoMae && femeasFiltradas.length">
                            <button type="button" class="list-group-item list-group-item-action"
                                v-for="animal in femeasFiltradas" :key="animal.id" @click="selectMae(animal)">
                                {{ animal.brinco }}
                            </button>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                            <input v-model="formData.rfid" type="text" class="form-control" id="rfid" placeholder="RFID"
                                required>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                            <input v-model="formData.observacoes" type="text" class="form-control" id="observacoes"
                                placeholder="Observações" required>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-primary" @click="submitForm">Salvar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Ocorrência -->
    <div class="modal fade" id="ocorrenciaModal" tabindex="-1" aria-labelledby="ocorrenciaModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ocorrenciaModalLabel">Registrar Ocorrência</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="registrarOcorrencia">
                        <div class="mb-3">
                            <label for="dataOcorrencia" class="form-label">Data da Ocorrência</label>
                            <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                placeholder="Data da Ocorência" class="form-control" id="dataOcorrencia"
                                v-model="novaOcorrencia.dataOcorrencia" required>
                        </div>
                        <div class="mb-3">
                            <label for="tipoOcorrencia" class="form-label">Tipo da Ocorrência</label>
                            <select class="form-select" id="tipoOcorrencia" v-model="novaOcorrencia.tipoOcorrencia"
                                required>
                                <option value="Morte">Morte</option>
                                <option value="Doença">Doença</option>
                                <option value="Outro">Outro</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="descricaoOcorrencia" class="form-label">Descrição</label>
                            <textarea class="form-control" id="descricaoOcorrencia"
                                v-model="novaOcorrencia.descricao"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Registrar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

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
                            <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                placeholder="Data da foto" class="form-control" id="dataFoto"
                                v-model="formData.dataFoto" required>
                        </div>
                        <div class="mb-3 input-group">
                            <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                            <textarea v-model="formData.observacao" class="form-control" id="observacao"
                                placeholder="Observação"></textarea>
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

    <!-- Modal de Confirmação de Exclusão -->
    <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1" aria-labelledby="confirmacaoExclusaoModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="confirmacaoExclusaoModalLabel">Confirmação de Exclusão</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Tem certeza de que deseja excluir este animal?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-danger" @click="apagarAnimal">Excluir</button>
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
            animalId: null,
            animal: null,
            animais: null,
            listaFemeas: [],
            listaMachos: [],
            femeasFiltradas: [],
            machosFiltrados: [],
            racas: [],
            piquetes: [],
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
            },
            novaOcorrencia: {
                dataOcorrencia: '',
                tipoOcorrencia: '',
                descricao: null,
            },
        };
    },
    mounted() {
        this.animalId = localStorage.getItem('animalSelecionado');
        this.buscarAnimalDaApi();
        this.slider = document.querySelector('.slider');
        this.width = window.getComputedStyle(this.slider).width;
        this.buscarFotos();
        this.preencheListas();
        this.buscarPiquetesDaApi();
        this.buscarRacasDaApi();
    },

    methods: {

        async buscarAnimalDaApi() {
      try {
        const response = await api.get(`http://127.0.0.1:8000/animais/animal/${this.animalId}/`);
        this.animais = response.data;
        this.animal = this.animais[0];
      } catch (error) {
        console.error('Erro ao buscar animal da API:', error);
      }
    },

    async buscarPiquetesDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/piquetes/', {
          params: {
            propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
          },
        });
        this.piquetes = response.data;
      } catch (error) {
        console.error('Erro ao buscar piquetes da API:', error);
      }
    },

    async buscarRacasDaApi() {
      try {
        const response = await api.get('http://127.0.0.1:8000/racas/', {
        });
        this.racas = response.data;
      } catch (error) {
        console.error('Erro ao buscar raças da API:', error);
      }
    },

        formatDate(date) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(date).toLocaleDateString(undefined, options);
        },
        editarAnimal(animal) {
            this.formData = {
                id: animal.id,
                brinco: animal.brinco,
                dataNascimento: animal.dataNascimento,
                sexo: animal.sexo,
                racaPredominante: animal.racaPredominante.id,
                racaObservacao: animal.racaObservacao,
                piquete: animal.piquete.id,
                brincoPai: animal.brincoPai,
                brincoMae: animal.brincoMae,
                status: 'Vivo',
                rfid: animal.rfid,
                observacoes: animal.observacoes,
            };
        },
        fecharModal(modalId) {
            var closeButton = document.getElementById(modalId).querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                console.error('Botão de fechar não encontrado no modal:', modalId);
            }
        },
        async apagarAnimal() {
            try {
                const response = await api.delete(`http://127.0.0.1:8000/animais/${this.formData.id}/`, {
                });

                if (response.status === 204) {
                    alert('Animal apagado com sucesso!');
                    this.$router.push('/animais');
                } else {
                    alert('Erro ao apagar animal. Tente novamente mais tarde.');
                }
            } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
            this.fecharModal("confirmacaoExclusaoModal");
        }, 
        
        async submitForm() {
            try {
                console.log('formdata: ', this.formData);
                const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formData.id}/`, this.formData, {
                });

                if (response.status === 200) {
                    alert('Alterações salvas com sucesso!');
                    this.resetForm();
                    this.buscarAnimalDaApi();
                    this.fecharModal("edicaoModal");
                } else {
                    alert('Erro ao salvar alterações. Tente novamente mais tarde.');
                }
            } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
        },

        abrirModalOcorrencia() {
            // Limpar dados da ocorrência anterior
            this.novaOcorrencia = {
            dataOcorrencia: '',
            tipoOcorrencia: '',
            descricao: null,
            };
        },

        
        async registrarOcorrencia() {
            try {
            // Enviar dados da ocorrência para a API
            const response = await api.post(`http://127.0.0.1:8000/ocorrencias/`, {
                animal: this.animal.id,
                dataOcorrencia: this.novaOcorrencia.dataOcorrencia,
                tipo: this.novaOcorrencia.tipoOcorrencia,
                descricao: this.novaOcorrencia.descricao,
            });
            if (response.status === 201) {
                alert('Ocorrência registrada com sucesso!');
                // Atualizar lista de animais
                this.buscarAnimalDaApi();
            } else {
                alert('Erro ao registrar ocorrência. Tente novamente mais tarde.');
            }
            } catch (error) {
            console.error('Erro ao enviar requisição:', error);
            alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
            this.fecharModal("ocorrenciaModal");
        },

        async preencheListas() {
            this.preencherListaMachos();
            this.preencherListaFemeas();
        },

        async preencherListaFemeas() {
            const response = await api.get(`http://127.0.0.1:8000/animais/femeas`, {
                params: {
                    propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
                },
            });
            this.listaFemeas = response.data;
        },

        async preencherListaMachos() {
            const response = await api.get(`http://127.0.0.1:8000/animais/machos`, {
                params: {
                    propriedadeSelecionada: localStorage.getItem('propriedadeSelecionada')
                },
            });
            this.listaMachos = response.data;
        },

        filterFemeas() {
            this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoMae));
        },

        filterMachos() {
            this.machosFiltrados = this.listaMachos.filter(animal => animal.brinco.toLowerCase().includes(this.formData.brincoPai));
        },

        selectPai(animal) {
            this.formData.brincoPai = animal.brinco;
            this.machosFiltrados = [];
        },

        selectMae(animal) {
            this.formData.brincoMae = animal.brinco;
            this.femeasFiltradas = [];
        },
        controlaSlide(id) {
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

        async buscarFotos() {
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

        getImagePath(nomeArquivo) {
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
            else {
                alert('Nenhuma imagem encontrada.');
            }
        },

        async resetForm() {
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
.animal-view {
    padding: 20px;
}

.actions {
    margin-top: 20px;
}

.actions button {
    margin-right: 10px;
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
</style>
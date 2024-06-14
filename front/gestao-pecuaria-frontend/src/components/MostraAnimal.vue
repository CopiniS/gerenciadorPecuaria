<template>
    <div>
        <div class="animal-view">
            <h1>Detalhes do Animal</h1>
            <div class="actions d-flex flex-wrap">
                <button @click="abrirModalOcorrencia(animal)" class="btn btn-success mx-1" data-bs-toggle="modal"
                    data-bs-target="#ocorrenciaModal">Incluir Ocorrência</button>
                <button @click="editarAnimal(animal); preencheListas()" class="btn btn-success mx-1"
                    data-bs-toggle="modal" data-bs-target="#edicaoModal" data-bs-whatever="@mdo">Editar</button>
                <button @click="editarAnimal(animal)" class="btn btn-success mx-1" data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal">Excluir</button>
                <button class="btn btn-success mx-1" data-bs-toggle="modal" data-bs-target="#cadastroModal">Adicionar
                    Foto</button>
                <button @click="buscarFotos()" class="btn btn-success mx-1" data-bs-toggle="modal"
                    data-bs-target="#visuModal">Visualizar Fotos</button>
            </div>

            <div class="d-flex align-items-start table-container flex-column">
                    <form class="row g-3 align-items-center">
                    <div class="col-auto d-flex align-items-center">
                        <label for="brinco" class="form-label me-2">Brinco</label>
                        <input v-model="formDataAnimal.brinco" type="text" class="form-control" id="brinco"
                            placeholder="Número do Brinco" required>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="dataNascimento" class="form-label me-2">Data de Nascimento</label>
                        <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                            placeholder="Data de nascimento" class="form-control" id="dataNascimento"
                            v-model="formDataAnimal.dataNascimento" required>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="sexo" class="form-label me-2">Sexo</label>
                        <select v-model="formDataAnimal.sexo" class="form-select" id="sexo">
                            <option disabled value="">Selecione o sexo</option>
                            <option v-for="opcao in ['macho', 'femea']" :key="opcao" :value="opcao"
                                v-bind:selected="formDataAnimal.sexo === opcao">{{ opcao }}</option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="raca" class="form-label me-2">Raça</label>
                        <select v-model="formDataAnimal.racaPredominante" class="form-select" id="racaPredominante"
                            aria-label="Raça Predominante" required>
                            <option disabled value="">Selecione a raça</option>
                            <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }} </option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="observacaoRaca" class="form-label me-2">Observações da Raça</label>
                        <textarea v-model="formDataAnimal.racaObservacao" class="form-control" id="racaObservacao"
                            placeholder="Observações sobre a Raça"></textarea>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="piquete" class="form-label me-2">Piquete</label>
                        <select v-model="formDataAnimal.piquete" class="form-select" id="piquete" aria-label="Piquete"
                            required>
                            <option disabled selected>Selecione o piquete</option>
                            <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{
                    piquete.nome }}</option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="brincoPai" class="form-label me-2">Brinco pai</label>
                        <input v-model="formDataAnimal.brincoPai" @input="filterMachos()" type="text" class="form-control"
                            placeholder="Digite o brinco do Pai...">
                    </div>
                    <div class="list-group" v-if="formDataAnimal.brincoPai && machosFiltrados.length">
                        <button type="button" class="list-group-item list-group-item-action"
                            v-for="animal in machosFiltrados" :key="animal.id" @click="selectPai(animal)">
                            {{ animal.brinco }}
                        </button>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="brincoMae" class="form-label me-2">Brinco mãe</label>
                        <input v-model="formDataAnimal.brincoMae" @input="filterFemeas()" type="text" class="form-control"
                            placeholder="Digite o brinco da Mãe...">
                    </div>
                    <div class="list-group" v-if="formDataAnimal.brincoMae && femeasFiltradas.length">
                        <button type="button" class="list-group-item list-group-item-action"
                            v-for="animal in femeasFiltradas" :key="animal.id" @click="selectMae(animal)">
                            {{ animal.brinco }}
                        </button>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="rfid" class="form-label me-2">RfId</label>
                        <input v-model="formDataAnimal.rfid" type="text" class="form-control" id="rfid" placeholder="RFID"
                            required>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="observacoes" class="form-label me-2">Observações</label>
                        <textarea v-model="formDataAnimal.observacoes" class="form-control" id="observacoes"
                            placeholder="Observações" required> </textarea>
                    </div>
                    <div v-if="formDataAnimal.dataCompra" class="col-auto d-flex align-items-center">
                        <label for="dataCompra" class="form-label me-2">DataCompra</label>
                        <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                            placeholder="Data da compra" class="form-control" id="dataDaCompra"
                            v-model="formDataAnimal.dataCompra" required>
                    </div>
                    <div v-if="formDataAnimal.valorCompra" class="col-auto d-flex align-items-center">
                        <label for="valor" class="form-label me-2">Valor Compra</label>
                        <input v-model="formDataAnimal.valorCompra" type="text" class="form-control" id="valorCompra"
                            placeholder="Valor da compra" required>
                    </div>
                </form>

                <h2>Ocorrências</h2>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Tipo</th>
                        <th>Descrição</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ocorrencia in ocorrencias" :key="ocorrencia.id">
                        <td>{{ formatarData(ocorrencia.dataOcorrencia) }}</td>
                        <td>{{ ocorrencia.tipo }}</td>
                        <td>{{ ocorrencia.descricao }}</td>
                        <td>
                            <button @click="editarOcorrencia(ocorrencia)" class="btn btn-warning btn-sm" data-bs-toggle="modal"
                                data-bs-target="#ocorrenciaModalEdicao">Editar</button>
                            <button @click="excluirOcorrencia(ocorrencia.id)" class="btn btn-danger btn-sm" data-bs-toggle="modal"
                                data-bs-target="#confirmacaoExclusaoOcorrenciaModal">Excluir</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            </div>

        </div>

        <!-- Modal de Edição de animal -->
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
                                <input v-model="formDataAnimal.brinco" type="text" class="form-control" id="brincoEditar"
                                    placeholder="Número do Brinco" required>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-calendar"></i></span>
                                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                    placeholder="Data de nascimento" class="form-control" id="dataNascimentoEdicao"
                                    v-model="formDataAnimal.dataNascimento" required>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-venus-mars"></i></span>
                                <select v-model="formDataAnimal.sexo" class="form-select" id="sexoEditar">
                                    <option disabled value="">Selecione o sexo</option>
                                    <option v-for="opcao in ['macho', 'femea']" :key="opcao" :value="opcao"
                                        v-bind:selected="formDataAnimal.sexo === opcao">{{ opcao }}</option>
                                </select>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-horse"></i></span>
                                <select v-model="formDataAnimal.racaPredominante" class="form-select" id="racaPredominante"
                                    aria-label="Raça Predominante" required>
                                    <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                                <textarea v-model="formDataAnimal.racaObservacao" class="form-control"
                                    id="racaObservacaoEditar" placeholder="Observações sobre a Raça"></textarea>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-tag"></i></span>
                                <select v-model="formDataAnimal.piquete" class="form-select" id="piquete" aria-label="Piquete"
                                    required>
                                    <option disabled selected>Selecione o piquete</option>
                                    <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{
                    piquete.nome }}</option>
                                </select>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-mars"></i></span>
                                <input v-model="formDataAnimal.brincoPai" @input="filterMachos()" type="text"
                                    class="form-control" placeholder="Digite o brinco do Pai...">
                            </div>
                            <div class="list-group" v-if="formDataAnimal.brincoPai && machosFiltrados.length">
                                <button type="button" class="list-group-item list-group-item-action"
                                    v-for="animal in machosFiltrados" :key="animal.id" @click="selectPai(animal)">
                                    {{ animal.brinco }}
                                </button>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-venus"></i></span>
                                <input v-model="formDataAnimal.brincoMae" @input="filterFemeas()" type="text"
                                    class="form-control" placeholder="Digite o brinco da Mãe...">
                            </div>
                            <div class="list-group" v-if="formDataAnimal.brincoMae && femeasFiltradas.length">
                                <button type="button" class="list-group-item list-group-item-action"
                                    v-for="animal in femeasFiltradas" :key="animal.id" @click="selectMae(animal)">
                                    {{ animal.brinco }}
                                </button>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                                <input v-model="formDataAnimal.rfid" type="text" class="form-control" id="rfid"
                                    placeholder="RFID" required>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                                <textarea v-model="formDataAnimal.observacoes" class="form-control" id="observacoes"
                                    placeholder="Observações" required></textarea>
                            </div>
                            <div class="mb-3 input-group">
                                <input v-model="comprado" type="checkbox" id="check-comprado"> Animal Comprado
                            </div>
                            <div v-if="comprado" class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-calendar">*</i></span>
                                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                    placeholder="Data da compra" class="form-control" id="dataDaCompra"
                                    v-model="formDataAnimal.dataCompra" required>
                            </div>
                            <div v-if="comprado" class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-weight"></i>*</span>
                                <input v-model="formDataAnimal.valorCompra" type="text" class="form-control" id="valorCompra"
                                    placeholder="Valor da compra" required>
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
                                <label for="tipo" class="form-label">Tipo da Ocorrência</label>
                                <select class="form-select" id="tipo" v-model="novaOcorrencia.tipo"
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

        <!-- Modal de Edição de Ocorrência -->
        <div class="modal fade" id="ocorrenciaModalEdicao" tabindex="-1" aria-labelledby="ocorrenciaModalEdicaoLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="ocorrenciaModalEdicaoLabel">Editar Ocorrência</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitEdicaoOcorrencia">
                            <div class="mb-3">
                                <label for="dataOcorrencia" class="form-label">Data da Ocorrência</label>
                                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                    placeholder="Data da Ocorência" class="form-control" id="dataOcorrencia"
                                    v-model="novaOcorrencia.dataOcorrencia" required>
                            </div>
                            <div class="mb-3">
                                <label for="tipo" class="form-label">Tipo da Ocorrência</label>
                                <select class="form-select" id="tipo" v-model="novaOcorrencia.tipo"
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
        <div class="modal fade" id="cadastroModal" tabindex="-1" aria-labelledby="cadastroModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="cadastroModalLabel">Cadastro de Fotos</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body-cadastro">
                        <form class="form-foto">
                            <div class="mb-3 input-group mb-3-foto">
                                <span class="input-group-text"><i class="fas fa-calendar-alt"></i></span>
                                <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')"
                                    placeholder="Data da foto" class="form-control" id="dataFoto"
                                    v-model="formDataFoto.dataFoto" required>
                            </div>
                            <div class="mb-3 input-group mb-3-foto">
                                <span class="input-group-text"><i class="fas fa-sticky-note"></i></span>
                                <textarea v-model="formDataFoto.observacao" class="form-control" id="observacao"
                                    placeholder="Observação"></textarea>
                            </div>
                            <div class="mb-3 input-group mb-3-foto">
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
        <div class="modal fade" id="confirmacaoExclusaoModal" tabindex="-1"
            aria-labelledby="confirmacaoExclusaoModalLabel" aria-hidden="true">
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

        <!-- Modal de Confirmação de Exclusão de Ocorrencia -->
        <div class="modal fade" id="confirmacaoExclusaoOcorrenciaModal" tabindex="-1"
            aria-labelledby="confirmacaoExclusaoOcorrenciaModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="confirmacaoExclusaoOcorrenciaModalLabel">Confirmação de Exclusão</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Tem certeza de que deseja excluir esta Ocorrência?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-danger" @click="apagarOcorrencia">Excluir</button>
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
            ocorrencias: [],
            piquetes: [],
            slider: null,
            width: 0,
            resizedImage: null,
            fotos: [],
            comprado: false,
            formDataFoto: {
                id: null,
                foto: null,
                dataFoto: '',
                observacao: '',
                animal: null,
            },
            formDataAnimal: {
                id: null,
                brinco: null,
                dataNascimento: null,
                sexo: null,
                racaPredominante: null,
                racaObservacao: null,
                piquete: null,
                brincoPai: null,
                brincoMae: null,
                status: null,
                rfid: null,
                observacoes: null,
                dataCompra: null,
                valorCompra: null,
            },
            novaOcorrencia: {
                dataOcorrencia: '',
                tipo: '',
                descricao: null,
            },
        };
    },
    mounted() {
        this.animalId = localStorage.getItem('animalSelecionado');
        this.buscarAnimalDaApi();
        this.slider = document.querySelector('.slider');
        this.width = window.getComputedStyle(this.slider).width;
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
                this.formDataFoto.animal = this.animal.id;
                this.buscarOcorrenciasDoAnimal();
                this.editarAnimal(this.animal);
            } catch (error) {
                console.error('Erro ao buscar animal da API:', error);
            }
        },

        async buscarOcorrenciasDoAnimal() {
            try {
                const response = await api.get(`http://127.0.0.1:8000/ocorrencias/`, {
                    params: {
                        animalSelecionado: this.animal.id
                    },
                });
                this.ocorrencias = response.data;
            } catch (error) {
                console.error('Erro ao buscar ocorrencias do animal na API:', error);
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
            this.formDataAnimal = {
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
                dataCompra: animal.dataCompra,
                valorCompra: animal.valorCompra,
            };

            if (this.formDataAnimal.dataCompra != null) {
                this.comprado = true;
            }
        },

        editarOcorrencia(ocorrencia){
            this.novaOcorrencia = {
                id: ocorrencia.id,
                dataOcorrencia: ocorrencia.dataOcorrencia,
                tipo: ocorrencia.tipo,
                descricao: ocorrencia.descricao,
            }
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
                const response = await api.delete(`http://127.0.0.1:8000/animais/${this.formDataAnimal.id}/`, {
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
                const response = await api.patch(`http://127.0.0.1:8000/animais/${this.formDataAnimal.id}/`, this.formDataAnimal, {
                });

                if (response.status === 200) {
                    alert('Alterações salvas com sucesso!');
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

        resetFormOcorrecia(){
            this.novaOcorrencia = {
                id: null,
                dataOcorrencia: '',
                tipo: '',
                descricao: null,
            };
        },

        excluirOcorrencia(ocorrenciaId){
            this.novaOcorrencia ={
                id: ocorrenciaId,
            }
        },

        abrirModalOcorrencia() {
            // Limpar dados da ocorrência anterior
            this.novaOcorrencia = {
                dataOcorrencia: '',
                tipo: '',
                descricao: null,
            };
        },


        async registrarOcorrencia() {
            try {
                // Enviar dados da ocorrência para a API
                const response = await api.post(`http://127.0.0.1:8000/ocorrencias/`, {
                    animal: this.animal.id,
                    dataOcorrencia: this.novaOcorrencia.dataOcorrencia,
                    tipo: this.novaOcorrencia.tipo,
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

        async submitEdicaoOcorrencia(){
            try {
                const response = await api.patch(`http://127.0.0.1:8000/ocorrencias/${this.novaOcorrencia.id}/`, this.novaOcorrencia , {
                });

                if (response.status === 200) {
                    alert('Alterações salvas com sucesso!');
                    this.resetFormOcorrecia();
                    this.buscarOcorrenciasDoAnimal();
                    this.fecharModal("ocorrenciaModalEdicao");
                } else {
                    alert('Erro ao salvar alterações. Tente novamente mais tarde.');
                }
                } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
        },

        async apagarOcorrencia(){
            try {
                const response = await api.delete(`http://127.0.0.1:8000/ocorrencias/${this.novaOcorrencia.id}/`, {
                });

                if (response.status === 204) {
                    alert('Ocorrência apagada com sucesso!');
                    this.buscarOcorrenciasDoAnimal();
                } else {
                    alert('Erro ao apagar ocorrencia. Tente novamente mais tarde.');
                }
            } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
            this.fecharModal("confirmacaoExclusaoOcorrenciaModal");
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
            this.femeasFiltradas = this.listaFemeas.filter(animal => animal.brinco.toLowerCase().includes(this.formDataAnimal.brincoMae));
        },

        filterMachos() {
            this.machosFiltrados = this.listaMachos.filter(animal => animal.brinco.toLowerCase().includes(this.formDataAnimal.brincoPai));
        },

        selectPai(animal) {
            this.formDataAnimal.brincoPai = animal.brinco;
            this.machosFiltrados = [];
        },

        selectMae(animal) {
            this.formDataAnimal.brincoMae = animal.brinco;
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
                this.formDataFoto.foto = file;

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
                        animalSelecionado: this.animal.id
                    },
                });
                this.fotos = response.data;
                this.fotos = this.fotos.sort((a, b) => new Date(b.dataFoto) - new Date(a.dataFoto));
            } catch (error) {
                console.error('Erro ao buscar fotos da API:', error);
            }
        },

        getImagePath(nomeArquivo) {
            return `http://127.0.0.1:8000${nomeArquivo}`;
        },

        async salvarImagem() {

            if (this.formDataFoto.foto) {
                try {
                    const response = await api.post('http://127.0.0.1:8000/fotos-animais/', this.formDataFoto, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                    if (response.status === 201) {
                        alert('Cadastro realizado com sucesso!');
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
            this.formDataFoto = {
                id: null,
                foto: null,
                dataFoto: '',
                observacao: '',
                animal: this.animal.id,
            }
        },

        formatarData(data) {
            const date = new Date(data);
            const utcDate = new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'UTC' };
            return utcDate.toLocaleDateString('pt-BR', options);
        },
    },

};
</script>

<style scoped>
.table-container {
    margin-left: 20px;
    margin-right: 20px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.table-container table thead tr th {
  border-bottom: 2px solid #4CAF50; /* Adiciona uma borda verde na parte inferior */
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
    border: 1px solid black;
    border-radius: 20px;
    margin-bottom: 20px;
}

.boxSelect img {
    width: 100%; 
    height: 100%;
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
    width: 90%; 
    max-width: 900px;
}

.slider {
    display: flex;
    overflow-x: hidden;
    width: 100%; 
}

.slide button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    background-color: cornflowerblue;
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

.content{
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
</style>
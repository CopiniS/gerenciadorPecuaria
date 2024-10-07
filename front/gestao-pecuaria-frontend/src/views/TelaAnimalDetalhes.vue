<template>
    <div class="background">
        <nav>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">
                <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
                    @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais"
                    aria-selected="true">Lista
                    de Animais</button>
                <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-view-tab"
                    @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-view"
                    aria-selected="true">Vizualização
                    do Animal</button>
            </div>
        </nav>
        <div class="tab-content" id="nav-tabContent">
            <div class="tab-pane fade" :class="{ 'show active': activeTab === 'animais' }" id="nav-animais"
                role="tabpanel" aria-labelledby="nav-animais-tab">
            </div>
            <div class="tab-pane fade" :class="{ 'show active': activeTab === 'visualizacao' }" id="nav-view"
                role="tabpanel" aria-labelledby="nav-view-tab">
            </div>
        </div>

        <div class="animal-view">
            <h1>Detalhes do Animal</h1>
            <div class="actions d-flex flex-wrap">
                <button @click="acessarEdicao(animal)" class="btn btn-success mx-1">Editar</button>
                <button class="btn btn-success mx-1" data-bs-toggle="modal"
                    data-bs-target="#confirmacaoExclusaoModal">Excluir</button>
                <button class="btn btn-success mx-1" @click="acessarFotoCadastro">Cadastrar Foto</button>
                <button @click="acessarFotoVisualizacao(animal)" class="btn btn-success mx-1">Visualizar Fotos</button>
                <button @click="acessarOcorrenciaCadastro(animal)" class="btn btn-success mx-1">Incluir
                    Ocorrência</button>

            </div>

            <div class="d-flex align-items-start table-container flex-column">
                <form class="row g-3 align-items-center">
                    <div class="col-auto d-flex align-items-center">
                        <label for="brinco" class="form-label me-2">Brinco</label>
                        <input v-model="formDataAnimal.brinco" type="text" class="form-control" id="brinco" disabled>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="dataNascimento" class="form-label me-2">Data de Nascimento</label>
                        <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" class="form-control"
                            id="dataNascimento" v-model="formDataAnimal.dataNascimento" disabled>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="sexo" class="form-label me-2">Sexo</label>
                        <select v-model="formDataAnimal.sexo" class="form-select" id="sexo" disabled>
                            <option disabled value="">Selecione o sexo</option>
                            <option v-for="opcao in ['macho', 'femea']" :key="opcao" :value="opcao"
                                v-bind:selected="formDataAnimal.sexo === opcao">{{ opcao }}</option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="raca" class="form-label me-2">Raça</label>
                        <select v-model="formDataAnimal.racaPredominante" class="form-select" id="racaPredominante"
                            aria-label="Raça Predominante" disabled>
                            <option disabled :value="null">Raça</option>
                            <option v-for="raca in racas" :key="raca.id" :value="raca.id">{{ raca.nome }} </option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="observacaoRaca" class="form-label me-2">Observações da Raça</label>
                        <input v-model="formDataAnimal.racaObservacao" class="form-control" id="racaObservacao"
                            disabled>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="piquete" class="form-label me-2">Piquete</label>
                        <select v-model="formDataAnimal.piquete" class="form-select" id="piquete" aria-label="Piquete"
                            disabled>
                            <option :value="null" disabled>Piquete</option>
                            <option v-for="piquete in piquetes" :key="piquete.id" :value="piquete.id">{{
                                piquete.nome }}</option>
                        </select>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="brincoPai" class="form-label me-2">Brinco pai</label>
                        <input v-model="formDataAnimal.brincoPai" @input="filterMachos()" type="text"
                            class="form-control" disabled>
                    </div>
                    <div class="list-group" v-if="formDataAnimal.brincoPai && machosFiltrados.length">
                        <button type="button" class="list-group-item list-group-item-action"
                            v-for="animal in machosFiltrados" :key="animal.id" @click="selectPai(animal)">
                            {{ animal.brinco }}
                        </button>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="brincoMae" class="form-label me-2">Brinco mãe</label>
                        <input v-model="formDataAnimal.brincoMae" @input="filterFemeas()" type="text"
                            class="form-control" disabled>
                    </div>
                    <div class="list-group" v-if="formDataAnimal.brincoMae && femeasFiltradas.length">
                        <button type="button" class="list-group-item list-group-item-action"
                            v-for="animal in femeasFiltradas" :key="animal.id" @click="selectMae(animal)">
                            {{ animal.brinco }}
                        </button>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="rfid" class="form-label me-2">RfId</label>
                        <input v-model="formDataAnimal.rfid" type="text" class="form-control" id="rfid" disabled>
                    </div>
                    <div class="col-auto d-flex align-items-center">
                        <label for="observacoes" class="form-label me-2">Observações</label>
                        <input v-model="formDataAnimal.observacoes" class="form-control" id="observacoes" disabled>
                    </div>
                    <div v-if="formDataAnimal.dataCompra" class="col-auto d-flex align-items-center">
                        <label for="dataCompra" class="form-label me-2">DataCompra</label>
                        <input type="text" onfocus="(this.type='date')" onblur="(this.type='text')" class="form-control"
                            id="dataDaCompra" v-model="formDataAnimal.dataCompra" disabled>
                    </div>
                    <div v-if="formDataAnimal.valorCompra" class="col-auto d-flex align-items-center">
                        <label for="valor" class="form-label me-2">Valor Compra</label>
                        <input v-model="formDataAnimal.valorCompra" type="text" class="form-control" id="valorCompra"
                            disabled>
                    </div>
                </form>
            </div>

            <!-- Ocorrências -->
            <div class="d-flex align-items-start table-container flex-column">
                <h2>Ocorrências</h2>
                <div class="button-container">
                    <RelatorioPdf titulo="Relatório de Ocorrências"
                        :cabecalho="['Nome do produtor: ' + nomeProdutor, 'Propriedade: ' + propriedadeAtualNome]"
                        :colunas="['Brinco', 'Data da ocorrência', 'Tipo', 'Descrição']"
                        :dados="ocorrencias.map(ocorrencia => [formDataAnimal.brinco, formatarData(ocorrencia.dataOcorrencia), ocorrencia.tipo, ocorrencia.descricao])" />
                </div>
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
                                <button @click="acessarOcorrenciaEdicao(ocorrencia)" class="btn-acoes btn-sm"
                                    title="Editar Ocorrência"><i class="fas fa-edit"></i></button>
                                <button @click="excluirOcorrencia(ocorrencia.id)" class="btn-acoes btn-sm"
                                    data-bs-toggle="modal" data-bs-target="#confirmacaoExclusaoOcorrenciaModal"><i
                                        class="fas fa-trash-alt" title="Excluir Ocorrência"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
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
                        <h5 class="modal-title" id="confirmacaoExclusaoOcorrenciaModalLabel">Confirmação de Exclusão
                        </h5>
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
import RelatorioPdf from '../components/RelatorioPdf.vue';

export default {
    components: {
        RelatorioPdf
    },
    data() {
        return {
            activeTab: 'visualizacao',
            propriedadeAtualNome: localStorage.getItem('propriedadeSelecionadaNome'),
            nomeProdutor: localStorage.getItem('produtorNome'),
            ocorrenciaId: null,
            animal: null,
            listaFemeas: [],
            listaMachos: [],
            femeasFiltradas: [],
            machosFiltrados: [],
            racas: [],
            ocorrencias: [],
            piquetes: [],
            comprado: false,
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
        };
    },
    mounted() {
        const animalId = this.$route.params.animalId;
        this.fetchAnimal(animalId);
        this.buscarPiquetesDaApi();
        this.buscarRacasDaApi();
    },

    methods: {
        //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
        async fetchAnimal(animalId) {
            try {
                const response = await api.get(`http://127.0.0.1:8000/animais/animal/${animalId}/`);
                const animais = response.data;
                this.animal = animais[0];

                this.buscarOcorrenciasDoAnimal();
                this.preencheFormAnimal();
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

        async apagarAnimal() {
            try {
                const response = await api.delete(`http://127.0.0.1:8000/animais/${this.formDataAnimal.id}/`, {
                });

                if (response.status === 204) {
                    alert('Exclusão realizada com sucesso!');
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

        async apagarOcorrencia() {
            try {
                const response = await api.delete(`http://127.0.0.1:8000/ocorrencias/${this.ocorrenciaId}/`, {
                });

                if (response.status === 204) {
                    alert('Exclusão realizada com sucesso');
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


        //ACESSAR OUTRAS PÁGINAS----------------------------------------------------------------------------------------------------------------------------------------------------------
        acessarEdicao(animal) {
            this.$router.push({
                name: 'AnimalEdicao',
                params: { animalId: animal.id }
            })
        },

        acessarOcorrenciaCadastro(animal) {
            this.$router.push({
                name: 'OcorrenciaCadastro',
                params: { animalId: animal.id }
            })
        },

        acessarOcorrenciaEdicao(ocorrencia) {
            this.$router.push({
                name: 'OcorrenciaEdicao',
                params: { ocorrenciaId: ocorrencia.id }
            })
        },

        acessarFotoCadastro(animal) {
            this.$router.push({
                name: 'FotoCadastro',
                params: { animalId: animal.id }
            })
        },

        acessarFotoVisualizacao(animal) {
            this.$router.push({
                name: 'FotoVisualizacao',
                params: { animalId: animal.id }
            })
        },


        //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
        selectTab(tab) {
            this.activeTab = tab;
            if (tab === 'animais') {
                this.$router.push('/animais');
            }
        },

        preencheFormAnimal() {
            this.formDataAnimal.id = this.animal.id;
            this.formDataAnimal.brinco = this.animal.brinco;
            this.formDataAnimal.dataNascimento = this.animal.dataNascimento;
            this.formDataAnimal.piquete = this.animal.piquete.nome;
            this.formDataAnimal.sexo = this.animal.sexo;
            this.formDataAnimal.racaObservacao = this.animal.racaObservacao;
            this.formDataAnimal.brincoPai = this.animal.brincoPai;
            this.formDataAnimal.brincoMae = this.animal.brincoMae;
            this.formDataAnimal.status = this.animal.status;
            this.formDataAnimal.rfid = this.animal.rfid;
            this.formDataAnimal.observacoes = this.animal.observacoes;
            this.formDataAnimal.dataCompra = this.animal.dataCompra;
            this.formDataAnimal.valorCompra = this.animal.valorCompra;
            if (this.animal.racaPredominante) {
                this.formDataAnimal.racaPredominante = this.animal.racaPredominante.nome;
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

        excluirOcorrencia(ocorrenciaId) {
            this.ocorrenciaPraExclusao = ocorrenciaId;
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
.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  z-index: 0; /* Garante que a imagem de fundo fique na camada mais baixa */
}

.background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../assets/logo-sem-fundo.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}

nav, .tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
}

.table-container, .button-container {
  position: relative;
  z-index: 1; /* Garante que as tabelas e botões estejam acima da imagem de fundo */
}

.table-container {
    margin-left: 20px;
    margin-right: 20px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    z-index: 2;
}

.table-container table thead tr th {
    border-bottom: 2px solid #4CAF50;
    /* Adiciona uma borda verde na parte inferior */
    background-color: #f0f0f0;
}

.animal-view {
    padding: 20px;
    z-index: 1;
}

.actions {
    margin-top: 20px;
    margin-bottom: 20px;
    z-index: 1;
}

.actions button {
    margin-right: 10px;
    margin-top: 5px;
    margin-bottom: 5px;
    z-index: 1;
}

.actions .btn {
    width: 200px;
}

table {
    width: 100%;
    border-collapse: collapse;
    z-index: 1;
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

<template>
    <!-- Formulário de criação de propriedade -->
    <div>
        <div class="modal" id="listModal" tabindex="-1" role="dialog" style="display: block;">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Cadastrar Propriedade</h5>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitForm">
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
                                <input v-model="formData.nome" type="text" class="form-control" placeholder="Nome"
                                    id="nome">
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>
                                <input v-model="formData.endereco" type="text" class="form-control"
                                    placeholder="Endereço" id="endereco">
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-flag"></i></span>
                                <select v-model="formData.estado" class="form-select" required
                                    @change="buscarCidadesPorEstado($event.target.value)">
                                    <option value="" disabled>Selecione o estado</option>
                                    <option v-for="estado in estados" :key="estado.id" :value="estado.id">{{ estado.nome
                                        }}</option>
                                </select>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-city"></i></span>
                                <select v-model="formData.cidade" class="form-select" required>
                                    <option value="" disabled>Selecione a cidade</option>
                                    <option v-for="cidade in cidades" :key="cidade.id" :value="cidade.nome">{{
                            cidade.nome }}</option>
                                </select>
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-globe"></i></span>
                                <input v-model="formData.latitude" type="text" class="form-control"
                                    placeholder="Latitude" id="latitude">
                            </div>
                            <div class="mb-3 input-group">
                                <span class="input-group-text"><i class="fas fa-globe"></i></span>
                                <input v-model="formData.longitude" type="text" class="form-control"
                                    placeholder="Longitude" id="longitude">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="voltar()">Cancelar</button>
                        <button type="button" class="btn btn-primary" @click="submitForm">Enviar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import api from '/src/interceptadorAxios'

export default {
    data() {
        return {
            propriedades: [],
            estados: [],
            cidades: [],
            formData: {
                id: null,
                nome: '',
                endereco: '',
                estado: '',
                cidade: '',
                latitude: '',
                longitude: '',
                produtor: [],
            },
        };
    },
    mounted() {
        this.buscarEstadosDaApi();
    },



    methods: {

        async buscarCidadesPorEstado(estadoId) {
            try {
                const response = await axios.get(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`);
                this.cidades = response.data;
            } catch (error) {
                console.error('Erro ao buscar cidades da API:', error);
            }
        },


        async buscarEstadosDaApi() {
            try {
                const response = await axios.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome');
                this.estados = response.data;
            } catch (error) {
                console.error('Erro ao buscar cidades da API:', error);
            }
        },


        async submitForm() {
            try {
                const response = await api.post('http://127.0.0.1:8000/propriedades/', this.formData);

                if (response.status === 201) {
                    alert('Cadastro realizado com sucesso!');
                    this.resetForm();
                    this.buscarPropriedadesDaApi();
                } else {
                    alert('Erro ao cadastrar propriedade. Tente novamente mais tarde.');
                }
            } catch (error) {
                console.error('Erro ao enviar requisição:', error);
                alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
            }
            this.fecharModal("cadastroModal");
        },

        voltar() {
            this.$router.push('/inicio');
        },

    },
}
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.modal {
    display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
    position: relative;
    width: auto;
    margin: 10px auto;
}

.modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 0.3rem;
    outline: 0;
}

.modal-header {
    padding: 15px;
    border-bottom: 1px solid #e9ecef;
    border-top-left-radius: 0.3rem;
    border-top-right-radius: 0.3rem;
}

.modal-title {
    margin-bottom: 0;
    line-height: 1.5;
}

.modal-body {
    position: relative;
    flex: 1 1 auto;
    padding: 15px;
}

.modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 15px;
    border-top: 1px solid #e9ecef;
    border-bottom-right-radius: 0.3rem;
    border-bottom-left-radius: 0.3rem;
}
</style>
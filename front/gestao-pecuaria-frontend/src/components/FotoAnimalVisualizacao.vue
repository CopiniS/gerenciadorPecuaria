<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'animais' }" id="nav-animais-tab"
        @click="selectTab('animais')" type="button" role="tab" aria-controls="nav-animais"
        aria-selected="true">Lista de Animais</button>
        <button class="nav-link" :class="{ active: activeTab === 'visualizacao' }" id="nav-visualizacao-tab"
          @click="selectTab('visualizacao')" type="button" role="tab" aria-controls="nav-visualizacao" 
          aria-selected="true">Visualização do Animal</button>
        <button class="nav-link" :class="{ active: activeTab === 'visualizacao-foto' }" id="nav-visualizacao-foto-tab" @click="selectTab('visualizacao-foto')" 
        type="button" role="tab" aria-controls="nav-visualizacao-foto" aria-selected="false">Fotos do Animal</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'aplicacoes' }" id="nav-vet" role="tabpanel" aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'visualizacao-foto' }" id="nav-visualizacao-foto" role="tabpanel" aria-labelledby="nav-visualizacao-foto-tab">
        <div class="table-container" id="visualizacao-foto" tabindex="-1" aria-labelledby="visualizacao-fotoLabel" aria-hidden="true">
          <h1 class="title fs-5" id="visualizacao-fotoLabel">Fotos</h1>
          <h2 class="title fs-5" id="visualizacao-fotoLabel">Animal: {{ brinco }}</h2>

            <div class="carrosel">
                <div id="carouselExampleCaptions" class="carousel slide">
                        <div class="carousel-indicators">
                            <button v-for="(foto, index) in fotos" :key="index"
                                :data-bs-target="'#carouselExampleCaptions'" :data-bs-slide-to="index"
                                :class="{ 'active': index === 0 }" :aria-label="'Slide ' + (index + 1)"
                                :aria-current="index === 0 ? 'true' : ''"></button>
                        </div>
                        <div class="carousel-inner">
                            <div v-for="(foto, index) in fotos" :key="index"
                                :class="['carousel-item', { active: index === 0 }]">
                                <img :src="getImagePath(foto.foto)" class="d-block w-100"
                                    :alt="'Foto ' + (index + 1)">
                                <div class="carousel-caption d-none d-md-block">
                                    <h5>{{ foto.dataFoto }}</h5>
                                    <h6>Observação:</h6>
                                    <p>{{ foto.observacao }}</p>
                                </div>
                            </div>
                        </div>
                        <button class="carousel-control-prev" type="button"
                            data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Anterior</span>
                        </button>
                        <button class="carousel-control-next" type="button"
                            data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Próximo</span>
                        </button>
                    </div>
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
            activeTab: 'visualizacao-foto',  // Aba inicial é 'visualizacao-foto'
            brinco: null,
            fotos: null,
            animal: null,
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
        this.animal = animal[0].id;
        this.brinco = animal[0].brinco;
        
        this.buscarFotos();
      } catch (error) {
        console.error('Erro ao buscar animal da API:', error);
      }
    },

    async buscarFotos() {
        try {
            const response = await api.get('http://127.0.0.1:8000/fotos-animais/', {
                params: {
                    animalSelecionado: this.animal
                },
            });
            this.fotos = response.data;
            this.fotos = this.fotos.sort((a, b) => new Date(b.dataFoto) - new Date(a.dataFoto));
        } catch (error) {
            console.error('Erro ao buscar fotos da API:', error);
        }
    },
    
    async submitForm() {
      if (this.verificaVazio()) {
        try {
            const response = await api.post('http://127.0.0.1:8000/fotos-animais/', this.formData , {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
            if (response.status === 201) {
                alert('Cadastro realizado com sucesso!');
                this.selectTab('visualizacao');
            } else {
                alert('Erro ao cadastrar aplicacao. Tente novamente mais tarde.');
            }
        } catch (error) {
          console.error('Erro ao enviar requisição:', error);
          alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
        }
      } 
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
            params: { animalId: this.animal } 
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

    getImagePath(nomeArquivo) {
        return `http://127.0.0.1:8000${nomeArquivo}`;
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

.modal-body-visualizacao-foto {
    justify-content: center;
    margin-top: 20px;
}

.carrossel {
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

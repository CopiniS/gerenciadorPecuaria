<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <nav class="navbar bg-body-tertiary">
          <div class="container">
            <a class="navbar-brand" href="#">
              <img src="../assets/logo.png" alt="ifsc" width="30" height="40">
            </a>
          </div>
        </nav>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Propriedade
            </a>
            <ul class="dropdown-menu">
              <li class="nav-item"><a href="/propriedade">Editar Propriedade</a></li>
              <li class="nav-item"><a href="/propriedades">Trocar de Propriedade</a></li>
              <li class="nav-item"><a href="/cadastropropriedade">Cadastrar Propriedade</a></li>
              <li class="nav-item"><a href="/propriedade" @click.prevent="confirmarApagarPropriedade">Excluir
                  Propriedade</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                Compra
              </a>
              <ul class="dropdown-menu">
                <li class="nav-item"><a href="/CompraProdutoAlimenticios">Compra Produto Alimenticio</a></li>
                <li class="nav-item"><a href="/CompraProdutoSanitarios">Compra Produto Sanitario</a></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                Produtos
              </a>
              <ul class="dropdown-menu">
                <li class="nav-item"><a href="/ProdutosSanitarios">Produtos Sanitarios</a></li>
                <li class="nav-item"><a href="/ProdutosAlimenticios">Produtos Alimenticios</a></li>
              </ul>
            </li>
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/animais" class="dropdown-item">Animal</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/raca" class="dropdown-item">Raça</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/lotes" class="dropdown-item">Lotes</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/Veterinarios" class="dropdown-item">Veterinario</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/Pesagens" class="dropdown-item">Pesagens</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/Suplementacao" class="dropdown-item"> Suplementação</router-link>
            </li>
          </ul>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-user"></i> Perfil
            </a>
            <ul class="dropdown-menu">
              <li><a href="/meuperfil">Meu perfil</a></li>
              <li class="nav-item">
                <router-link to="#" class="dropdown-item" @click.prevent="confirmAction">Sair</router-link>
              </li>
            </ul>
          </li>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  name: 'NavbarComponent',
  data() {
    return {
      propriedade: null
    }
  },
  mounted() {
    const propriedadeSelecionada = localStorage.getItem('propriedadeSelecionada');
    if (propriedadeSelecionada) {
      this.buscarPropriedadeDaApi(propriedadeSelecionada);
    }
  },
  methods:{
    async buscarPropriedadeDaApi(propriedadeId) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/propriedades/${propriedadeId}/`);
        this.propriedade = response.data;
      } catch (error) {
        console.error('Erro ao buscar propriedade da API:', error);
      }
    },
    confirmarApagarPropriedade() {
      if (confirm("Você tem certeza que deseja excluir esta propriedade?")) {
        this.apagarPropriedade();
      }
    },
    async apagarPropriedade() {
      if (!this.propriedade) return;
      try {
        const response = await api.delete(`http://127.0.0.1:8000/propriedades/${this.propriedade.id}/`);
        if (response.status === 204) {
          alert('Propriedade apagada com sucesso!');
          localStorage.removeItem('propriedadeSelecionada');
          this.$router.push('/propriedades');
        } else {
          alert('Erro ao apagar propriedade. Tente novamente mais tarde.');
        }
      } catch (error) {
        console.error('Erro ao enviar requisição:', error);
        alert('Erro ao enviar requisição. Verifique o console para mais detalhes.');
      }
    },
    confirmAction() {
      if (confirm("Você tem certeza que deseja sair?")){
        this.fazLogout();
      }
    },
    async fazLogout(){
      localStorage.clear();
      this.$router.push('/login');  
    }
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
  white-space: nowrap; /* Impede a quebra de linha */
}

.perfil{
  position: relative;
}

.perfil-content a{
  display: block;
   
}
</style>

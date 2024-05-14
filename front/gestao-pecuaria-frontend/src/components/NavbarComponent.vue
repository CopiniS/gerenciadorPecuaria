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
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/propriedade" class="dropdown-item">Propriedade</router-link>
            </li>
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
              <router-link to="/ProdutosSanitarios" class="dropdown-item">Produtos Sanitarios</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/ProdutosAlimenticios" class="dropdown-item">Produtos Alimenticios</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/Pesagens" class="dropdown-item">Pesagens</router-link>
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

export default {
  name: 'NavbarComponent',
  
  methods:{
    confirmAction() {
      if (confirm("Você tem certeza que deseja sair?")){
        this.fazLogout();
      }
    },

    async fazLogout(){
      localStorage.clear;
      this.$router.push('/login');  
    }
  }
}
</script>

<style scoped>
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
}

.perfil{
  position: relative;
}

.perfil-content a{
  display: block;
   
}
</style>

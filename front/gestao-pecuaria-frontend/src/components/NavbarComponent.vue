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
          </ul>
          <div class="perfil">
            <img src="../assets/perfil.png" alt="Menu" width="40" height="40">
            <div class="perfil-content">
              <ul>
                <li href="#">Meu perfil</li>
                <li class="nav-item">
                  <router-link to="#" class="dropdown-item" @click.prevent="confirmAction">Sair</router-link>
                </li>
              </ul>
            </div>
          </div>
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

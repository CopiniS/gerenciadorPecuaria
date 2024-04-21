<template>
  <div id="app">
    <NavbarComponent v-if="notIsLoginAndCadastroPage" />

    <LoginView v-if="isLoginPage" />

    <Cadastro v-if="isCadastroPage" />

  </div>
</template>

<script>
import NavbarComponent from './components/NavbarComponent.vue'
import LoginView from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'

export default {
  name: 'App',
  components: {
    NavbarComponent,
    LoginView,
    Cadastro
  },
  computed: {
    notIsLoginAndCadastroPage() {
      return this.$route.name !== "login" && this.$route.name !== "cadastro";
    },
    isLoginPage() {
      return this.$route.name === "login";
    },
    isCadastroPage() {
      return this.$route.name === "cadastro";
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>

<template>
  <div id="app">
    <NavbarComponent v-if="notIsLoginAndCadastroPage" />

    <PopUpPropriedade v-if="isPropriedadePage"/>

    <CadastroPropriedade v-if="isCadastroPropriedadePage"/>

    <LoginView v-if="isLoginPage" />

    <Cadastro v-if="isCadastroPage" />

  </div>
</template>

<script>
import NavbarComponent from './components/NavbarComponent.vue'
import LoginView from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import PopUpPropriedade from './views/PopUpPropriedade.vue';
import CadastroPropriedade from './components/CadastroPropriedade.vue';

export default {
  name: 'App',
  components: {
    NavbarComponent,
    LoginView,
    Cadastro, 
    PopUpPropriedade,
    CadastroPropriedade
  },
  computed: {
    notIsLoginAndCadastroPage() {
      return this.$route.name !== "login" && this.$route.name !== "cadastro" && this.$route.name !== "PopUpPropriedade" && this.$route.name !== "CadastroPropriedade";
    },
    isLoginPage() {
      return this.$route.name === "login";
    },
    isCadastroPage() {
      return this.$route.name === "cadastro";
    },
    isPropriedadePage() {
      return this.$route.name === "PopUpPropriedade";
    },
    isCadastroPropriedadePage() {
      return this.$route.name === "CadastroPropriedade";
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

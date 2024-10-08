<template>
  <div class="background">
    <h1>Bem vindo</h1>
  </div>
    
</template>

<script>

export default {
  name: 'InicialView',
}
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
  /* opacity: 0.1; */
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}


</style>
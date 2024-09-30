<template>
<div class="skeleton-container">
    <div class="d-flex align-items-start table-container flex-column">
        <div class="d-flex align-items-start mb-3">
            <h2 class="me-3">Filtros</h2>
            <button class="btn-acoes btn-sm" @click="toggleFormulario">
                <i class="fas fa-chevron-down"></i>
            </button>
        </div>
    </div>       

    <div class="table-container">
        <div class="button-container">
            <button type="button" class="btn btn-success"></button>
            <button type="button" class="btn btn-success"></button>
        </div>
        <table class="table">
            <thead>
            <tr>
                <th><div class="skeleton-header"></div></th>
                <th><div class="skeleton-header"></div></th>
                <th><div class="skeleton-header"></div></th>
                <th><div class="skeleton-header"></div></th>
                <th><div class="skeleton-header"></div></th>
                <th><div class="skeleton-header"></div></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="n in 5" :key="n">
                <td><div class="skeleton-row"></div></td>
                <td><div class="skeleton-row"></div></td>
                <td><div class="skeleton-row"></div></td>
                <td><div class="skeleton-row"></div></td>
                <td><div class="skeleton-row"></div></td>
                <td><div class="skeleton-row"></div></td>
            </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
export default {
  name: 'SkeletonGastos',
};
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

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
  background-image: url("../assets/logo-sem-fundo.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 40%;
  opacity: 0.1;
  z-index: 0; /* A imagem de fundo deve estar abaixo do conteúdo */
}

nav,
.tab-content {
  position: relative;
  z-index: 1; /* Coloca o conteúdo acima da marca d'água */
}

.table-container,
.button-container {
  position: relative;
  z-index: 1; /* Garante que as tabelas e botões estejam acima da imagem de fundo */
}

/* Estilo do botão de ação */
.btn-success {
  width: 120px; /* Largura dos botões */
  height: 40px; /* Altura dos botões */
  background: linear-gradient(-90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
  background-size: 400% 400%;
  border: none;
  border-radius: 4px;
  animation: skeleton-loading 1.2s ease-in-out infinite;
  color: transparent; /* Torna o texto invisível */
  cursor: not-allowed; /* Indica que o botão está desabilitado */
}

.btn-acoes {
  background-color: transparent;
  border: none;
  padding: 0;
  z-index: 2; /* Garante que o botão de ação esteja acima da imagem */
}

.btn-acoes i {
  color: #176d1a;
}

/* Estilo do contêiner de botões */
.button-container {
  display: flex;
  gap: 10px; /* Espaçamento entre os botões */
  margin-bottom: 20px;
  white-space: nowrap;
}

/* Estilo do contêiner da tabela */
.table-container {
  background-color: transparent !important;
}

/* Estilo para cabeçalho da tabela */
.table-container table thead tr th {
  border-bottom: 2px solid #176d1a; /* Adiciona uma borda verde na parte inferior */
  background-color: transparent !important;
}

/* Estilo do skeleton para os filtros */
.skeleton-filter {
  width: 250px; /* Largura do filtro */
  height: 20px; /* Altura do filtro */
  background: linear-gradient(-90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
  background-size: 400% 400%;
  animation: skeleton-loading 1.2s ease-in-out infinite;
  border-radius: 4px; /* Borda arredondada */
  margin-bottom: 10px; /* Espaçamento entre os filtros */
}

/* Estilo do cabeçalho da tabela */
.skeleton-header {
  width: 100px; /* Largura do cabeçalho */
  height: 20px; /* Altura do cabeçalho */
  background: linear-gradient(-90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
  background-size: 400% 400%;
  animation: skeleton-loading 1.2s ease-in-out infinite;
  border-radius: 4px; /* Borda arredondada */
}

/* Estilo da linha da tabela */
.skeleton-row {
  height: 20px; /* Altura da linha */
  background: linear-gradient(-90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
  background-size: 400% 400%;
  animation: skeleton-loading 1.2s ease-in-out infinite;
  border-radius: 4px; /* Borda arredondada */
  margin: 10px 0; /* Espaçamento vertical entre as linhas */
}

/* Animação de carregamento */
@keyframes skeleton-loading {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}
</style>

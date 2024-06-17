<template>
  <div>
    <nav class="navbar navbar-dark bg-dark fixed-top custom-navbar">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <a class="navbar-brand" href="#">Nome da Aplicação</a>
        <a class="navbar-brand" href="#">Propriedade atual: {{ nomeProp }}</a>
        <div class="offcanvas offcanvas-start text-bg-dark custom-offcanvas justify-content-center" tabindex="-1" id="offcanvasDarkNavbar" aria-labelledby="offcanvasDarkNavbarLabel">
          <div class="offcanvas-header">
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-center flex-grow-1 pe-3">
              <li class="nav-item">
                <a href="/inicio" class="nav-link"><i class="fas fa-home"></i> Home</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/meuperfil" class="nav-link"><i class="fas fa-user"></i> Perfil</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fas fa-landmark"></i> Propriedade
                </a>
                <ul class="dropdown-menu justify-content-center">
                  <li><a class="dropdown-item" href="/propriedade"><i class="fas fa-edit"></i> Editar Propriedade</a></li>
                  <hr class="custom-hr">
                  <li><a class="dropdown-item" href="/propriedades"><i class="fas fa-exchange-alt"></i> Trocar de Propriedade</a></li>
                  <hr class="custom-hr">
                  <li><a class="dropdown-item" href="/cadastropropriedade"><i class="fas fa-plus"></i> Cadastrar Propriedade</a></li>
                  <hr class="custom-hr">
                  <li><a class="dropdown-item" href="/propriedade" @click.prevent="confirmarApagarPropriedade"><i class="fas fa-trash-alt"></i> Excluir Propriedade</a></li>
                </ul>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/compraprodutos" class="nav-link"><i class="fas fa-box"></i> Compra de produtos</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/produtos" class="nav-link"><i class="fas fa-box"></i> Produtos</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/animais" class="nav-link"><i class="fas fa-paw"></i> Animais</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/raca" class="nav-link"><i class="fas fa-dna"></i> Raças</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/piquetes" class="nav-link"><i class="fas fa-layer-group"></i> Piquetes</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/Veterinarios" class="nav-link"><i class="fas fa-user-md"></i> Veterinarios</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/Pesagens" class="nav-link"><i class="fas fa-weight"></i> Pesagens</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/Suplementacao" class="nav-link"><i class="fas fa-prescription-bottle-alt"></i> Suplementações</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/aplicacoes-produtos" class="nav-link"><i class="fas fa-syringe"></i> Aplicações de Produtos</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/vendas-animais" class="nav-link"><i class="fas fa-calculator"></i> Vendas de animais</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/inseminacoes" class="nav-link"><i class="fas fa-capsules"></i> Inseminações</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/outras-despesas" class="nav-link"><i class="fas fa-money-bill-wave"></i> Outras Despesas</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/Movimentacoes" class="nav-link"><i class="fas fa-cogs"></i>Movimentacoes</a>
              </li>
              <hr class="custom-hr">
              <li class="nav-item">
                <a href="/login" class="nav-link"><i class="fas fa-sign-out-alt"></i> Sair</a>
              </li>
              <hr class="custom-hr">
            </ul>
          </div>
        </div>
      </div>
    </nav>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import api from '/src/interceptadorAxios';

export default {
  name: 'NavbarComponent',
  data() {
    return {
      propriedade: [],
      nomeProp: null,
    }
  },
  mounted() {
    const propriedadeSelecionada = localStorage.getItem('propriedadeSelecionada');
    if (propriedadeSelecionada) {
      this.buscarPropriedadeDaApi(propriedadeSelecionada);
    }
  },
  methods: {
    async buscarPropriedadeDaApi(propriedadeId) {
      try {
        const response = await api.get(`http://127.0.0.1:8000/propriedades/${propriedadeId}/`);
        this.propriedade = response.data;
        this.nomeProp = this.propriedade.nome;
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
      if (confirm("Você tem certeza que deseja sair?")) {
        this.fazLogout();
      }
    },
    async fazLogout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0px;
}

a {
  color: #cfcfcf !important; /* Tom de cinza claro para o texto */
  white-space: nowrap; /* Impede a quebra de linha */
  font-size: 1.1em; /* Aumenta o tamanho da letra */
}


.nav-item .dropdown-item {
  display: flex;
  align-items: center;
  font-size: 1em;
  justify-content: center;
}

.nav-item .dropdown-item i {
  margin-right: 8px; /* Espaço entre o ícone e o texto */
}

.dropdown-menu {
  background-color: #252525 !important; /* Fundo cinza escuro para o dropdown */
  border: none; /* Remove a borda do dropdown */
}

.dropdown-item:hover {
  background-color: #3a3a3a !important; /* Fundo cinza mais claro no hover */
  color: #cfcfcf !important; /* Cor do texto no hover */
}

.nav-item:hover {
  background-color: #3a3a3a !important; /* Fundo cinza mais claro no hover */
  color: #cfcfcf !important; /* Cor do texto no hover */
}

.custom-offcanvas {
  width: 350px !important; /* Largura personalizada para o menu lateral */
}

.custom-hr {
  border-color: black; /* Cor preta para as linhas hr */
}

.custom-close {
  color: black; /* Cor preta para o botão de fechar */
  opacity: 1; /* Garantir que o botão esteja totalmente opaco */
}


/* Personaliza a barra de rolagem */
::-webkit-scrollbar {
  width: 8px; /* Largura da barra de rolagem */
  height: 8px; /* Altura da barra de rolagem horizontal */
}

/* Fundo da barra de rolagem */
::-webkit-scrollbar-track {
  background: #252525; /* Cor do fundo da barra de rolagem */
}

/* Cor da barra de rolagem */
::-webkit-scrollbar-thumb {
  background-color: #101010; /* Cor da barra de rolagem */
  border-radius: 10px; /* Bordas arredondadas */
  border: 2px solid #252525; /* Adiciona uma borda */
}

/* Barra de rolagem ao passar o mouse */
::-webkit-scrollbar-thumb:hover {
  background: #575656; /* Cor da barra de rolagem ao passar o mouse */
}

/* Adiciona margem superior ao conteúdo para evitar sobreposição com o navbar */
.content {
  margin-top: 50px;
}
</style>



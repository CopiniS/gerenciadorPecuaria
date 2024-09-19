<template>
  <div class="background">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button class="nav-link" :class="{ active: activeTab === 'meu-perfil' }" id="nav-vet-tab"
          @click="selectTab('meu-perfil')" type="button" role="tab" aria-controls="nav-vet" aria-selected="true">Meu Perfil
            </button>
        <button class="nav-link" :class="{ active: activeTab === 'trocar-senha' }" id="nav-cadastro-tab"
          @click="selectTab('trocar-senha')" type="button" role="tab" aria-controls="nav-cadastro"
          aria-selected="false">Trocar Senha</button>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'meu-perfil' }" id="nav-vet" role="tabpanel"
        aria-labelledby="nav-vet-tab">
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'trocar-senha' }" id="nav-cadastro" role="tabpanel"
        aria-labelledby="nav-cadastro-tab">
        <div class="table-container" id="cadastro" tabindex="-1" aria-labelledby="cadastroLabel" aria-hidden="true">
          <h1 class="title fs-5" id="cadastroLabel">Trocar senha</h1>
          <form @submit.prevent="submitForm">
              <div class="mb-4 input-group">
                <span class="input-group-text"
                  ><i class="fas fa-lock"></i
                ></span>
                <input
                  v-model="formData.password"
                  :type="passwordType"
                  class="form-control"
                  :class="{ 'is-invalid': !isPasswordValido }"
                  id="password"
                  :placeholder="passwordPlaceholder"
                />
                <span
                  class="input-group-text"
                  @click="togglePasswordVisibility"
                >
                  <i
                    :class="
                      passwordType === 'password'
                        ? 'fas fa-eye'
                        : 'fas fa-eye-slash'
                    "
                  ></i>
                </span>
              </div>

              <div class="mb-4 input-group">
                <span class="input-group-text"
                  ><i class="fas fa-lock"></i
                ></span>
                <input
                  v-model="formData.confirm_password"
                  :type="confirmPasswordType"
                  class="form-control"
                  :class="{ 'is-invalid': !isConfirmPasswordValido }"
                  id="confirmPassword"
                  :placeholder="confirmPasswordPlaceholder"
                />
                <span
                  class="input-group-text"
                  @click="toggleConfirmPasswordVisibility"
                >
                  <i
                    :class="
                      confirmPasswordType === 'password'
                        ? 'fas fa-eye'
                        : 'fas fa-eye-slash'
                    "
                  ></i>
                </span>
              </div>
              <div class="button-group justify-content-end">
                <button type="button" class="btn btn-secondary" @click="selectTab('meu-perfil')">
                  Cancelar
                </button>
                <button
                  type="submit"
                  class="btn btn-success"
                >
                  Enviar
                </button>
              </div>
            </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "/src/interceptadorAxios";
import { masksMixin } from "../mixins/maks";

export default {
  mixins: [masksMixin],

  data() {
    return {
      activeTab: "trocar-senha",
      formData: {
        new_password: null,
        confirm_password: null,
      },
      isPasswordValido: true,
      isConfirmPasswordValido: true,
      passwordPlaceholder: "Nova Senha",
      passwordType: "password", // Controla o tipo do input da senha
      confirmPasswordPlaceholder: "Repita a Senha",
      confirmPasswordType: "confirmPassword",
    };
  },

  methods: {

    //REQUISIÇÕES AO BANCO DE DADOS---------------------------------------------------------------------------------------------------------------------
    async submitForm() {
      if (this.verificaVazio()) {
        try {
          const response = await api.post(
            "http://127.0.0.1:8000/alterar-senha/",
            this.formData
          );
          if (response.status === 200) {
            alert("Senha alterada com sucesso!");
            this.selectTab('meu-perfil')
          } else {
            alert("Erro ao alterar a senha. Tente novamente mais tarde.");
          }
        } catch (error) {
          console.error("Erro ao enviar requisição:", error);
          alert(
            "Erro ao enviar requisição. Verifique o console para mais detalhes."
          );
        }
      }
    },

    //VALIDAÇÕES-------------------------------------------------------------------------------------------------------------------------------------------------------------

    verificaVazio() {
      //PASSWORD
      if (this.formData.password != null && this.formData.password != "") {
        this.isPasswordValido = true;
        this.passwordPlaceholder = "Nova Senha*";
      } else {
        this.isPasswordValido = false;
        this.passwordPlaceholder = "Nova Senha é um Campo Obrigatório";
      }

      return (
        this.isPasswordValido
      );
    },

    //FUNÇÕES AUXILIARES----------------------------------------------------------------------------------------------------------------------------------------------------------
    selectTab(tab) {
      this.activeTab = tab;
      if (tab === 'meu-perfil') {
        this.$router.push('/meuperfil');
      }
    },

    togglePasswordVisibility() {
      this.passwordType =
        this.passwordType === "password" ? "text" : "password";
    },

    toggleConfirmPasswordVisibility() {
      this.confirmPasswordType =
        this.confirmPasswordType === "password" ? "text" : "password";
    },
  },
};
</script>



<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.background {
  background-color: #ededef;
  min-height: 100vh;
  padding: 20px;
}

.nav-link.active {
  background-color: #d0d0d0 !important;
}

.table-container {
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.button-container {
  text-align: left;
  margin-bottom: 20px;
}

.table-container table tbody tr td {
  background-color: #ededef !important;
}

.table-container table thead tr th {
  border-bottom: 2px solid #176d1a;
  background-color: #f0f0f0;
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

.is-invalid {
  border-color: #dc3545;
}
#legenda {
  font-size: 16px;
}
</style>

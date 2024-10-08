<template>
  <div class="login-container">
    <div class="login-content">
      <!-- Div para a logo -->
      <div class="logo-section">
        <img src="@/assets/logo-sem-fundo.png" alt="Logo" class="logo-img" />
      </div>

      <form @submit.prevent="submitForm">
        <div class="mb-4 input-group">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
          <input v-model="email" type="email" class="form-control" id="email" placeholder="Email" required>
        </div>
        <div class="mb-4 input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input v-model="password" :type="passwordType" class="form-control" id="password" placeholder="Senha" required>
          <span class="input-group-text" @click="togglePasswordVisibility">
            <i :class="passwordType === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
          </span>
        </div>

        <div class="text-right mb-3">
          <a href="#" data-bs-toggle="modal" data-bs-target="#recuperarSenhaModal">Esqueceu sua senha?</a>
        </div>

        <button type="button" class="btn btn-primary btn-block" @click="login">
          <i class="fas fa-sign-in-alt"></i> Entrar
        </button>

          <button type="button" class="btn btn-primary btn-block" @click="login">
            <i class="fas fa-sign-in-alt"></i> Entrar
          </button>

          <hr>

          <button type="button" class="btn btn-outline-secondary btn-block" @click="registrar">
            <i class="fas fa-user-plus"></i> Não tenho conta
          </button>
        </form>
      </div>
    </div>

    <!-- Modal de Recuperação de Senha -->
    <div class="modal fade" id="recuperarSenhaModal" tabindex="-1" aria-labelledby="recuperarSenhaModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="recuperarSenhaModalLabel">Recuperar Senha</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="recuperacaoMessage" :class="`alert ${recuperacaoMessageType}`">{{ recuperacaoMessage }}</div>
            <form @submit.prevent="enviarRecuperacaoSenha">
              <div class="mb-4 input-group">
                <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                <input v-model="emailRecuperacao" type="email" class="form-control" id="emailRecuperacao" placeholder="Digite seu email" required>
              </div>

              <button type="submit" class="btn btn-primary btn-block">
                <i class="fas fa-paper-plane"></i> Enviar link de recuperação
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal } from 'bootstrap';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      emailRecuperacao: '',
      recuperacaoMessage: '',
      recuperacaoMessageType: '',
      emailRecuperacaoValido: false,
      verificandoEmail: false,
      passwordType: 'password',
    };
  },
  methods: {
    async login() {
      this.errorMessage = '';

      try {
        const response = await axios.post('http://127.0.0.1:8000/token/', {
          email: this.email,
          password: this.password
        });

        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        const nome = await this.retornaNomeProdutor();
        localStorage.setItem('produtorNome', nome);

        this.$router.push('/propriedades-escolha');
        
      } catch (error) {
        this.errorMessage = 'Email ou senha incorretos.';
      }
    },
    registrar() {
      this.$router.push('/cadastro');
    },
    async retornaNomeProdutor() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/meuperfil/');
        return response.data.nome;
      } catch (error) {
        console.error('Erro ao buscar propriedades da API:', error);
        return '';
      }
    },
    togglePasswordVisibility() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
    },
    async verificarEmailRecuperacao() {
      if (!this.emailRecuperacao || this.verificandoEmail) return;
      
      this.verificandoEmail = true;
      this.recuperacaoMessage = '';
      this.emailRecuperacaoValido = false;

      try {
        const response = await axios.post('http://127.0.0.1:8000/verificar-email/', {
          email: this.emailRecuperacao
        });

        if (response.data.existe) {
          this.recuperacaoMessage = 'Email encontrado! Você pode prosseguir com a recuperação.';
          this.recuperacaoMessageType = 'alert-success';
          this.emailRecuperacaoValido = true;
        } else {
          this.recuperacaoMessage = 'Email não cadastrado. Por favor, verifique o email digitado.';
          this.recuperacaoMessageType = 'alert-danger';
          this.emailRecuperacao = ''; // Limpa o campo de email
          this.emailRecuperacaoValido = false;
        }
      } catch (error) {
        this.recuperacaoMessage = 'Erro ao verificar email. Tente novamente.';
        this.recuperacaoMessageType = 'alert-danger';
        this.emailRecuperacaoValido = false;
      } finally {
        this.verificandoEmail = false;
      }
    },
    async enviarRecuperacaoSenha() {
      await this.verificarEmailRecuperacao();

      if (!this.emailRecuperacaoValido) {
        this.recuperacaoMessage = 'Por favor, verifique o email antes de continuar.';
        this.recuperacaoMessageType = 'alert-warning';
        return;
      }

      try {
        await axios.post('http://127.0.0.1:8000/recuperar-senha/', {
          email: this.emailRecuperacao
        });

        this.recuperacaoMessage = 'Se este email estiver registrado, você receberá um link de recuperação.';
        this.recuperacaoMessageType = 'alert-success';
        
        this.emailRecuperacao = '';
        this.emailRecuperacaoValido = false;

        setTimeout(() => {
          const modal = Modal.getInstance(document.getElementById('recuperarSenhaModal'));
          if (modal) {
            modal.hide();
          }
        }, 3000);
      } catch (error) {
        this.recuperacaoMessage = 'Erro ao enviar email de recuperação. Tente novamente.';
        this.recuperacaoMessageType = 'alert-danger';
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.login-form {
  background: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.title-login {
  font-size: 24px;
  font-weight: bold;
  color: #343a40;
}

.btn-block {
  width: 100%;
  padding: 10px;
}

.alert-custom {
  font-size: 14px;
}

.text-right {
  text-align: right;
}

.modal-body .alert {
  margin-bottom: 15px;
}

.modal-content {
  padding: 20px;
}
</style>


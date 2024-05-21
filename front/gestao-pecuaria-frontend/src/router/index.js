import { createRouter, createWebHistory } from 'vue-router';
import TelaAnimais from '@/views/TelaAnimais.vue';
import TelaPropriedade from '@/views/TelaPropriedade.vue';
import TelaRaca from '@/views/TelaRaca.vue';
import Login from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import PopUpPropriedade from '@/views/PopUpPropriedade.vue'
import TelaLotes from '@/views/TelaLotes.vue';
import CadastroPropriedade from '@/components/CadastroPropriedade.vue';
import InicialView from '@/views/InicialView.vue';
import PerfilProdutor from '@/components/PerfilProdutor.vue';
import TelaVeterinarios from '@/views/TelaVeterinarios.vue';
import TelaProdutosSanitarios from '@/views/TelaProdutosSanitarios.vue';
import TelaProdutosAlimenticios from '@/views/TelaProdutosAlimenticios.vue';
import TelaPesagens from '@/views/TelaPesagens.vue';
import TelaCompraProdutosAlimenticios from '@/views/TelaCompraProdutosAlimenticios.vue';
import TelaCompraProdutosSanitarios from '@/views/TelaCompraProdutosSanitarios.vue';
import TelaSuplementacao from '@/views/TelaSuplementacao.vue';

const routes = [
  
  {
    path: '/cadastro',
    name: 'cadastro',
    component: Cadastro, 
  },
  {
    path: '/login',
    name: 'login',
    component: Login, 
  },
  {
    path: '/',
    redirect: '/login' 
  }, 
  {
    path: '/inicio',
    name: 'inicio',
    component: InicialView, 
  },
  {
    path: '/propriedades',
    name: 'PopUpPropriedade',
    component: PopUpPropriedade, 
  },
  {
    path: '/propriedade',
    name: 'TelaPropriedade',
    component: TelaPropriedade, 
  },
  {
    path: '/cadastropropriedade',
    name: 'CadastroPropriedade',
    component: CadastroPropriedade, 
  },
  {
    path: '/animais',
    name: 'TelaAnimais',
    component: TelaAnimais, 
  },
  {
    path: '/raca',
    name: 'TelaRaca',
    component: TelaRaca, 
  },
  {
    path: '/lotes',
    name: 'TelaLotes',
    component: TelaLotes, 
  },
  {
    path: '/meuperfil',
    name: 'PerfilProdutor',
    component: PerfilProdutor, 
  },
  {
    path: '/Veterinarios',
    name: 'TelaVeterinarios',
    component: TelaVeterinarios, 
  },
  {
    path: '/ProdutosSanitarios',
    name: 'TelaProdutosSanitarios',
    component: TelaProdutosSanitarios, 
  },
  {
    path: '/ProdutosAlimenticios',
    name: 'TelaProdutosAlimenticios',
    component: TelaProdutosAlimenticios, 
  },
  {
    path: '/Pesagens',
    name: 'TelaPesagens',
    component: TelaPesagens 
  },
  {
    path: '/CompraProdutoAlimenticios',
    name: 'TelaCompraProdutosAlimenticios',
    component: TelaCompraProdutosAlimenticios 
  },
  {
    path: '/CompraProdutoSanitarios',
    name: 'TelaCompraProdutosSanitarios',
    component: TelaCompraProdutosSanitarios
  },
  {
    path: '/Suplementacao',
    name: 'TelaSuplementacao',
    component: TelaSuplementacao
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

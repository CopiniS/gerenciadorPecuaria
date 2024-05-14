import { createRouter, createWebHistory } from 'vue-router';
import TelaAnimais from '@/views/TelaAnimais.vue';
import TelaPropriedade from '@/views/TelaPropriedade.vue';
import TelaRaca from '@/views/TelaRaca.vue';
import Login from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import PopUpPropriedade from '@/views/PopUpPropriedade.vue'
import TelaLotes from '@/views/TelaLotes.vue';
import TelaVeterinarios from '@/views/TelaVeterinarios.vue';
import TelaProdutosSanitarios from '@/views/TelaProdutosSanitarios.vue';
import TelaProdutosAlimenticios from '@/views/TelaProdutosAlimenticios.vue';
import TelaPesagens from '@/views/TelaPesagens.vue';
import PerfilProdutor from '@/components/PerfilProdutor.vue';

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
  
  

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

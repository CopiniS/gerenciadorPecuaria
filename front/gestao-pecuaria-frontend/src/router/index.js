import { createRouter, createWebHistory } from 'vue-router';
import TelaAnimais from '@/views/TelaAnimais.vue';
import TelaPropriedade from '@/views/TelaPropriedade.vue';
import TelaRaca from '@/views/TelaRaca.vue';
import TelaCidade from '@/views/TelaCidade.vue';
import Login from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import TelaLotes from '@/views/TelaLotes.vue';

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
    path: '/cidade',
    name: 'TelaCidade',
    component: TelaCidade, 
  },
  {
    path: '/lotes',
    name: 'TelaLotes',
    component: TelaLotes, 
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

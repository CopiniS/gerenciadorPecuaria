import { createRouter, createWebHistory } from 'vue-router';
import TelaAnimais from '@/views/TelaAnimais.vue';
import TelaPropriedade from '@/views/TelaPropriedade.vue';
import TelaRaca from '@/views/TelaRaca.vue';
import Login from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import PopUpPropriedade from '@/views/PopUpPropriedade.vue'
import TelaPiquetes from '@/views/TelaPiquetes.vue';
import CadastroPropriedade from '@/components/CadastroPropriedade.vue';
import InicialView from '@/views/InicialView.vue';
import PerfilProdutor from '@/components/PerfilProdutor.vue';
import TelaVeterinarios from '@/views/TelaVeterinarios.vue';
import TelaProdutos from '@/views/TelaProdutos.vue';
import TelaPesagens from '@/views/TelaPesagens.vue';
import TelaCompraProdutos from '@/views/TelaCompraProdutos.vue';
import TelaSuplementacao from '@/views/TelaSuplementacao.vue';
import TelaAplicacoesProdutos from '@/views/TelaAplicacoesProdutos.vue'
import TelaVendasAnimais from '@/views/TelaVendasAnimais.vue'
import TelaInseminacoes from '@/views/TelaInseminacoes.vue'
import TelaOutrasDespesas from '@/views/TelaOutrasDespesas.vue'
import ViewAnimal from '@/views/ViewAnimal.vue';
import TelaMovimentacoes from '@/views/TelaMovimentacoes.vue';
import VeterinarioCadastro from '@/components/VeterinarioCadastro.vue';
import VeterinarioEdicao from '@/components/VeterinarioEdicao.vue';
import OutraDespesaEdicao from '@/components/OutraDespesaEdicao.vue';
import OutraDespesaCadastro from '@/components/OutraDespesaCadastro.vue';

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
    path: '/piquetes',
    name: 'TelaPiquetes',
    component: TelaPiquetes, 
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
    path: '/produtos',
    name: 'TelaProdutos',
    component: TelaProdutos, 
  },
  {
    path: '/Pesagens',
    name: 'TelaPesagens',
    component: TelaPesagens 
  },
  {
    path: '/compraprodutos',
    name: 'TelaCompraProdutos',
    component: TelaCompraProdutos
  },
  {
    path: '/Suplementacao',
    name: 'TelaSuplementacao',
    component: TelaSuplementacao
  },
  {
    path: '/aplicacoes-produtos',
    name: 'TelaAplicacoesProdutos',
    component: TelaAplicacoesProdutos
  },
  {
    path: '/vendas-animais',
    name: 'TelaVendasAnimais',
    component: TelaVendasAnimais
  },
  {
    path: '/inseminacoes',
    name: 'TelaInseminacoes',
    component: TelaInseminacoes
  },
  {
    path: '/vizualizarAnimal',
    name: 'VizualizarAnimal',
    component: ViewAnimal
  },
  {
    path: '/Movimentacoes',
    name: 'TelaMovimentacoes',
    component: TelaMovimentacoes
  },
  {
    path: '/cadastroVeterinario',
    name: 'CadastroVeterinario',
    component: VeterinarioCadastro
  },
  {
    path: '/editarVeterinario',
    name: 'EdicaoVeterinario',
    component: VeterinarioEdicao
  },

  {
    path: '/outras-despesas',
    name: 'TelaOutrasDespesas',
    component: TelaOutrasDespesas,
  },

  {
    path: '/editar-despesa/:despesaId',
    name: 'EdicaoDespesa',
    component: OutraDespesaEdicao,
    props: true
  },

  {
    path: '/cadastrar-despesa',
    name: 'CadastroDespesa',
    component: OutraDespesaCadastro
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import TelaAnimais from '@/views/TelaAnimais.vue';
import TelaPropriedade from '@/views/TelaPropriedade.vue';
import TelaRaca from '@/views/TelaRaca.vue';
import RacaCadastro from '@/components/RacaCadastro.vue';
import RacaEdicao from '@/components/RacaEdicao.vue';
import Login from '@/views/LoginView.vue'
import Cadastro from '@/views/CadastroView.vue'
import PopUpPropriedade from '@/views/PopUpPropriedade.vue'
import TelaPiquetes from '@/views/TelaPiquetes.vue';
import PropriedadeCadastro from '@/components/PropriedadeCadastro.vue';
import PropriedadeEdicao from '@/components/PropriedadeEdicao.vue';
import InicialView from '@/views/InicialView.vue';
import PerfilProdutor from '@/components/PerfilProdutor.vue';
import TelaVeterinarios from '@/views/TelaVeterinarios.vue';
import TelaProdutos from '@/views/TelaProdutos.vue';
import ProdutoCadastro from '@/components/ProdutoCadastro.vue'
import ProdutoEdicao from '@/components/ProdutoEdicao.vue'
import TelaPesagens from '@/views/TelaPesagens.vue';
import TelaCompraProdutos from '@/views/TelaCompraProdutos.vue';
import CompraProdutoCadastro from '@/components/CompraProdutoCadastro.vue';
import CompraProdutoEdicao from '@/components/CompraProdutoEdicao.vue';
import TelaSuplementacao from '@/views/TelaSuplementacao.vue';
import SuplementacaoCadastro from '@/components/SuplementacaoCadastro.vue';
import SuplementacaoEdicao from '@/components/SuplementacaoEdicao.vue';
import SuplementacaoFinalizacao from '@/components/SuplementacaoFinalizacao.vue';
import TelaAplicacoesProdutos from '@/views/TelaAplicacoesProdutos.vue'
import TelaVendasAnimais from '@/views/TelaVendasAnimais.vue';
import VendaAnimalCadastro from '@/components/VendaAnimalCadastro.vue';
import VendaAnimalEdicao from '@/components/VendaAnimalEdicao.vue';
import VendaAnimalVisualizacao from '@/components/VendaAnimalVisualizacao.vue';
import TelaInseminacoes from '@/views/TelaInseminacoes.vue'
import TelaOutrasDespesas from '@/views/TelaOutrasDespesas.vue'
import ViewAnimal from '@/views/ViewAnimal.vue';
import TelaMovimentacoes from '@/views/TelaMovimentacoes.vue';
import MovimentacaoCadastro from '@/components/MovimentacaoCadastro.vue';
import MovimentacaoEdicao from '@/components/MovimentacaoEdicao.vue';
import MovimentacaoVisualizacao from '@/components/MovimentacaoVisualizacao.vue';
import VeterinarioCadastro from '@/components/VeterinarioCadastro.vue';
import VeterinarioEdicao from '@/components/VeterinarioEdicao.vue';
import OutraDespesaEdicao from '@/components/OutraDespesaEdicao.vue';
import OutraDespesaCadastro from '@/components/OutraDespesaCadastro.vue';
import PiqueteCadastro from '@/components/PiqueteCadastro.vue';
import PiqueteEdicao from '@/components/PiqueteEdicao.vue';
import AnimaisCadastro from '@/components/AnimaisCadastro.vue';
import AnimaisEdicao from '@/components/AnimaisEdicao.vue';
import AplicacoesProdutosCadastro from '@/components/AplicacoesProdutosCadastro.vue';
import AplicacoesProdutosEdicao from '@/components/AplicacoesProdutosEdicao.vue';

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
    path: '/propriedades-escolha',
    name: 'PopUpPropriedade',
    component: PopUpPropriedade, 
  },
  {
    path: '/propriedades',
    name: 'TelaPropriedade',
    component: TelaPropriedade, 
  },
  {
    path: '/propriedade-cadastro',
    name: 'PropriedadeCadastro',
    component: PropriedadeCadastro, 
  },
  {
    path: '/propriedade-edicao/:propriedadeId',
    name: 'PropriedadeEdicao',
    component: PropriedadeEdicao, 
    props: true
  },
  {
    path: '/animais',
    name: 'TelaAnimais',
    component: TelaAnimais, 
  },
  {
    path: '/racas',
    name: 'TelaRaca',
    component: TelaRaca, 
  },
  {
    path: '/raca-cadastro',
    name: 'RacaCadastro',
    component: RacaCadastro, 
  },
  {
    path: '/raca-edicao/:racaId',
    name: 'RacaEdicao',
    component: RacaEdicao, 
    props: true
  },
  {
    path: '/piquetes',
    name: 'TelaPiquetes',
    component: TelaPiquetes, 
  },

  {
    path: '/piquetes-cadastro',
    name: 'PiqueteCadastro',
    component: PiqueteCadastro, 
  },

  {
    path: '/piquetes-edicao/:piqueteId',
    name: 'PiqueteEdicao',
    component: PiqueteEdicao, 
    props: true,
  },

  {
    path: '/animais-cadastro',
    name: 'AnimaisCadastro',
    component: AnimaisCadastro, 
  },

  {
    path: '/animal-edicao',
    name: 'AnimalEdicao',
    component: AnimaisEdicao,
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
    path: '/produtos-cadastro',
    name: 'ProdutoCadastro',
    component: ProdutoCadastro, 
  },
  {
    path: '/produtos-edicao/:produtoId',
    name: 'ProdutoEdicao',
    component: ProdutoEdicao,
    props: true, 
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
    path: '/compraprodutos-cadastro',
    name: 'CompraProdutoCadastro',
    component: CompraProdutoCadastro
  },
  {
    path: '/compraprodutos-edicao/:compraId',
    name: 'CompraProdutoEdicao',
    component: CompraProdutoEdicao,
    props: true
  },
  {
    path: '/suplementacoes',
    name: 'TelaSuplementacao',
    component: TelaSuplementacao
  },
  {
    path: '/suplementacao-cadastro',
    name: 'SuplementacaoCadastro',
    component: SuplementacaoCadastro
  },
  {
    path: '/suplementacao-edicao/:suplementacaoId',
    name: 'SuplementacaoEdicao',
    component: SuplementacaoEdicao,
    props: true
  },
  {
    path: '/suplementacao-finalizacao/:suplementacaoId',
    name: 'SuplementacaoFinalizacao',
    component: SuplementacaoFinalizacao,
    props: true
  },

  {
    path: '/aplicacoes-produtos-cadastro',
    name: 'AplicacoesProdutosCadastro',
    component: AplicacoesProdutosCadastro
  },

  {
    path: '/aplicacoes-produtos-edicao',
    name: 'AplicacoesProdutosEdicao',
    component: AplicacoesProdutosEdicao
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
    path: '/vendas-animais-cadastro',
    name: 'VendaAnimalCadastro',
    component: VendaAnimalCadastro
  },
  {
    path: '/vendas-animais-edicao/:vendaId',
    name: 'VendaAnimalEdicao',
    component: VendaAnimalEdicao,
    props: true
  },
  {
    path: '/vendas-animais-visualizacao/:dataSelecionada',
    name: 'VendaAnimalVisualizacao',
    component: VendaAnimalVisualizacao,
    props: true
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
    path: '/movimentacoes',
    name: 'TelaMovimentacoes',
    component: TelaMovimentacoes
  },
  {
    path: '/movimentacoes-cadastro',
    name: 'MovimentacaoCadastro',
    component: MovimentacaoCadastro
  },
  {
    path: '/movimentacoes-edicao/:movimentacaoId',
    name: 'MovimentacaoEdicao',
    component: MovimentacaoEdicao,
    props: true
  },
  {
    path: '/movimentacoes-visualizacao/:',
    name: 'MovimentacaoVisualizacao',
    component: MovimentacaoVisualizacao
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

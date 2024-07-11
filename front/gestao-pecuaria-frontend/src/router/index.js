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
import VeterinarioCadastro from '@/components/VeterinarioCadastro.vue';
import VeterinarioEdicao from '@/components/VeterinarioEdicao.vue';
import TelaProdutos from '@/views/TelaProdutos.vue';
import ProdutoCadastro from '@/components/ProdutoCadastro.vue'
import ProdutoEdicao from '@/components/ProdutoEdicao.vue'
import TelaPesagens from '@/views/TelaPesagens.vue';
import PesagemCadastro from '@/components/PesagemCadastro.vue';
import PesagemEdicao from '@/components/PesagemEdicao.vue';
import TelaCompraProdutos from '@/views/TelaCompraProdutos.vue';
import CompraProdutoCadastro from '@/components/CompraProdutoCadastro.vue';
import CompraProdutoEdicao from '@/components/CompraProdutoEdicao.vue';
import TelaSuplementacao from '@/views/TelaSuplementacao.vue';
import SuplementacaoCadastro from '@/components/SuplementacaoCadastro.vue';
import SuplementacaoEdicao from '@/components/SuplementacaoEdicao.vue';
import SuplementacaoFinalizacao from '@/components/SuplementacaoFinalizacao.vue';
import TelaAplicacoesProdutos from '@/views/TelaAplicacoesProdutos.vue';
import AplicacaoProdutoCadastro from '@/components/AplicacaoProdutoCadastro.vue';
import AplicacaoProdutoEdicao from '@/components/AplicacaoProdutoEdicao.vue';
import TelaVendasAnimais from '@/views/TelaVendasAnimais.vue';
import VendaAnimalCadastro from '@/components/VendaAnimalCadastro.vue';
import VendaAnimalEdicao from '@/components/VendaAnimalEdicao.vue';
import TelaInseminacoes from '@/views/TelaInseminacoes.vue';
import InseminacaoCadastro from '@/components/InseminacaoCadastro.vue';
import InseminacaoEdicao from '@/components/InseminacaoEdicao.vue';
import TelaOutrasDespesas from '@/views/TelaOutrasDespesas.vue'
import ViewAnimal from '@/views/ViewAnimal.vue';
import TelaMovimentacoes from '@/views/TelaMovimentacoes.vue';
import MovimentacaoCadastro from '@/components/MovimentacaoCadastro.vue';
import MovimentacaoEdicao from '@/components/MovimentacaoEdicao.vue';
import OutraDespesaEdicao from '@/components/OutraDespesaEdicao.vue';
import OutraDespesaCadastro from '@/components/OutraDespesaCadastro.vue';
import PiqueteCadastro from '@/components/PiqueteCadastro.vue';
import PiqueteEdicao from '@/components/PiqueteEdicao.vue';
import AnimaisCadastro from '@/components/AnimaisCadastro.vue';
import AnimaisEdicao from '@/components/AnimaisEdicao.vue';

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
    path: '/raca-cadastro/:animalJSON',
    name: 'RacaCadastro',
    component: RacaCadastro,
    props: true 
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
    path: '/animais-cadastro/:animalJSON',
    name: 'AnimaisCadastro',
    component: AnimaisCadastro, 
    props: true
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
    path: '/veterinarios',
    name: 'TelaVeterinarios',
    component: TelaVeterinarios, 
  },
  {
    path: '/veterinarios/cadastro',
    name: 'VeterinarioCadastro',
    component: VeterinarioCadastro
  },
  {
    path: '/veterinarios/edicao/:veterinarioId',
    name: 'VeterinarioEdicao',
    component: VeterinarioEdicao,
    props: true
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
    path: '/pesagens',
    name: 'TelaPesagens',
    component: TelaPesagens 
  },
  {
    path: '/pesagens-cadastro',
    name: 'PesagemCadastro',
    component: PesagemCadastro 
  },
  {
    path: '/pesagens-edicao/:pesagemId',
    name: 'PesagemEdicao',
    component: PesagemEdicao,
    props: true
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
    path: '/aplicacoes-produtos/cadastro',
    name: 'AplicacaoProdutoCadastro',
    component: AplicacaoProdutoCadastro,
  },

  {
    path: '/aplicacoes-produtos/edicao/:aplicacaoId',
    name: 'AplicacaoProdutoEdicao',
    component: AplicacaoProdutoEdicao,
    props: true,
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
    path: '/inseminacoes',
    name: 'TelaInseminacoes',
    component: TelaInseminacoes
  },
  {
    path: '/inseminacoes-cadastro',
    name: 'InseminacaoCadastro',
    component: InseminacaoCadastro
  },
  {
    path: '/inseminacoes-edicao/:inseminacaoId',
    name: 'InseminacaoEdicao',
    component: InseminacaoEdicao,
    props: true
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

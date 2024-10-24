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
import PerfilTrocarSenha from '@/components/PerfilTrocarSenha.vue';
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
import AnimalVisualizacao from '@/views/TelaAnimalDetalhes.vue';
import TelaInseminacoes from '@/views/TelaInseminacoes.vue';
import InseminacaoCadastro from '@/components/InseminacaoCadastro.vue';
import InseminacaoEdicao from '@/components/InseminacaoEdicao.vue';
import TelaGastos from '@/views/TelaGastos.vue'
import TelaMovimentacoes from '@/views/TelaMovimentacoes.vue';
import MovimentacaoCadastro from '@/components/MovimentacaoCadastro.vue';
import MovimentacaoEdicao from '@/components/MovimentacaoEdicao.vue';
import GastoEdicao from '@/components/GastoEdicao.vue';
import GastoCadastro from '@/components/GastoCadastro.vue';
import PiqueteCadastro from '@/components/PiqueteCadastro.vue';
import PiqueteEdicao from '@/components/PiqueteEdicao.vue';
import AnimaisCadastro from '@/components/AnimaisCadastro.vue'; 
import AnimaisEdicao from '@/components/AnimaisEdicao.vue';
import OcorrenciaCadastro from '@/components/OcorrenciaCadastro.vue';
import OcorrenciaEdicao from '@/components/OcorrenciaEdicao.vue';
import FotoAnimalCadastro from '@/components/FotoAnimalCadastro.vue';
import FotoAnimalVisualizacao from '@/components/FotoAnimalVisualizacao.vue';
import PrimeiraPropriedade from '@/views/PrimeiraPropriedade.vue';
import ResetPassword from '@/components/ResetPassword.vue';

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
    path: '/animal-edicao/:animalId',
    name: 'AnimalEdicao',
    component: AnimaisEdicao,
    props: true
  },

  
  {
    path: '/vizualizarAnimal/:animalId',
    name: 'VizualizarAnimal',
    component: AnimalVisualizacao,
    props: true
  },

  {
    path: '/meuperfil',
    name: 'PerfilProdutor',
    component: PerfilProdutor, 
  },

  {
    path: '/trocar-senha',
    name: 'PerfilTrocarSenha',
    component: PerfilTrocarSenha, 
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
    path: '/gastos',
    name: 'TelaGastos',
    component: TelaGastos,
  },

  {
    path: '/gasto-edicao/:gastoId',
    name: 'EdicaoGasto',
    component: GastoEdicao,
    props: true
  },

  {
    path: '/gasto-cadastro',
    name: 'CadastroGasto',
    component: GastoCadastro
  },

  {
    path: '/primeira-propriedade',
    name: 'PrimeiraPropriedade',
    component: PrimeiraPropriedade
  },

  {
    path: '/ocorrencia-cadastro/:animalId',
    name: 'OcorrenciaCadastro',
    component: OcorrenciaCadastro,
    props: true,
  },

  {
    path: '/ocorrencia-edicao/:ocorrenciaId',
    name: 'OcorrenciaEdicao',
    component: OcorrenciaEdicao,
    props: true,
  },
  
  {
    path: '/foto-cadastro/:animalId',
    name: 'FotoCadastro',
    component: FotoAnimalCadastro,
    props: true,
  },

  {
    path: '/foto-visualizacao/:animalId',
    name: 'FotoVisualizacao',
    component: FotoAnimalVisualizacao,
    props: true,
  },

  {
    path: '/redefinir-senha/:uid/:token',
    name: 'ResetPassword',
    component: ResetPassword
  },



];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

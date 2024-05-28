from core import views
from rest_framework import routers
from django.urls import path, include

#teste
app_name = 'core'
router = routers.DefaultRouter()
router.register('propriedades', views.PropriedadeViewSet)
router.register('racas', views.RacaViewSet)
router.register('animais', views.AnimalViewSet)
router.register('piquetes' , views.PiqueteViewSet)
router.register('veterinarios', views.VeterinarioViewSet)
router.register('produtos', views.ProdutoViewSet)
router.register('pesagens', views.PesagemViewSet)
router.register('compras-produtos', views.CompraProdutoViewSet)
router.register('suplementacoes', views.SuplementacaoViewSet)
router.register('ocorrencias', views.OcorrenciaViewSet)
router.register('inseminacoes', views.InseminacaoViewSet)
router.register('outras-despesas', views.OutraDespesaViewSet)
router.register('vendas-animais', views.VendaAnimalViewSet)
router.register('aplicacoes-produtos', views.AplicacaoProdutoViewSet)
router.register('fotos-animais', views.FotoViewSet)

urlpatterns = [
    path('',include(router.urls)),
]



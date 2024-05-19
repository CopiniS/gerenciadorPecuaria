from core import views
from rest_framework import routers
from django.urls import path, include


app_name = 'core'
router = routers.DefaultRouter()
router.register('propriedades', views.PropriedadeViewSet)
router.register('racas', views.RacaViewSet)
router.register('animais', views.AnimalViewSet)
router.register('lotes' , views.LoteViewSet)
router.register('veterinarios', views.VeterinarioViewSet)
router.register('produtos-sanitarios', views.ProdutoSanitarioViewSet)
router.register('produtos-alimenticios', views.ProdutoAlimenticioViewSet)
router.register('pesagens', views.PesagemViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
"""
URL configuration for gestaoPecuaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'core'
router = routers.DefaultRouter()
router.register('produtores', views.ProdutorViewSet)
router.register('propriedades', views.PropriedadeViewSet)
router.register('racas', views.RacaViewSet)
router.register('animais', views.AnimalViewSet)
router.register('lotes' , views.LoteViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('produtor/login/', views.ProdutorLoginAPIView.as_view(), name='produtor-login'),
]

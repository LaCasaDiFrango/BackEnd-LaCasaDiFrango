from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core.views.usuario.user import UserViewSet
from core.views.usuario.endereco import EnderecoViewSet
from core.views.usuario.cartao import CartaoViewSet
from core.views.produto.produto import ProdutoViewSet
from core.views.produto.categoria import CategoriaViewSet

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'enderecos', EnderecoViewSet, basename='enderecos')
router.register(r'cartoes', CartaoViewSet, basename='cartoes')
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'categorias', CategoriaViewSet, basename='categorias')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # API
    path('api/', include(router.urls)),
]

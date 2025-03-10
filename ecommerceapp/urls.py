from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ecommerceapp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    path("todos-produtos/", TodosProdutosView.as_view(), name="todosprodutos"),
    path("produto/<slug:slug>/", ProdutoDetalheView.as_view(), name="produtodetalhe"),
    path("add-cart-<int:pro_id>/", AddCartView.as_view(), name="add-cart"),
    path("meu-cart/", MeuCartView.as_view(), name="meucart"),
    path("manipular-cart/<int:cp_id>/", ManipularCartView.as_view(), name="manipularcart"),
    path("limpar-cart/", LimparCartView.as_view(), name="limparcart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("pagamento/", PagamentoView.as_view(), name="pagamento"),

    path("registrar/", ClienteRegistrarView.as_view(), name="clienteregistrar"),
    path("sair/", ClienteSairView.as_view(), name="clientesair"),
    path("entrar/", ClienteEntrarView.as_view(), name="clienteentrar"),
    path("perfil/", ClientePerfilView.as_view(), name="clienteperfil"),
    path("perfil/pedido-<int:pk>/", ClientePedidoViewDetalhe.as_view(), name="clientepedidodetalhe"),
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),

    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-pedido/<int:pk>/", AdminPedidoDetalheView.as_view(), name="adminpedidodetalhe"),
    path("admin-todos-pedidos/", AdminPedidoListView.as_view(), name="adminpedidolist"),
    path("admin-pedido-<int:pk>-mudar/", AdminPedidoMudarStatusView.as_view(), name="adminpedidomudar"),
    path("pesquisar/", PesquisarView.as_view(), name="pesquisar"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
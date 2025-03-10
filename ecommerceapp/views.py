from django.shortcuts import render, redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.urls.base import reverse
from .forms import *
from.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


class LojaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated:
                try:
                    cliente = request.user.cliente
                    cart_obj.cliente = cliente
                    cart_obj.save()
                except ObjectDoesNotExist:
                    pass
        return super().dispatch(request, *args, **kwargs)



class HomeView(LojaMixin, TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_produtos = Produto.objects.all().order_by("-id")
        paginator = Paginator(all_produtos, 4)
        page_number = self.request.GET.get('page')
        produto_list = paginator.get_page(page_number)
        context['produto_list'] = produto_list
        return context
    
class TodosProdutosView(LojaMixin, TemplateView):
    template_name = 'todosprodutos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todascategorias'] = Categoria.objects.all()
        return context
    

class ProdutoDetalheView(LojaMixin, TemplateView):
    template_name = 'produtodetalhe.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        produto.visualizacao +=1
        produto.save()
        context['produto'] = produto
        return context
    
class AddCartView(LojaMixin, View):
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            produto_cart = cart_obj.cartitem_set.filter(produto=produto_obj)

            if produto_cart.exists():
                cartproduto = produto_cart.last()
                cartproduto.quantidade += 1
                cartproduto.subtotal += produto_obj.venda
                cartproduto.save()
                cart_obj.total += produto_obj.venda
                cart_obj.save()
            else:
                cartproduto = CartItem.objects.create(cart=cart_obj, produto=produto_obj, avaliacao=produto_obj.venda, quantidade=1, subtotal=produto_obj.venda)
                cart_obj.total += produto_obj.venda
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduto = CartItem.objects.create(cart=cart_obj, produto=produto_obj, avaliacao=produto_obj.venda, quantidade=1, subtotal=produto_obj.venda)
            cart_obj.total += produto_obj.venda
            cart_obj.save()
        return redirect('ecommerceapp:meucart')
    
class ManipularCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        acao = request.GET.get("acao")
        cp_obj = CartItem.objects.get (id=cp_id)
        cart_obj = cp_obj.cart

        if acao == "inc":
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.avaliacao
            cp_obj.save()
            cart_obj.total += cp_obj.avaliacao
            cart_obj.save()
        elif acao == "dcr":
            cp_obj.quantidade -= 1
            cp_obj.subtotal -= cp_obj.avaliacao
            cp_obj.save()
            cart_obj.total -= cp_obj.avaliacao
            cart_obj.save()
            if cp_obj.quantidade == 0:
                cp_obj.delete()
        elif acao == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            
        return redirect('ecommerceapp:meucart')
    


class LimparCartView(LojaMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartitem_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('ecommerceapp:meucart')


class MeuCartView(LojaMixin, TemplateView):
    template_name = 'meucart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
        

class CheckoutView(LojaMixin, CreateView):
    template_name = 'processar.html'
    form_class = Checar_PedidoForm
    success_url = reverse_lazy('ecommerceapp:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect("/entrar/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.sub_total = cart_obj.total
            form.instance.desconto = 0
            form.instance.total = cart_obj.total
            form.instance.pedido_status = "Pedido Recebido"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("pagamento_metodo")
            pedido = form.save()
            if pm == "khalti":
                return redirect(reverse('ecommerceapp:pagamento')+ "?o_id=" + str(pedido.id))
        else:
            return redirect('ecommerceapp:home')
        return super().form_valid(form)
    

class PagamentoView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get('o_id')
        pedido = Pedido_order.objects.get(id=o_id)
        cliente = pedido.cart.cliente
        context = {
            "pedido": pedido,
            "cliente": cliente,
        }
        return render(request, 'pagamento.html', context)


class ClienteRegistrarView(CreateView):
    template_name = 'clienteregistrar.html'
    form_class = ClienteRegistrarForm
    success_url = reverse_lazy('ecommerceapp:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url    

class ClienteSairView(View):
    def get(self, request):
        logout(request)
        return redirect('ecommerceapp:home')
    

class ClienteEntrarView(FormView):
    template_name = 'clienteentrar.html'
    form_class = ClienteEntrarForm
    success_url = reverse_lazy('ecommerceapp:home')

    def form_valid(self, form):
        unome = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=unome, password=pword)
        if usr is not None and Cliente.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Usuário ou senha inválidos'})
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
    

class SobreView(LojaMixin, TemplateView):
    template_name = 'sobre.html'


class ContatoView(LojaMixin, TemplateView):
    template_name = 'contato.html'


class ClientePerfilView(LojaMixin, TemplateView):
    template_name = 'clienteperfil.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.request.user.cliente
        context['cliente'] = cliente

        Pedidos = Pedido_order.objects.filter(cart__cliente=cliente)
        context['pedidos'] = Pedidos
        return context
    

class ClientePedidoViewDetalhe(DetailView):
    template_name = 'clientepedidodetalhe.html'
    model = Pedido_order
    context_object_name = 'pedido_obj'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)
    

class AdminLoginView(FormView):
    template_name = 'admin_paginas/adminlogin.html'
    form_class = ClienteEntrarForm
    success_url = reverse_lazy('ecommerceapp:adminhome')

    def form_valid(self, form):
        unome = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=unome, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Usuário ou senha inválidos'})
        return super().form_valid(form)
    

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_paginas/adminhome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PedidosPendentes'] = Pedido_order.objects.filter(pedido_status="Pedido Recebido").order_by("-id")
        return context
    

class AdminPedidoDetalheView(AdminRequiredMixin, DetailView):
    template_name = 'admin_paginas/adminpedidodetalhe.html'
    model = Pedido_order
    context_object_name = 'pedido_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todosstatus'] = PEDIDO_STATUS 
        return context


class AdminPedidoListView(AdminRequiredMixin, ListView):
    template_name = 'admin_paginas/adminpedidolist.html'
    queryset = Pedido_order.objects.all().order_by("-id")
    context_object_name = 'todospedidos'


class AdminPedidoMudarStatusView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = Pedido_order.objects.get(id=pedido_id)
        novo_status = request.POST.get("status")
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()
        return redirect(reverse_lazy("ecommerceapp:adminpedidodetalhe", kwargs={"pk": pedido_id}))
    

class PesquisarView(LojaMixin, TemplateView):
    template_name = 'pesquisar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        result = Produto.objects.filter(
            Q(titulo__contains=kw) | Q(descricao__contains=kw) | Q(return_devolucao__contains=kw))
        context["result"] = result
        return context
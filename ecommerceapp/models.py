from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    data_on = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.nome_completo
    

class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo
    
    
class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/')
    preco_mercado = models.PositiveBigIntegerField()
    venda = models.PositiveBigIntegerField()
    descricao = models.TextField()
    garantia = models.CharField(max_length=300,null=True,blank=True)
    return_devolucao = models.CharField(max_length=300,null=True,blank=True)
    visualizacao = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.titulo
    

class Cart(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return "Cart" + str(self.id)
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveBigIntegerField()
    
    def __str__(self):
        return "Cart" + str(self.cart.id) + "CartItem:" + str(self.id)
    
PEDIDO_STATUS = (
    ('Pedido Recebido', 'Pedido Recebido'),
    ('Pedido em Processo', 'Pedido em Processo'),
    ('Pedido Enviado', 'Pedido Enviado'),
    ('Pedido Entregue', 'Pedido Entregue'),
    ('Pedido Cancelado', 'Pedido Cancelado'),
)

METODO = (
    ("Dinheiro na Entrega", "Dinheiro na Entrega"),
    ("khalti", "khalti"),
)
   
class Pedido_order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    endereco_envio = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    sub_total = models.PositiveBigIntegerField()
    desconto = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)
    criado_em = models.DateTimeField(auto_now_add=True)
    pagamento_metodo = models.CharField(max_length=20, choices=METODO, default="Dinheiro na Entrega")
    pagamento_completo = models.BooleanField(default=False, null=True, blank=True)
  
    def __str__(self):
        return "Pedido_order:" + str(self.id)
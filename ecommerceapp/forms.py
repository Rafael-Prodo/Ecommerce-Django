from django import forms
from .models import *
from django.contrib.auth.models import User


class Checar_PedidoForm(forms.ModelForm):
    ordenado_por = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    endereco_envio = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    pagamento_metodo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 150px;'}), choices=METODO)

    class Meta:
        model = Pedido_order
        fields = ['ordenado_por', 'endereco_envio', 'telefone', 'email', 'pagamento_metodo']


class ClienteRegistrarForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    nome_completo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    endereco = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))


    class Meta:
        model = Cliente
        fields = ['username', 'password', 'email', 'nome_completo', 'endereco']

    def clean_username(self):
        unome = self.cleaned_data.get('username')
        if User.objects.filter(username=unome).exists():
            raise forms.ValidationError("Username already exists")
        return unome
    
class ClienteEntrarForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'form-control', 'style': 'max-width: 300px;'}))


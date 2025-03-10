# 🛒 Ecommerce-Django

Bem-vindo ao Ecommerce-Django, uma plataforma de comércio eletrônico desenvolvida com Python e Django, projetada para oferecer uma experiência de compra online eficiente e intuitiva.

## 🚀 Funcionalidades Principais

- Catálogo de Produtos: Navegação por uma variedade de produtos organizados por categorias.
- Carrinho de Compras: Adição e remoção de produtos com atualização em tempo real do total.
- Processo de Checkout: Finalização de compras com integração a métodos de pagamento.
- Autenticação de Usuários: Sistema de registro e login para clientes.
- Painel Administrativo: Gerenciamento de produtos, pedidos e usuários.

## 🛠️ Tecnologias Utilizadas

- Linguagem: Python 3.7.3
- Framework: Django 2.2.4
- Banco de Dados: SQLite (padrão)
- Front-end: HTML5, CSS3, JavaScript
- Bibliotecas Adicionais:
- django-crispy-forms para formulários estilizados
- Pillow para manipulação de imagens
  
## 📂 Estrutura do Projeto

- ecommerceproject/: Diretório principal do projeto Django.
- ecommerceapp/: Aplicativo principal contendo as funcionalidades de e-commerce.
- templates/: Arquivos HTML para renderização das páginas.
- media/: Arquivos de mídia, como imagens de produtos.
- db.sqlite3: Banco de dados SQLite.
- manage.py: Script de gerenciamento do Django.

## 🚀 Como Executar o Projeto
  
- Clone o repositório:
  
  ```bash
  git clone https://github.com/Rafael-Prodo/Ecommerce-Django.git

- Navegue até o diretório do projeto:

    ```bash
  cd Ecommerce-Django
  
- Crie e ative um ambiente virtual: 

  ```bash
  python -m venv venv source venv/bin/activate # No Windows: venv\Scripts\activate.bat
  
- Instale as dependências:

    ```bash
  pip install -r requirements.txt
  
- Realize as migrações do banco de dados:

    ```bash
  python manage.py migrate
  
- Inicie o servidor de desenvolvimento:

    ```bash
  python manage.py runserver
  
- Acesse o projeto em <a href="http://localhost:8000/"></a>

## 🤝 Contribuições

- Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📖 Referências

- Este projeto foi inspirado pelo curso [@cursodetecnologiaeprogramação](https://www.youtube.com/@cursodetecnologiaeprogramação), com exemplos práticos alinhados ao mercado.

## 📝 Licença

- Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

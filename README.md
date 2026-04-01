🛒 Sistema de Loja (Simulação com Python + SQLAlchemy)
📌 Descrição

Este projeto consiste em um sistema de simulação de uma loja virtual desenvolvido em Python. A aplicação permite o gerenciamento completo de produtos, estoque, carrinho de compras e processamento de pagamentos, com persistência de dados utilizando banco de dados via SQLAlchemy.
O sistema foi projetado com foco em organização modular, separação de responsabilidades e integração com banco de dados relacional.

🚀 Funcionalidades

📦 Gestão de Produtos (Estoque)
Cadastrar mercadorias
Listar produtos disponíveis no estoque
Atualizar informações de produtos
Excluir produtos do estoque

🛍️ Carrinho de Compras
Adicionar produtos ao carrinho
Remover produtos do carrinho
Visualizar itens adicionados
Calcular valor total da compra

💳 Pagamento
Simulação de pagamento
Finalização da compra
Atualização automática do estoque após pagamento

🗄️ Banco de Dados
O arquivo de banco é database.db
A conexão é feita em connection.py
O SQLAlchemy é usado como ORM para gerenciar a persistência

🧱 Tecnologias Utilizadas
Python: linguagem principal do projeto.
SQLAlchemy: usado como ORM para modelagem e persistência de dados.
SQLite: banco de dados local, acessado via sqlite3 e SQLAlchemy.
Biblioteca padrão do Python: para entrada/saída no terminal e lógica de menu.

⚙️ Instalação e Configuração

1. Clonar o repositório
   git clone https://github.com/seu-usuario/seu-projeto.git
   cd seu-projeto
2. Criar ambiente virtual
   Python -m venv .venv
3. Ativar ambiente virtual
  Windows:
  .venv\Scripts\activate
  Linux/Mac:
  source .venv/bin/activate
4. Instalar dependências
  pip install -r requirements.txt

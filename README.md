🛒 Sistema de Loja (Simulação com Python + SQLAlchemy)\n
📌 Descrição\n

Este projeto consiste em um sistema de simulação de uma loja virtual desenvolvido em Python. A aplicação permite o gerenciamento completo de produtos, estoque, carrinho de compras e processamento de pagamentos, com persistência de dados utilizando banco de dados via SQLAlchemy.
O sistema foi projetado com foco em organização modular, separação de responsabilidades e integração com banco de dados relacional.

🚀 Funcionalidades\n

📦 Gestão de Produtos (Estoque)\n
Cadastrar mercadorias\n
Listar produtos disponíveis no estoque\n
Atualizar informações de produtos\n
Excluir produtos do estoque\n

🛍️ Carrinho de Compras\n
Adicionar produtos ao carrinho\n
Remover produtos do carrinho\n
Visualizar itens adicionados\n
Calcular valor total da compra\n\n

💳 Pagamento\n
Simulação de pagamento\n
Finalização da compra\n
Atualização automática do estoque após pagamento\n\n

🗄️ Banco de Dados\n
O arquivo de banco é database.db\n
A conexão é feita em connection.py\n
O SQLAlchemy é usado como ORM para gerenciar a persistência\n\n

🧱 Tecnologias Utilizadas\n
Python: linguagem principal do projeto.\n
SQLAlchemy: usado como ORM para modelagem e persistência de dados.\n
SQLite: banco de dados local, acessado via sqlite3 e SQLAlchemy.\n
Biblioteca padrão do Python: para entrada/saída no terminal e lógica de menu.\n\n

⚙️ Instalação e Configuração\n
1. Clonar o repositório\n
   git clone\n
2. Criar ambiente virtual\n
   Python -m venv .venv\n
3. Ativar ambiente virtual\n
  Windows:\n
  .venv\Scripts\activate\n
  Linux/Mac:\n
  source .venv/bin/activate\n
4. Instalar dependências\n
  pip install -r requirements.txt\n

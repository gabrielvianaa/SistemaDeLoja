<div align="center">

# HARDWARE COMMERCE

**Aplicação desktop para gerenciamento completo de uma loja de componentes de hardware.**  
Interface gráfica moderna em tema escuro, construída com Python e CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-7F77DD?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.48-D71F00?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-embutido-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Werkzeug](https://img.shields.io/badge/Werkzeug-3.0.1-FF6600?style=flat-square)
![License](https://img.shields.io/badge/licença-MIT-22C55E?style=flat-square)

</div>

## Visão geral

O HARDWARE COMMERCE é um sistema de ponto de venda (PDV) desktop para lojas de hardware. Ele reúne catálogo de produtos, carrinho de compras, processamento de pagamentos e painel administrativo em uma única aplicação leve — sem necessidade de servidor externo ou conexão com internet.

### Funcionalidades principais

| Área | Recursos |
|---|---|
| **Catálogo** | Listagem por categoria, busca em tempo real, filtros por chips |
| **Carrinho** | Adicionar / remover produtos, controle de quantidade, estoque atualizado em tempo real |
| **Pagamento** | 5 métodos (Pix, Boleto, Crédito, Débito, Parcelado), descontos automáticos, parcelamento com juros configurável |
| **Usuários** | Cadastro com CPF validado, autenticação por e-mail e senha, persistência do carrinho entre sessões |
| **Admin** | Cadastrar / remover / editar produtos, configurar descontos e parcelamento, gerenciar administradores |


## Tecnologias

### Linguagem e runtime

| Tecnologia | Versão | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Linguagem principal |

### Interface gráfica

| Tecnologia | Versão | Uso |
|---|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | 5.2.2 | Widgets modernos sobre Tkinter — tema escuro nativo |
| [darkdetect](https://github.com/albertosottile/darkdetect) | 0.8.0 | Detecção de tema do sistema operacional |

### Banco de dados e ORM

| Tecnologia | Versão | Uso |
|---|---|---|
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0.48 | ORM declarativo, gerenciamento de sessões e migrations |
| [SQLite](https://www.sqlite.org/) | embutido no Python | Banco de dados local — arquivo `app/database/database.db` |
| [greenlet](https://greenlet.readthedocs.io/) | 3.3.2 | Dependência interna do SQLAlchemy (concorrência) |

### Segurança

| Tecnologia | Versão | Uso |
|---|---|---|
| [Werkzeug](https://werkzeug.palletsprojects.com/) | 3.0.1 | Hash de senhas (PBKDF2-SHA256) — `generate_password_hash` / `check_password_hash` |

### Utilitários

| Tecnologia | Versão | Uso |
|---|---|---|
| [packaging](https://packaging.pypa.io/) | 26.0 | Gerenciamento de versões de dependências |
| [MarkupSafe](https://markupsafe.palletsprojects.com/) | 3.0.3 | Dependência do Werkzeug |


## Pré-requisitos

- **Python 3.10 ou superior** — [download](https://www.python.org/downloads/)
- **pip** — já incluso no Python 3.4+
- Sistema operacional: Windows 10+, macOS 11+ ou Linux (Ubuntu 20.04+)

> **Não é necessário** instalar banco de dados, servidor ou qualquer dependência de sistema. O SQLite é embutido no Python.

## Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sistema-de-loja.git
cd sistema-de-loja
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema

```bash
python main.py
```

O banco de dados (`database.db`) e os arquivos de configuração (`descontos.json`, `parcelas.json`) serão criados automaticamente na primeira execução.

## Primeiro acesso

Na primeira execução, o sistema cria automaticamente:

- **8 categorias** de produtos (Processadores, Placas de Vídeo, Memórias RAM, Air Coolers, Water Coolers, Armazenamento, Fontes de Alimentação, Gabinetes)
- **8 produtos padrão** para demonstração
- **Administrador padrão** com as credenciais abaixo

```
Usuário: admin
Senha:   admin123
```

> ⚠️ **Importante:** altere a senha padrão do admin antes de usar o sistema em produção.


## Guia rápido de uso

### Como cliente

1. Abra o sistema — o catálogo de produtos é exibido automaticamente
2. Use os **filtros de categoria** ou a **barra de busca** para encontrar produtos
3. Clique em **"+ Adicionar ao carrinho"** em qualquer produto
4. Acompanhe o carrinho no painel direito — ajuste quantidades com os botões `+` e `−`
5. Selecione o **método de pagamento** (Pix tem 10% de desconto, Boleto 5%)
6. Clique em **"Finalizar compra"** para ver o resumo do pedido

### Como administrador

1. Clique em **"Login Admin"** na sidebar
2. Entre com as credenciais de administrador
3. Com o modo admin ativo, novos controles aparecem na sidebar

### Métodos de pagamento e descontos padrão

| Método | Desconto | Parcelamento |
|---|---|---|
| Pix | 10% | Não |
| Boleto | 5% | Não |
| Cartão de Débito | 0% | Não |
| Cartão de Crédito | 0% | Até 12× (3× sem juros, 2% a.m. após) |
| Parcelado | 0% | Até 12× (3× sem juros, 2% a.m. após) |

> Os descontos e regras de parcelamento são **totalmente configuráveis** pelo painel admin.


## Interface e Design

A documentação completa de interface está em [`docs/documentacao/documentacao-interfaces.md`](docs/documentacao/documentacao-interfaces.md) e o guia de estilo em [`docs/guia-estilo/design-system.md`](docs/guia-estilo/design-system.md).

O diagrama de navegação completo está em [`docs/userflow/user-flow.svg`](docs/userflow/user-flow.svg).

---

### Telas do cliente

#### T01 — Boas-vindas
Tela inicial exibida ao abrir o sistema e após qualquer logout.

![T01 — Boas-vindas](docs/prototipos/T01-boas-vindas.svg)

---

#### T02 — Catálogo de Produtos (Visitante)
Listagem somente-leitura. Visitantes não podem adicionar ao carrinho.

![T02 — Catálogo Visitante](docs/prototipos/T02-catalogo-visitante.svg)

---

#### T02A — Catálogo de Produtos (Logado)
Versão interativa com seleção de produto, campo de quantidade e botão de adição ao carrinho.

![T02A — Catálogo Logado](docs/prototipos/T02A-catalogo-logado.svg)

---

#### T03 — Carrinho de Compras
Visualização dos itens, remoção, seleção de método de pagamento e finalização.

![T03 — Carrinho](docs/prototipos/T03-carrinho.svg)

---

#### T04 — Dados do Cartão / Parcelamento
Formulário exibido ao selecionar Cartão de Crédito ou Parcelado.

![T04 — Dados do Cartão](docs/prototipos/T04-dados-cartao.svg)

---

#### T05 — Login de Usuário

![T05 — Login](docs/prototipos/T05-login.svg)

---

#### T06 — Cadastro de Usuário
CPF é auto-formatado durante a digitação. Após o cadastro o usuário já fica autenticado.

![T06 — Cadastro](docs/prototipos/T06-cadastro.svg)

---

#### T07 — Resumo do Pedido
Exibida após pagamento bem-sucedido com total pago, desconto e parcelas.

![T07 — Pedido Sucesso](docs/prototipos/T07-pedido-sucesso.svg)

---

### Telas do administrador

#### T08 — Login Admin

![T08 — Login Admin](docs/prototipos/T08-login-admin.svg)

---

#### T09 — Cadastrar Mercadoria

![T09 — Cadastrar Mercadoria](docs/prototipos/T09-cadastrar-mercadoria.svg)

---

#### T10 — Retirar Mercadoria
Seleção por clique na tabela. Botão desabilitado até seleção.

![T10 — Retirar Mercadoria](docs/prototipos/T10-retirar-mercadoria.svg)

---

#### T11 — Alterar Preço

![T11 — Alterar Preço](docs/prototipos/T11-alterar-preco.svg)

---

#### T12 — Criar Admin

![T12 — Criar Admin](docs/prototipos/T12-criar-admin.svg)

---

#### T13 — Listar Admins

![T13 — Listar Admins](docs/prototipos/T13-listar-admins.svg)

---

#### T14 — Listar Usuários
Email e CPF mascarados por privacidade.

![T14 — Listar Usuários](docs/prototipos/T14-listar-usuarios.svg)

---

#### T15 — Configurar Descontos

![T15 — Configurar Descontos](docs/prototipos/T15-configurar-descontos.svg)

---

#### T16 — Configurar Parcelamento

![T16 — Configurar Parcelamento](docs/prototipos/T16-configurar-parcelamento.svg)

---

## Estrutura do projeto

```
SistemaDeLoja/
├── main.py                          # Entry point — inicializa banco e loop principal
├── requirements.txt
├── docs/
│   ├── prototipos/                  # SVG individual de cada tela (17 arquivos)
│   │   ├── T01-boas-vindas.svg
│   │   ├── T02-catalogo-visitante.svg
│   │   ├── T02A-catalogo-logado.svg
│   │   ├── T03-carrinho.svg
│   │   ├── T04-dados-cartao.svg
│   │   ├── T05-login.svg
│   │   ├── T06-cadastro.svg
│   │   ├── T07-pedido-sucesso.svg
│   │   ├── T08-login-admin.svg
│   │   ├── T09-cadastrar-mercadoria.svg
│   │   ├── T10-retirar-mercadoria.svg
│   │   ├── T11-alterar-preco.svg
│   │   ├── T12-criar-admin.svg
│   │   ├── T13-listar-admins.svg
│   │   ├── T14-listar-usuarios.svg
│   │   ├── T15-configurar-descontos.svg
│   │   └── T16-configurar-parcelamento.svg
│   ├── userflow/
│   │   └── user-flow.svg
│   ├── documentacao/
│   │   └── documentacao-interfaces.md
│   └── guia-estilo/
│       └── design-system.md
└── app/
    ├── core/
    │   └── carrinho.py
    ├── database/
    │   ├── models.py
    │   ├── connection.py
    │   ├── database.db
    │   ├── descontos.json
    │   └── parcelas.json
    ├── services/
    │   ├── produto_service.py
    │   ├── carrinho_service.py
    │   ├── usuario_service.py
    │   ├── admin_service.py
    │   └── pagamento_service.py
    └── ui/
        └── app.py
```


## Dependências completas (`requirements.txt`)

```
SQLAlchemy==2.0.48
Werkzeug==3.0.1
customtkinter
```

---

## Variáveis de configuração

**`descontos.json`**
```json
{
  "Cartao de Credito": 0.0,
  "Cartao de Debito": 0.0,
  "Parcelado": 0.0,
  "Boleto": 0.05,
  "Pix": 0.10
}
```

**`parcelas.json`**
```json
{
  "max_parcelas": 12,
  "sem_juros_ate": 3,
  "tipo_taxa": "juros",
  "taxa_mensal": 0.02
}
```

## Solução de problemas

**`ModuleNotFoundError: No module named 'customtkinter'`**
```bash
pip install customtkinter
```

**`ModuleNotFoundError: No module named 'sqlalchemy'`**
```bash
pip install SQLAlchemy==2.0.48
```

**A janela não abre no Linux (erro de display)**
```bash
sudo apt-get install python3-tk
```

**O banco de dados corrompeu ou quero resetar tudo**
```bash
rm app/database/database.db
rm app/database/descontos.json
rm app/database/parcelas.json
python main.py
```

**Erro de permissão ao criar o banco no Windows**  
Execute o terminal como administrador ou mova o projeto para uma pasta sem restrições (ex.: `C:\Users\SeuNome\Projetos\`).


## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).


<div align="center">
  Desenvolvido com Python · CustomTkinter · SQLAlchemy · SQLite
</div>

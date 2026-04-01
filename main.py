from app.database.base import Base
from app.database.connection import engine, database_file
from app.services import produto_service
from app.services.carrinho_service import adicionar_ao_carrinho
from app.core.carrinho import Carrinho
from app.services.produto_service import buscar_produto_por_id, deletar_produto


def ensure_produtos_schema():
    import sqlite3

    conn = sqlite3.connect(str(database_file))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'")
    if cur.fetchone() is not None:
        cur.execute("PRAGMA table_info(produtos)")
        columns = cur.fetchall()
        for column in columns:
            if column[1] == 'id' and column[2].upper() != 'FLOAT':
                conn.close()
                Base.metadata.drop_all(engine)
                Base.metadata.create_all(engine)
                return
    conn.close()

ensure_produtos_schema()
Base.metadata.create_all(engine)

def safe_int_input(prompt: str):
    valor = input(prompt)
    try:
        return int(valor)
    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")
        return None


def safe_float_input(prompt: str):
    valor = input(prompt)
    try:
        return float(valor)
    except ValueError:
        print("Entrada inválida. Digite um número válido.")
        return None

if not produto_service.listarProdutos():
    produto_service.criarProduto(1, "i7 12700k", 1500.00, 10, "Processadores")
    produto_service.criarProduto(2, "RTX 4070", 2500.00, 5, "Placas de Vídeo")
    produto_service.criarProduto(3, "16GB DDR4", 300.00, 20, "Memórias RAM")
    produto_service.criarProduto(4, "Air Cooler XYZ", 200.00, 15, "Air Coolers")
    produto_service.criarProduto(5, "Water Cooler ABC", 400.00, 8, "Water Coolers")
    produto_service.criarProduto(6, "SSD 1TB", 500.00, 12, "Armazenamento")
    produto_service.criarProduto(7, "Fonte 650W", 350.00, 10, "Fontes de Alimentação")
    produto_service.criarProduto(8, "Gabinete Gamer", 250.00, 7, "Gabinetes")

def menu():
    carrinho = Carrinho()
    admin_logado = False
    ADMIN_PASSWORD = "admin123"

    while True:
        print("\nMenu:")
        print("1. Listar Produtos")
        print("2. Adicionar Produto ao Carrinho")
        print("3. Ver Carrinho")
        print("4. Pagar")
        print(f"5. {'Logout Admin' if admin_logado else 'Login Admin'}")
        if admin_logado:
            print("6. Cadastrar Mercadoria")
            print("7. Retirar Mercadoria")
            print("8. Alterar Preço da Mercadoria")
            print("9. Sair")
        else:
            print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            produtos = produto_service.listarProdutos()
            for produto in produtos:
                print(f"ID: {produto.id} | Nome: {produto.nome} | Preço: R${produto.preco} | Estoque: {produto.estoque} | Categoria: {produto.categoria}")
        
        elif escolha == '2':
            produto_id = safe_float_input("Digite o ID do produto: ")
            if produto_id is None:
                continue
            quantidade = safe_int_input("Digite a quantidade: ")
            if quantidade is None:
                continue
            resultado = adicionar_ao_carrinho(carrinho, produto_id, quantidade)
            print(resultado)

        elif escolha == '3':
            print("\nCarrinho:")
            for item in carrinho.itens:
                print(f"Produto ID: {item['produto_id']} | Quantidade: {item['quantidade']} | Preço: R${item['preco']:.2f} | Subtotal: R${item['subtotal']:.2f}")
            print(f"Total: R${carrinho.total():.2f}")
        elif escolha == '4':
            if not carrinho.itens:
                print("O carrinho está vazio. Adicione produtos antes de pagar.")
                continue

            print("\nMétodos de pagamento:")
            print("1. Cartão")
            print("2. Boleto")
            print("3. Pix")
            metodo = input("Escolha uma opção de pagamento: ")
            metodos = {
                '1': 'Cartão',
                '2': 'Boleto',
                '3': 'Pix'
            }
            metodo_escolhido = metodos.get(metodo)
            if metodo_escolhido is None:
                print("Método de pagamento inválido.")
                continue

            total = carrinho.finalizar_compra()
            print(f"Pagamento de R${total:.2f} realizado com {metodo_escolhido}. Obrigado pela compra!")
        elif escolha == '5':
            if not admin_logado:
                senha = input("Digite a senha do administrador: ")
                if senha == ADMIN_PASSWORD:
                    admin_logado = True
                    print("Login admin realizado com sucesso.")
                else:
                    print("Senha inválida. Acesso negado.")
            else:
                admin_logado = False
                print("Logout admin realizado.")
        elif escolha == '6' and admin_logado:
            produto_id = safe_float_input("Digite o ID do novo produto: ")
            if produto_id is None:
                continue
            if buscar_produto_por_id(produto_id) is not None:
                print("Já existe um produto com esse ID.")
                continue

            nome = input("Digite o nome do produto: ")
            preco = safe_float_input("Digite o preço do produto: ")
            if preco is None:
                continue
            estoque = safe_int_input("Digite a quantidade em estoque: ")
            if estoque is None:
                continue
            categoria = input("Digite a categoria do produto: ")
            produto_service.criarProduto(produto_id, nome, preco, estoque, categoria)
            print(f"Produto '{nome}' cadastrado com sucesso.")
        elif escolha == '7' and admin_logado:
            produto_id = safe_float_input("Digite o ID do produto a ser retirado: ")
            if produto_id is None:
                continue
            if buscar_produto_por_id(produto_id) is None:
                print("Produto não encontrado.")
                continue

            if deletar_produto(produto_id):
                print(f"Produto de ID {produto_id} retirado com sucesso.")
            else:
                print("Não foi possível retirar o produto.")
        elif escolha == '8' and admin_logado:
            produto_id = safe_float_input("Digite o ID do produto para alterar o preço: ")
            if produto_id is None:
                continue
            produto = buscar_produto_por_id(produto_id)
            if produto is None:
                print("Produto não encontrado.")
                continue

            novo_preco = safe_float_input(f"Digite o novo preço para {produto.nome}: ")
            if novo_preco is None:
                continue
            produto_atualizado = produto_service.atualizar_preco(produto_id, novo_preco)
            if produto_atualizado:
                print(f"Preço do produto '{produto_atualizado.nome}' atualizado para R${produto_atualizado.preco:.2f}.")
            else:
                print("Não foi possível atualizar o preço do produto.")
        elif (escolha == '6' and not admin_logado) or (escolha == '9' and admin_logado):
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()
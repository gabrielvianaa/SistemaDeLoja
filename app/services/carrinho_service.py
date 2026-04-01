from app.services.produto_service import buscar_produto_por_id, atualizar_estoque


def adicionar_ao_carrinho(carrinho, produto_id: float, quantidade: int) -> str:
    produto = buscar_produto_por_id(produto_id)
    if produto is None:
        return "Produto não encontrado."
    if quantidade <= 0:
        return "Quantidade deve ser maior que zero."
    if quantidade > produto.estoque:
        return "Quantidade indisponível em estoque."

    novo_estoque = produto.estoque - quantidade
    atualizar_estoque(produto.id, novo_estoque)
    carrinho.adicionar_item(produto, quantidade)
    return f"{quantidade}x {produto.nome} adicionado(s) ao carrinho."

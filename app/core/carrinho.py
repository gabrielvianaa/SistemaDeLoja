class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        produto.estoque -= quantidade
        self.itens.append({
            "produto_id": produto.id,
            "quantidade": quantidade,
            "preco": produto.preco,
            "subtotal": produto.preco * quantidade,
        })

    def total(self):
        return sum(item["subtotal"] for item in self.itens)

    def finalizar_compra(self):
        total = self.total()
        self.itens.clear()
        return total

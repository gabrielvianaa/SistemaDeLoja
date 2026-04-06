class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        self.itens.append({
            "produto_id": produto['id'],
            "categoria": produto['categoria'],
            "quantidade": quantidade,
            "preco": produto['preco'],
            "subtotal": produto['preco'] * quantidade,
        })

    def total(self):
        return sum(item["subtotal"] for item in self.itens)

    def remover_item(self, produto_id, quantidade):
        for item in self.itens:
            if item["produto_id"] == produto_id:
                if quantidade >= item["quantidade"]:
                    removido = item["quantidade"]
                    self.itens.remove(item)
                else:
                    removido = quantidade
                    item["quantidade"] -= quantidade
                    item["subtotal"] = item["preco"] * item["quantidade"]
                return removido
        return 0

    def finalizar_compra(self):
        total = self.total()
        self.itens.clear()
        return total

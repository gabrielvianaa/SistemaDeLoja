from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List
import json

METODOS_DISPONIVEIS = ["Cartao de Credito", "Cartao de Debito", "Parcelado", "Boleto", "Pix"]
METODOS_CARTAO = {"Cartao de Credito", "Parcelado"}  # methods that need card details

_DB_DIR = Path(__file__).resolve().parent.parent / "database"


_DESCONTOS_FILE = _DB_DIR / "descontos.json"

_DEFAULTS_DESCONTO: dict = {
    "Cartao de Credito": 0.0,
    "Cartao de Debito":  0.0,
    "Parcelado":         0.0,
    "Boleto":            0.05,
    "Pix":               0.10,
}


def _load_descontos() -> dict:
    if _DESCONTOS_FILE.exists():
        try:
            data = json.loads(_DESCONTOS_FILE.read_text(encoding="utf-8"))
            return {m: data.get(m, _DEFAULTS_DESCONTO[m]) for m in METODOS_DISPONIVEIS}
        except Exception:
            pass
    return dict(_DEFAULTS_DESCONTO)


def _save_descontos() -> None:
    _DESCONTOS_FILE.write_text(
        json.dumps(DESCONTOS, indent=2, ensure_ascii=False), encoding="utf-8"
    )


DESCONTOS: dict = _load_descontos()


def get_desconto(metodo: str) -> float:
    return DESCONTOS.get(metodo, 0.0)


def set_desconto(metodo: str, pct: float) -> None:
    if metodo not in METODOS_DISPONIVEIS:
        raise ValueError(f"Metodo invalido: {metodo}")
    if not (0.0 <= pct <= 1.0):
        raise ValueError("Desconto deve estar entre 0% e 100%.")
    DESCONTOS[metodo] = pct
    _save_descontos()


_PARCELAS_FILE = _DB_DIR / "parcelas.json"

_DEFAULTS_PARCELAS: dict = {
    "max_parcelas": 12,
    "sem_juros_ate": 3,      
    "tipo_taxa": "juros",    
    "taxa_mensal": 0.02,     
}


def _load_parcelas() -> dict:
    if _PARCELAS_FILE.exists():
        try:
            data = json.loads(_PARCELAS_FILE.read_text(encoding="utf-8"))
            cfg = dict(_DEFAULTS_PARCELAS)
            cfg.update({k: data[k] for k in _DEFAULTS_PARCELAS if k in data})
            return cfg
        except Exception:
            pass
    return dict(_DEFAULTS_PARCELAS)


def _save_parcelas() -> None:
    _PARCELAS_FILE.write_text(
        json.dumps(PARCELAS, indent=2, ensure_ascii=False), encoding="utf-8"
    )


PARCELAS: dict = _load_parcelas()


def get_parcelas_config() -> dict:
    return dict(PARCELAS)


def set_parcelas_config(max_parcelas: int, sem_juros_ate: int,
                        tipo_taxa: str, taxa_mensal: float) -> None:
    if max_parcelas < 1 or max_parcelas > 24:
        raise ValueError("Numero de parcelas deve ser entre 1 e 24.")
    if sem_juros_ate < 0 or sem_juros_ate > max_parcelas:
        raise ValueError("'Sem juros ate' deve estar entre 0 e o maximo de parcelas.")
    if tipo_taxa not in ("juros", "desconto"):
        raise ValueError("Tipo de taxa deve ser 'juros' ou 'desconto'.")
    if not (0.0 <= taxa_mensal <= 1.0):
        raise ValueError("Taxa mensal deve estar entre 0% e 100%.")
    PARCELAS["max_parcelas"] = max_parcelas
    PARCELAS["sem_juros_ate"] = sem_juros_ate
    PARCELAS["tipo_taxa"] = tipo_taxa
    PARCELAS["taxa_mensal"] = taxa_mensal
    _save_parcelas()


def calcular_parcelas(subtotal: float) -> list:
    
    cfg = PARCELAS
    resultado = []
    for n in range(1, cfg["max_parcelas"] + 1):
        if n <= cfg["sem_juros_ate"]:
            taxa = 0.0
            total = subtotal
        else:
            meses_com_taxa = n - cfg["sem_juros_ate"]
            taxa = cfg["taxa_mensal"] * meses_com_taxa
            if cfg["tipo_taxa"] == "juros":
                total = subtotal * (1 + taxa)
            else:
                total = subtotal * (1 - taxa)
        valor_parcela = total / n
        if n <= cfg["sem_juros_ate"] or taxa == 0:
            sufixo = "sem juros"
        elif cfg["tipo_taxa"] == "juros":
            total_taxa = taxa * 100
            sufixo = f"+{total_taxa:.1f}% juros"
        else:
            total_taxa = taxa * 100
            sufixo = f"-{total_taxa:.1f}% desc."
        label = f"{n}x  R${valor_parcela:.2f}  ({sufixo})  Total: R${total:.2f}"
        resultado.append({"n": n, "valor_parcela": valor_parcela,
                          "total": total, "taxa": taxa, "label": label})
    return resultado



@dataclass
class ItemPedido:
    produto_id: float
    nome: str
    categoria: str
    quantidade: int
    preco_unitario: float
    subtotal: float


@dataclass
class Pedido:
    metodo: str
    itens: List[ItemPedido]
    subtotal_original: float
    desconto_pct: float
    desconto_valor: float
    total: float
    parcelas: int = 1
    valor_parcela: float = 0.0
    data: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M"))

    def resumo(self) -> str:
        linhas = [f"Pedido em {self.data}", f"Metodo: {self.metodo}", ""]
        for item in self.itens:
            linhas.append(
                f"  {item.nome} ({item.categoria})  x{item.quantidade}"
                f"  —  R${item.subtotal:.2f}"
            )
        linhas.append("")
        linhas.append(f"Subtotal:  R${self.subtotal_original:.2f}")
        if self.desconto_pct > 0:
            linhas.append(f"Desconto ({int(self.desconto_pct * 100)}%):  -R${self.desconto_valor:.2f}")
        linhas.append(f"Total pago:  R${self.total:.2f}")
        if self.parcelas > 1:
            linhas.append(f"Parcelado em {self.parcelas}x de R${self.valor_parcela:.2f}")
        return "\n".join(linhas)


def processar_pagamento(carrinho, metodo: str, parcelas: int = 1) -> "Pedido":
    if metodo not in METODOS_DISPONIVEIS:
        raise ValueError(f"Metodo de pagamento invalido: {metodo}")
    if not carrinho.itens:
        raise ValueError("Carrinho esta vazio.")

    itens_pedido = [
        ItemPedido(
            produto_id=item["produto_id"],
            nome=item.get("nome", ""),
            categoria=item["categoria"],
            quantidade=item["quantidade"],
            preco_unitario=item["preco"],
            subtotal=item["subtotal"],
        )
        for item in carrinho.itens
    ]

    subtotal_original = carrinho.total()


    if metodo in METODOS_CARTAO and parcelas > 1:
        opts = calcular_parcelas(subtotal_original)
        opt = next((o for o in opts if o["n"] == parcelas), opts[0])
        total = opt["total"]
        valor_parcela = opt["valor_parcela"]
        desconto_pct = 0.0
        desconto_valor = 0.0
        if opt["taxa"] != 0:
            cfg = PARCELAS
            if cfg["tipo_taxa"] == "desconto":
                desconto_pct = opt["taxa"]
                desconto_valor = subtotal_original * desconto_pct
    else:
        desconto_pct = get_desconto(metodo)
        desconto_valor = subtotal_original * desconto_pct
        total = subtotal_original - desconto_valor
        valor_parcela = total

    carrinho.finalizar_compra()

    return Pedido(
        metodo=metodo,
        itens=itens_pedido,
        subtotal_original=subtotal_original,
        desconto_pct=desconto_pct,
        desconto_valor=desconto_valor,
        total=total,
        parcelas=parcelas,
        valor_parcela=valor_parcela,
    )


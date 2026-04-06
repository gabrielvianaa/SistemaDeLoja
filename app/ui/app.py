import customtkinter as ctk
from tkinter import messagebox

from app.services import produto_service
from app.services.carrinho_service import adicionar_ao_carrinho
from app.services.produto_service import buscar_produto_por_id, deletar_produto
from app.services import admin_service
from app.services.pagamento_service import (
    processar_pagamento, METODOS_DISPONIVEIS, METODOS_CARTAO,
    get_desconto, set_desconto,
    get_parcelas_config, set_parcelas_config, calcular_parcelas,
)
from app.core.carrinho import Carrinho
from app.database.models import Categoria
from app.database.connection import SessionLocal


class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Loja")
        self.root.geometry("960x620")
        self.root.minsize(800, 520)
        self.carrinho = Carrinho()
        self.admin_logado = False
        self._build_layout()


    def _build_layout(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)


        self.header = ctk.CTkFrame(self.root, height=56, corner_radius=0, fg_color="#1e1d2e")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_propagate(False)

        ctk.CTkLabel(
            self.header, text="  Loja",
            font=ctk.CTkFont("Arial", 20, "bold"), text_color="#f3f4f6",
        ).pack(side="left", padx=16)

        self.lbl_status = ctk.CTkLabel(
            self.header, text="Visitante",
            font=ctk.CTkFont("Arial", 13), text_color="#8d8980",
        )
        self.lbl_status.pack(side="right", padx=20)


        self.sidebar = ctk.CTkFrame(self.root, width=230, corner_radius=0, fg_color="#2c2a40")
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.content = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#1e1d2e")
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.footer = ctk.CTkFrame(self.root, height=42, corner_radius=0, fg_color="#2c2a40")
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.footer.grid_propagate(False)

        self.lbl_cart = ctk.CTkLabel(
            self.footer,
            text="Carrinho vazio",
            font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
        )
        self.lbl_cart.pack(side="left", padx=20, pady=10)

        self._build_sidebar()
        self._show_welcome()


    def _build_sidebar(self):
        for w in self.sidebar.winfo_children():
            w.destroy()

        W, H, PY = 210, 38, 2

        def nav_btn(text, cmd, color="#d1d5db", danger=False):
            fg = "#3b1515" if danger else "transparent"
            hv = "#5c2020" if danger else "#3f3d58"
            tc = "#f87171" if danger else color
            ctk.CTkButton(
                self.sidebar, text=text, width=W, height=H,
                anchor="w", fg_color=fg, hover_color=hv,
                text_color=tc, font=ctk.CTkFont("Arial", 13),
                command=cmd, corner_radius=8,
            ).pack(pady=PY, padx=10)

        def section_label(text):
            ctk.CTkLabel(
                self.sidebar, text=text,
                font=ctk.CTkFont("Arial", 10, "bold"), text_color="#575267",
            ).pack(pady=(14, 2), padx=16, anchor="w")

        def divider():
            ctk.CTkFrame(self.sidebar, height=1, fg_color="#3f3d58").pack(fill="x", padx=14, pady=8)

        section_label("LOJA")
        nav_btn("Listar Produtos",       self._view_produtos)
        nav_btn("Ver Carrinho",          self._view_carrinho)
        nav_btn("Adicionar ao Carrinho", self._dialog_adicionar_carrinho)

        divider()

        if not self.admin_logado:
            nav_btn("Login Admin", self._dialog_login, color="#8d8980")
        else:
            section_label("ADMIN")
            nav_btn("Cadastrar Mercadoria",  self._dialog_cadastrar_produto)
            nav_btn("Retirar Mercadoria",    self._dialog_retirar_produto)
            nav_btn("Alterar Preco",         self._dialog_alterar_preco)
            divider()
            nav_btn("Criar Admin",           self._dialog_criar_admin)
            nav_btn("Listar Admins",         self._view_admins)
            nav_btn("Configurar Descontos",     self._dialog_descontos)
            nav_btn("Configurar Parcelamento",  self._dialog_parcelas)
            nav_btn("Logout",                self._logout, color="#f87171")

        nav_btn("Sair", self.root.quit, danger=True)


    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _content_frame(self, title):
        self._clear_content()
        outer = ctk.CTkFrame(self.content, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=28, pady=22)
        ctk.CTkLabel(
            outer, text=title,
            font=ctk.CTkFont("Arial", 20, "bold"), text_color="#f3f4f6",
        ).pack(anchor="w", pady=(0, 14))
        return outer

    def _table_header(self, parent, columns):
        hdr = ctk.CTkFrame(parent, fg_color="#575267", corner_radius=6)
        hdr.pack(fill="x", pady=(0, 3))
        for label, width in columns:
            ctk.CTkLabel(
                hdr, text=label, width=width, anchor="w",
                font=ctk.CTkFont("Arial", 12, "bold"), text_color="#b0adc8",
            ).pack(side="left", padx=10, pady=7)

    def _table_row(self, parent, values, columns, even):
        row = ctk.CTkFrame(parent, fg_color="#2e2c44" if even else "#242238", corner_radius=4)
        row.pack(fill="x", pady=1)
        for (label, width), val in zip(columns, values):
            color = val[1] if isinstance(val, tuple) else "#d1d5db"
            text  = val[0] if isinstance(val, tuple) else str(val)
            ctk.CTkLabel(
                row, text=text, width=width, anchor="w",
                font=ctk.CTkFont("Arial", 12), text_color=color,
            ).pack(side="left", padx=10, pady=6)

    def _update_cart_bar(self):
        n = len(self.carrinho.itens)
        if n == 0:
            self.lbl_cart.configure(text="Carrinho vazio", text_color="#8d8980")
        else:
            total = self.carrinho.total()
            self.lbl_cart.configure(
                text=f"{n} {'item' if n == 1 else 'itens'}  |  Total: R${total:.2f}",
                text_color="#6ee7b7",
            )


    def _show_welcome(self):
        self._clear_content()
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.place(relx=0.5, rely=0.46, anchor="center")


        icons = ["🛍️", "🛒", "🏪", "🛍️", "✨", "🛒"]
        lbl_icon = ctk.CTkLabel(frame, text="🛍️", font=ctk.CTkFont("Arial", 56))
        lbl_icon.pack(pady=(0, 6))


        title_colors = ["#3d3b54", "#575267", "#7a7890", "#a8a5be", "#ccc9e0", "#f3f4f6"]
        lbl_title = ctk.CTkLabel(
            frame, text="Bem-vindo a Loja",
            font=ctk.CTkFont("Arial", 30, "bold"), text_color="#3d3b54",
        )
        lbl_title.pack(pady=(0, 6))

        lbl_sub = ctk.CTkLabel(
            frame, text="Selecione uma opcao no menu lateral para comecar.",
            font=ctk.CTkFont("Arial", 13), text_color="#706e78",
        )
        lbl_sub.pack()


        sep = ctk.CTkFrame(frame, fg_color="#860029", height=3, corner_radius=2)
        sep.pack(pady=(10, 0))
        sep.configure(width=0)


        _icon_step = [0]
        _fade_step = [0]
        _sep_width = [0]

        def _animate_icon():
            _icon_step[0] = (_icon_step[0] + 1) % len(icons)
            try:
                lbl_icon.configure(text=icons[_icon_step[0]])
                frame.after(700, _animate_icon)
            except Exception:
                pass

        def _animate_fade():
            if _fade_step[0] < len(title_colors):
                try:
                    lbl_title.configure(text_color=title_colors[_fade_step[0]])
                    _fade_step[0] += 1
                    frame.after(80, _animate_fade)
                except Exception:
                    pass

        def _animate_sep():
            if _sep_width[0] < 340:
                _sep_width[0] = min(_sep_width[0] + 20, 340)
                try:
                    sep.configure(width=_sep_width[0])
                    frame.after(18, _animate_sep)
                except Exception:
                    pass

        frame.after(80, _animate_fade)
        frame.after(100, _animate_sep)
        frame.after(900, _animate_icon)


    def _view_produtos(self):
        outer = self._content_frame("Produtos Disponiveis")
        cols = [("Nome", 260), ("Categoria", 170), ("Preco", 120), ("Estoque", 95)]
        scroll = ctk.CTkScrollableFrame(outer, fg_color="#282636", corner_radius=8)
        scroll.pack(fill="both", expand=True)
        self._table_header(scroll, cols)
        produtos = produto_service.listarProdutos()
        if not produtos:
            ctk.CTkLabel(scroll, text="Nenhum produto cadastrado.", text_color="#706e78").pack(pady=24)
            return
        for i, p in enumerate(produtos):
            estoque_color = "#f87171" if p["estoque"] < 5 else "#d1d5db"
            self._table_row(scroll, [
                p["nome"],
                (p["categoria"], "#b0adc8"),
                (f"R${p['preco']:.2f}", "#6ee7b7"),
                (str(p["estoque"]), estoque_color),
            ], cols, i % 2 == 0)

    def _view_carrinho(self):
        outer = self._content_frame("Meu Carrinho")
        if not self.carrinho.itens:
            ctk.CTkLabel(
                outer, text="Seu carrinho esta vazio.",
                font=ctk.CTkFont("Arial", 14), text_color="#706e78",
            ).pack(expand=True)
            return

        selected_pid = [None]
        selected_frames = {}

        cols = [("Nome", 240), ("Categoria", 150), ("Qtd", 60), ("Preco", 115), ("Subtotal", 125)]

        scroll = ctk.CTkScrollableFrame(outer, fg_color="#282636", corner_radius=8)
        scroll.pack(fill="both", expand=True)

        # ── header ──
        hdr = ctk.CTkFrame(scroll, fg_color="#575267", corner_radius=6)
        hdr.pack(fill="x", pady=(0, 3))
        for label, width in cols:
            ctk.CTkLabel(
                hdr, text=label, width=width, anchor="w",
                font=ctk.CTkFont("Arial", 12, "bold"), text_color="#b0adc8",
            ).pack(side="left", padx=10, pady=7)

        def refresh_rows():
            # rebuild rows in-place after a removal
            for key in list(selected_frames.keys()):
                selected_frames[key][0].destroy()
                del selected_frames[key]
            selected_pid[0] = None
            lbl_sel.configure(text="Selecione um item")
            lbl_err.configure(text="")
            e_qty.delete(0, "end")
            btn_remove.configure(state="disabled")
            lbl_total.configure(
                text=f"Total:  R${self.carrinho.total():.2f}" if self.carrinho.itens else "Carrinho vazio"
            )
  
            if not self.carrinho.itens:
                self._view_carrinho()
                return
            build_rows()

        def select_row(pid):
            selected_pid[0] = pid
            for p_id, (row_frame, _) in selected_frames.items():
                keys = list(selected_frames.keys())
                bg = "#67648a" if p_id == pid else ("#2e2c44" if keys.index(p_id) % 2 == 0 else "#242238")
                row_frame.configure(fg_color=bg)
            item = next((it for it in self.carrinho.itens if it["produto_id"] == pid), None)
            if item:
                prod = buscar_produto_por_id(pid)
                nome = prod["nome"] if prod else "Produto"
                lbl_sel.configure(text=f"{nome}  —  {item['quantidade']} un. no carrinho")
            lbl_err.configure(text="")
            btn_remove.configure(state="normal")

        def build_rows():
            for i, item in enumerate(self.carrinho.itens):
                even = i % 2 == 0
                bg = "#2e2c44" if even else "#242238"
                prod = buscar_produto_por_id(item["produto_id"])
                nome = prod["nome"] if prod else "Produto"
                row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=4, cursor="hand2")
                row.pack(fill="x", pady=1)
                values = [
                    nome,
                    item["categoria"],
                    str(item["quantidade"]),
                    f"R${item['preco']:.2f}",
                    f"R${item['subtotal']:.2f}",
                ]
                colors = ["#f3f4f6", "#b0adc8", "#d1d5db", "#d1d5db", "#6ee7b7"]
                for (_, width), text, color in zip(cols, values, colors):
                    ctk.CTkLabel(
                        row, text=text, width=width, anchor="w",
                        font=ctk.CTkFont("Arial", 12), text_color=color,
                    ).pack(side="left", padx=10, pady=6)
                pid = item["produto_id"]
                selected_frames[pid] = (row, values)
                row.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))
                for child in row.winfo_children():
                    child.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))

        build_rows()

        
        total_bar = ctk.CTkFrame(outer, fg_color="#575267", height=42, corner_radius=8)
        total_bar.pack(fill="x", pady=(6, 4))
        total_bar.pack_propagate(False)
        lbl_total = ctk.CTkLabel(
            total_bar,
            text=f"Total:  R${self.carrinho.total():.2f}",
            font=ctk.CTkFont("Arial", 15, "bold"), text_color="#6ee7b7",
        )
        lbl_total.pack(side="right", padx=20, pady=10)

       
        bottom = ctk.CTkFrame(outer, fg_color="#2c2a40", corner_radius=8)
        bottom.pack(fill="x", pady=(0, 2))

        lbl_sel = ctk.CTkLabel(
            bottom, text="Selecione um item",
            font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
        )
        lbl_sel.pack(side="left", padx=14, pady=10)

        lbl_err = ctk.CTkLabel(
            bottom, text="",
            font=ctk.CTkFont("Arial", 11), text_color="#f87171",
        )
        lbl_err.pack(side="left", padx=6, pady=10)

        def do_remove():
            pid = selected_pid[0]
            if pid is None:
                return
            item = next((it for it in self.carrinho.itens if it["produto_id"] == pid), None)
            if not item:
                return
            raw = e_qty.get().strip()
            try:
                qty = int(raw) if raw else item["quantidade"]
                if qty <= 0:
                    raise ValueError
            except ValueError:
                lbl_err.configure(text="Quantidade invalida.")
                return
            from app.services.produto_service import atualizar_estoque, buscar_produto_por_id as _bpp
            prod = _bpp(pid)
            removido = self.carrinho.remover_item(pid, qty)
            if prod and removido:
                atualizar_estoque(pid, prod["estoque"] + removido)
            self._update_cart_bar()
            refresh_rows()

        ctk.CTkLabel(
            bottom, text="Qtd a remover:",
            font=ctk.CTkFont("Arial", 12), text_color="#d1d5db",
        ).pack(side="right", padx=(0, 6), pady=10)

        e_qty = ctk.CTkEntry(bottom, width=62, height=32, placeholder_text="tudo")
        e_qty.pack(side="right", pady=10)

        btn_remove = ctk.CTkButton(
            bottom, text="Remover do Carrinho", height=32, width=180,
            fg_color="#7f1d1d", hover_color="#5c1414",
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=do_remove, corner_radius=8, state="disabled",
        )
        btn_remove.pack(side="right", padx=14, pady=10)

        checkout_bar = ctk.CTkFrame(outer, fg_color="transparent")
        checkout_bar.pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(
            checkout_bar,
            text="Selecione o metodo e finalize:",
            font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
        ).pack(side="left", padx=14)

        combo_metodo = ctk.CTkComboBox(
            checkout_bar, values=METODOS_DISPONIVEIS,
            state="readonly", width=190, height=34,
            command=lambda _: update_checkout_preview(),
        )
        combo_metodo.set(METODOS_DISPONIVEIS[0])
        combo_metodo.pack(side="left", padx=(6, 0))

        lbl_checkout_info = ctk.CTkLabel(
            checkout_bar, text="",
            font=ctk.CTkFont("Arial", 11), text_color="#fbbf24",
        )
        lbl_checkout_info.pack(side="left", padx=10)

        def update_checkout_preview():
            metodo = combo_metodo.get()
            subtotal = self.carrinho.total()
            if metodo in METODOS_CARTAO:
                opts = calcular_parcelas(subtotal)
                cfg = get_parcelas_config()
                max_p = cfg["max_parcelas"]
                opt1 = opts[0]
                lbl_total.configure(text=f"Total:  R${opt1['total']:.2f}")
                lbl_checkout_info.configure(
                    text=f"Parcelavel em ate {max_p}x  —  clique em Finalizar para detalhes",
                    text_color="#b0adc8",
                )
            else:
                pct = get_desconto(metodo)
                total_final = subtotal * (1 - pct)
                lbl_total.configure(text=f"Total:  R${total_final:.2f}")
                if pct > 0:
                    lbl_checkout_info.configure(
                        text=f"{int(pct*100)}% desc.  economia R${subtotal*pct:.2f}",
                        text_color="#fbbf24",
                    )
                else:
                    lbl_checkout_info.configure(text="")

        update_checkout_preview()

        def confirmar_compra():
            metodo = combo_metodo.get()
            if metodo in METODOS_CARTAO:
                self._dialog_cartao(metodo, lbl_err)
            else:
                try:
                    pedido = processar_pagamento(self.carrinho, metodo)
                except ValueError as ex:
                    lbl_err.configure(text=str(ex))
                    return
                self._update_cart_bar()
                self._show_success(pedido)

        ctk.CTkButton(
            checkout_bar, text="Finalizar Compra", height=34, width=160,
            fg_color="#15803d", hover_color="#166534",
            font=ctk.CTkFont("Arial", 13, "bold"),
            command=confirmar_compra, corner_radius=8,
        ).pack(side="right", padx=14)

    def _view_admins(self):
        outer = self._content_frame("Administradores")
        cols = [("ID", 60), ("Username", 200), ("Email", 300)]
        scroll = ctk.CTkScrollableFrame(outer, fg_color="#282636", corner_radius=8)
        scroll.pack(fill="both", expand=True)
        self._table_header(scroll, cols)
        admins = admin_service.listar_admins()
        if not admins:
            ctk.CTkLabel(scroll, text="Nenhum admin cadastrado.", text_color="#706e78").pack(pady=24)
            return
        for i, a in enumerate(admins):
            self._table_row(scroll, [
                str(a.id),
                (a.username, "#f3f4f6"),
                (a.email or "---", "#b0adc8"),
            ], cols, i % 2 == 0)


    def _form_card(self, title, back_fn=None, back_label="← Voltar"):
        outer = self._content_frame(title)
        if back_fn:
            ctk.CTkButton(
                outer, text=back_label, width=110, height=28, anchor="w",
                fg_color="transparent", hover_color="#3f3d58",
                font=ctk.CTkFont("Arial", 12), text_color="#706e78",
                command=back_fn, corner_radius=6,
            ).pack(anchor="w", pady=(0, 10))
        card = ctk.CTkFrame(outer, fg_color="#282636", corner_radius=12)
        card.pack(anchor="nw", fill="x")
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(padx=36, pady=22, fill="x")
        return outer, body

    def _ifield(self, parent, label, placeholder="", show=""):
        ctk.CTkLabel(parent, text=label, anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
                     ).pack(fill="x", pady=(6, 0))
        e = ctk.CTkEntry(parent, placeholder_text=placeholder, show=show, height=38)
        e.pack(fill="x", pady=(2, 2))
        return e

    def _ifield_password(self, parent, label, placeholder="********"):
        """Password field with eye toggle button."""
        ctk.CTkLabel(parent, text=label, anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
                     ).pack(fill="x", pady=(6, 0))
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(2, 2))
        e = ctk.CTkEntry(row, placeholder_text=placeholder, show="*", height=38)
        e.pack(side="left", fill="x", expand=True)
        _visible = [False]
        def toggle():
            _visible[0] = not _visible[0]
            e.configure(show="" if _visible[0] else "*")
            btn.configure(text="�" if _visible[0] else "👁̸")
        btn = ctk.CTkButton(
            row, text="👁̸", width=42, height=38,
            fg_color="#3f3d58", hover_color="#575267",
            font=ctk.CTkFont("Arial", 16), text_color="#8d8980",
            command=toggle, corner_radius=8,
        )
        btn.pack(side="left", padx=(4, 0))
        return e

    def _ierr(self, parent):
        lbl = ctk.CTkLabel(parent, text="", font=ctk.CTkFont("Arial", 11), text_color="#f87171")
        lbl.pack(anchor="w", pady=(4, 0))
        return lbl

    def _ibtn(self, parent, text, cmd, danger=False):
        fg = "#991b1b" if danger else "#860029"
        hv = "#7f1d1d" if danger else "#5e001c"
        ctk.CTkButton(
            parent, text=text, height=40,
            fg_color=fg, hover_color=hv,
            font=ctk.CTkFont("Arial", 13, "bold"),
            command=cmd, corner_radius=8,
        ).pack(fill="x", pady=(12, 4))


    def _dialog_login(self):
        outer, body = self._form_card("Login Admin")
        e_user = self._ifield(body, "Username", "admin")
        e_pass = self._ifield_password(body, "Senha")
        lbl    = self._ierr(body)

        def ok():
            if admin_service.autenticar_admin(e_user.get(), e_pass.get()):
                self.admin_logado = True
                self.lbl_status.configure(
                    text=f"{e_user.get()} (Admin)", text_color="#6ee7b7"
                )
                self._build_sidebar()
                self._show_welcome()
            else:
                e_pass.delete(0, "end")
                lbl.configure(text="Username ou senha incorretos.")

        e_pass.bind("<Return>", lambda _: ok())
        self._ibtn(body, "Entrar", ok)

    def _dialog_adicionar_carrinho(self):
        produtos = produto_service.listarProdutos()
        outer = self._content_frame("Adicionar ao Carrinho")
        if not produtos:
            ctk.CTkLabel(outer, text="Nenhum produto disponivel.", text_color="#706e78").pack(pady=24)
            return

        selected_id    = [None]
        selected_frames = {}
        cols = [("Nome", 230), ("Categoria", 150), ("Preco", 110), ("Disponivel", 100)]
        estoque_map = {p["id"]: p["estoque"] for p in produtos}

        list_outer = ctk.CTkFrame(outer, fg_color="#282636", corner_radius=8)
        list_outer.pack(fill="both", expand=True)

        hdr = ctk.CTkFrame(list_outer, fg_color="#575267", corner_radius=6)
        hdr.pack(fill="x", padx=4, pady=(4, 0))
        for label, width in cols:
            ctk.CTkLabel(hdr, text=label, width=width, anchor="w",
                         font=ctk.CTkFont("Arial", 11, "bold"), text_color="#b0adc8",
                         ).pack(side="left", padx=8, pady=5)

        scroll = ctk.CTkScrollableFrame(list_outer, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=4, pady=(2, 4))

        def select_row(pid):
            selected_id[0] = pid
            keys = list(selected_frames.keys())
            for p_id, (rf, _) in selected_frames.items():
                bg = "#67648a" if p_id == pid else (
                    "#2e2c44" if keys.index(p_id) % 2 == 0 else "#242238")
                rf.configure(fg_color=bg)
            lbl_err.configure(text="")
            disponivel = estoque_map.get(pid, 0)
            lbl_disp.configure(
                text=f"Disponivel: {disponivel}",
                text_color="#f87171" if disponivel < 5 else "#6ee7b7",
            )

        for i, p in enumerate(produtos):
            even = i % 2 == 0
            bg = "#2e2c44" if even else "#242238"
            row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=4, cursor="hand2")
            row.pack(fill="x", pady=1)
            row_values = [p["nome"], p["categoria"], f"R${p['preco']:.2f}", f"{p['estoque']} un."]
            colors = ["#f3f4f6", "#b0adc8", "#6ee7b7",
                      "#f87171" if p["estoque"] < 5 else "#8d8980"]
            for (_, width), text, color in zip(cols, row_values, colors):
                ctk.CTkLabel(row, text=text, width=width, anchor="w",
                             font=ctk.CTkFont("Arial", 12), text_color=color,
                             ).pack(side="left", padx=8, pady=6)
            pid = p["id"]
            selected_frames[pid] = (row, row_values)
            row.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))

        bottom = ctk.CTkFrame(outer, fg_color="#2c2a40", corner_radius=8)
        bottom.pack(fill="x", pady=(6, 0))

        ctk.CTkLabel(bottom, text="Quantidade:",
                     font=ctk.CTkFont("Arial", 13), text_color="#d1d5db",
                     ).pack(side="left", padx=(14, 6), pady=10)
        e_qty = ctk.CTkEntry(bottom, width=72, height=34, placeholder_text="1")
        e_qty.pack(side="left", pady=10)

        lbl_disp = ctk.CTkLabel(bottom, text="Selecione um produto",
                                font=ctk.CTkFont("Arial", 11), text_color="#706e78")
        lbl_disp.pack(side="left", padx=12, pady=10)

        lbl_err = ctk.CTkLabel(bottom, text="",
                               font=ctk.CTkFont("Arial", 11), text_color="#f87171")
        lbl_err.pack(side="left", padx=4, pady=10)

        def ok():
            if selected_id[0] is None:
                lbl_err.configure(text="Selecione um produto.")
                return
            try:
                qty = int(e_qty.get()) if e_qty.get().strip() else 1
                if qty <= 0:
                    raise ValueError
            except ValueError:
                lbl_err.configure(text="Quantidade invalida.")
                return
            resultado = adicionar_ao_carrinho(self.carrinho, selected_id[0], qty)
            if "adicionado" in resultado.lower():
                self._update_cart_bar()
                self._view_carrinho()
            else:
                lbl_err.configure(text=resultado)

        ctk.CTkButton(bottom, text="Adicionar ao Carrinho", height=34, width=200,
                      fg_color="#860029", hover_color="#5e001c",
                      font=ctk.CTkFont("Arial", 13, "bold"),
                      command=ok, corner_radius=8,
                      ).pack(side="right", padx=14, pady=10)

    def _dialog_cadastrar_produto(self):
        session = SessionLocal()
        try:
            cat_nomes = [c.nome for c in session.query(Categoria).all()]
        finally:
            session.close()

        if not cat_nomes:
            outer = self._content_frame("Cadastrar Mercadoria")
            ctk.CTkLabel(outer, text="Nenhuma categoria encontrada.", text_color="#f87171").pack(pady=24)
            return

        outer, body = self._form_card("Cadastrar Mercadoria", back_fn=self._view_produtos)

        ctk.CTkLabel(body, text="Categoria", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980").pack(fill="x", pady=(6, 0))
        combo = ctk.CTkComboBox(body, values=cat_nomes, state="readonly", height=38)
        combo.pack(fill="x", pady=(2, 4))
        combo.set(cat_nomes[0])

        e_nome = self._ifield(body, "Nome do Produto", "ex: RTX 4090")

        row_lbl = ctk.CTkFrame(body, fg_color="transparent")
        row_lbl.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row_lbl, text="Preco (R$)", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980").pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(row_lbl, text="Estoque", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980").pack(side="left", expand=True, fill="x", padx=(10, 0))
        row_ent = ctk.CTkFrame(body, fg_color="transparent")
        row_ent.pack(fill="x", pady=(2, 4))
        e_preco   = ctk.CTkEntry(row_ent, height=38, placeholder_text="ex: 1500.00")
        e_preco.pack(side="left", expand=True, fill="x")
        e_estoque = ctk.CTkEntry(row_ent, height=38, placeholder_text="ex: 10")
        e_estoque.pack(side="left", expand=True, fill="x", padx=(10, 0))

        lbl = self._ierr(body)

        def ok():
            nome = e_nome.get().strip()
            if not nome:
                lbl.configure(text="Informe o nome do produto.")
                return
            try:
                preco   = float(e_preco.get())
                estoque = int(e_estoque.get())
            except ValueError:
                lbl.configure(text="Preco ou estoque invalidos.")
                return
            try:
                produto_service.criarProduto(combo.get(), nome, preco, estoque)
                self._view_produtos()
            except ValueError as e:
                lbl.configure(text=str(e))

        self._ibtn(body, "Cadastrar", ok)

    def _dialog_retirar_produto(self):
        produtos = produto_service.listarProdutos()
        outer = self._content_frame("Retirar Mercadoria")
        if not produtos:
            ctk.CTkLabel(outer, text="Nenhum produto cadastrado.", text_color="#706e78").pack(pady=24)
            return

        ctk.CTkLabel(outer, text="Selecione o produto a retirar do estoque",
                     font=ctk.CTkFont("Arial", 12), text_color="#706e78",
                     ).pack(anchor="w", pady=(0, 10))

        selected_id    = [None]
        selected_frames = {}
        cols = [("Nome", 230), ("Categoria", 150), ("Preco", 110), ("Estoque", 90)]

        list_outer = ctk.CTkFrame(outer, fg_color="#282636", corner_radius=8)
        list_outer.pack(fill="both", expand=True)

        hdr = ctk.CTkFrame(list_outer, fg_color="#575267", corner_radius=6)
        hdr.pack(fill="x", padx=4, pady=(4, 0))
        for label, width in cols:
            ctk.CTkLabel(hdr, text=label, width=width, anchor="w",
                         font=ctk.CTkFont("Arial", 11, "bold"), text_color="#b0adc8",
                         ).pack(side="left", padx=8, pady=5)

        scroll = ctk.CTkScrollableFrame(list_outer, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=4, pady=(2, 4))

        def select_row(pid):
            selected_id[0] = pid
            keys = list(selected_frames.keys())
            for p_id, (rf, _) in selected_frames.items():
                bg = "#3b1515" if p_id == pid else (
                    "#2e2c44" if keys.index(p_id) % 2 == 0 else "#242238")
                rf.configure(fg_color=bg)
            prod = next((p for p in produtos if p["id"] == pid), None)
            if prod:
                lbl_sel.configure(text=f"Selecionado: {prod['nome']}", text_color="#fbbf24")
            lbl_err.configure(text="")
            btn_del.configure(state="normal")

        for i, p in enumerate(produtos):
            even = i % 2 == 0
            bg = "#2e2c44" if even else "#242238"
            row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=4, cursor="hand2")
            row.pack(fill="x", pady=1)
            values = [p["nome"], p["categoria"], f"R${p['preco']:.2f}", str(p["estoque"])]
            colors = ["#f3f4f6", "#b0adc8", "#6ee7b7",
                      "#f87171" if p["estoque"] < 5 else "#8d8980"]
            for (_, width), text, color in zip(cols, values, colors):
                ctk.CTkLabel(row, text=text, width=width, anchor="w",
                             font=ctk.CTkFont("Arial", 12), text_color=color,
                             ).pack(side="left", padx=8, pady=6)
            pid = p["id"]
            selected_frames[pid] = (row, values)
            row.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))

        bottom = ctk.CTkFrame(outer, fg_color="#2c2a40", corner_radius=8)
        bottom.pack(fill="x", pady=(6, 0))

        lbl_sel = ctk.CTkLabel(bottom, text="Nenhum produto selecionado",
                               font=ctk.CTkFont("Arial", 12), text_color="#8d8980")
        lbl_sel.pack(side="left", padx=14, pady=10)

        lbl_err = ctk.CTkLabel(bottom, text="",
                               font=ctk.CTkFont("Arial", 11), text_color="#f87171")
        lbl_err.pack(side="left", padx=4, pady=10)

        def do_delete():
            if selected_id[0] is None:
                return
            if deletar_produto(selected_id[0]):
                self._view_produtos()
            else:
                lbl_err.configure(text="Nao foi possivel retirar.")

        btn_del = ctk.CTkButton(
            bottom, text="Retirar do Estoque", height=32, width=180,
            fg_color="#7f1d1d", hover_color="#5c1414",
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=do_delete, corner_radius=8, state="disabled",
        )
        btn_del.pack(side="right", padx=14, pady=10)

    def _dialog_alterar_preco(self):
        produtos = produto_service.listarProdutos()
        outer = self._content_frame("Alterar Preco")
        if not produtos:
            ctk.CTkLabel(outer, text="Nenhum produto cadastrado.", text_color="#706e78").pack(pady=24)
            return

        ctk.CTkLabel(outer, text="Clique em um produto para seleciona-lo",
                     font=ctk.CTkFont("Arial", 12), text_color="#706e78",
                     ).pack(anchor="w", pady=(0, 10))

        selected_id    = [None]
        selected_frames = {}
        cols = [("Nome", 230), ("Categoria", 150), ("Preco Atual", 120), ("Estoque", 90)]

        list_outer = ctk.CTkFrame(outer, fg_color="#282636", corner_radius=8)
        list_outer.pack(fill="both", expand=True)

        hdr = ctk.CTkFrame(list_outer, fg_color="#575267", corner_radius=6)
        hdr.pack(fill="x", padx=4, pady=(4, 0))
        for label, width in cols:
            ctk.CTkLabel(hdr, text=label, width=width, anchor="w",
                         font=ctk.CTkFont("Arial", 11, "bold"), text_color="#b0adc8",
                         ).pack(side="left", padx=8, pady=5)

        scroll = ctk.CTkScrollableFrame(list_outer, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=4, pady=(2, 4))

        def select_row(pid):
            selected_id[0] = pid
            keys = list(selected_frames.keys())
            for p_id, (rf, _) in selected_frames.items():
                bg = "#67648a" if p_id == pid else (
                    "#2e2c44" if keys.index(p_id) % 2 == 0 else "#242238")
                rf.configure(fg_color=bg)
            prod = next((p for p in produtos if p["id"] == pid), None)
            if prod:
                lbl_sel.configure(
                    text=f"Selecionado: {prod['nome']}  —  Preco atual: R${prod['preco']:.2f}",
                    text_color="#6ee7b7",
                )
            lbl_err.configure(text="")

        for i, p in enumerate(produtos):
            even = i % 2 == 0
            bg = "#2e2c44" if even else "#242238"
            row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=4, cursor="hand2")
            row.pack(fill="x", pady=1)
            values = [p["nome"], p["categoria"], f"R${p['preco']:.2f}", str(p["estoque"])]
            colors = ["#f3f4f6", "#b0adc8", "#6ee7b7",
                      "#f87171" if p["estoque"] < 5 else "#8d8980"]
            for (_, width), text, color in zip(cols, values, colors):
                ctk.CTkLabel(row, text=text, width=width, anchor="w",
                             font=ctk.CTkFont("Arial", 12), text_color=color,
                             ).pack(side="left", padx=8, pady=6)
            pid = p["id"]
            selected_frames[pid] = (row, values)
            row.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, _pid=pid: select_row(_pid))

        bottom = ctk.CTkFrame(outer, fg_color="#2c2a40", corner_radius=8)
        bottom.pack(fill="x", pady=(6, 0))

        lbl_sel = ctk.CTkLabel(bottom, text="Nenhum produto selecionado",
                               font=ctk.CTkFont("Arial", 12), text_color="#8d8980")
        lbl_sel.pack(side="left", padx=14, pady=10)

        lbl_err = ctk.CTkLabel(bottom, text="",
                               font=ctk.CTkFont("Arial", 11), text_color="#f87171")
        lbl_err.pack(side="left", padx=4, pady=10)

        ctk.CTkLabel(bottom, text="Novo preco (R$):",
                     font=ctk.CTkFont("Arial", 12), text_color="#d1d5db",
                     ).pack(side="right", padx=(0, 6), pady=10)
        e_preco = ctk.CTkEntry(bottom, width=120, height=32, placeholder_text="ex: 1200.00")
        e_preco.pack(side="right", pady=10)

        def ok():
            if selected_id[0] is None:
                lbl_err.configure(text="Selecione um produto.")
                return
            try:
                novo = float(e_preco.get().strip().replace(",", "."))
                if novo <= 0:
                    raise ValueError
            except ValueError:
                lbl_err.configure(text="Preco invalido.")
                return
            if produto_service.atualizar_preco(selected_id[0], novo):
                self._view_produtos()
            else:
                lbl_err.configure(text="Nao foi possivel atualizar.")

        ctk.CTkButton(bottom, text="Salvar", height=32, width=120,
                      fg_color="#860029", hover_color="#5e001c",
                      font=ctk.CTkFont("Arial", 12, "bold"),
                      command=ok, corner_radius=8,
                      ).pack(side="right", padx=14, pady=10)

    def _dialog_criar_admin(self):
        outer, body = self._form_card("Criar Admin", back_fn=self._view_admins)

        e_u  = self._ifield(body, "Username", "novo_admin")
        e_p  = self._ifield_password(body, "Senha")
        e_em = self._ifield(body, "Email (opcional)", "admin@loja.com")
        lbl  = self._ierr(body)

        def ok():
            u  = e_u.get().strip()
            p  = e_p.get()
            em = e_em.get().strip() or None
            if not u or not p:
                lbl.configure(text="Username e senha sao obrigatorios.")
                return
            try:
                admin_service.criar_admin(u, p, em)
                self._view_admins()
            except Exception as e:
                lbl.configure(text=str(e))

        self._ibtn(body, "Criar Admin", ok)


    def _show_success(self, pedido):
        self._clear_content()
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.place(relx=0.5, rely=0.44, anchor="center")

        # Animated emoji
        emojis = ["🎉", "🎊", "✨", "🎊", "🎉"]
        lbl_emoji = ctk.CTkLabel(
            frame, text="🎉",
            font=ctk.CTkFont("Arial", 72),
        )
        lbl_emoji.pack()

        lbl_msg = ctk.CTkLabel(
            frame, text="Compra finalizada com sucesso!",
            font=ctk.CTkFont("Arial", 26, "bold"), text_color="#6ee7b7",
        )
        lbl_msg.pack(pady=(8, 4))

        ctk.CTkLabel(
            frame,
            text=f"Total pago: R${pedido.total:.2f}  via {pedido.metodo}",
            font=ctk.CTkFont("Arial", 14), text_color="#d1d5db",
        ).pack(pady=(0, 4))

        if pedido.parcelas > 1:
            ctk.CTkLabel(
                frame,
                text=f"Parcelado em {pedido.parcelas}x de R${pedido.valor_parcela:.2f}",
                font=ctk.CTkFont("Arial", 13), text_color="#b0adc8",
            ).pack(pady=(0, 4))

        if pedido.desconto_pct > 0:
            ctk.CTkLabel(
                frame,
                text=f"Voce economizou R${pedido.desconto_valor:.2f} ({int(pedido.desconto_pct*100)}% de desconto)",
                font=ctk.CTkFont("Arial", 13), text_color="#fbbf24",
            ).pack(pady=(0, 16))

        ctk.CTkButton(
            frame, text="Voltar ao inicio", width=200, height=36,
            fg_color="#860029", hover_color="#5e001c",
            font=ctk.CTkFont("Arial", 13, "bold"),
            command=self._show_welcome, corner_radius=8,
        ).pack(pady=(8, 0))


        _step = [0]
        def _animate():
            _step[0] = (_step[0] + 1) % len(emojis)
            try:
                lbl_emoji.configure(text=emojis[_step[0]])
                self.root.after(400, _animate)
            except Exception:
                pass
        self.root.after(400, _animate)


    def _dialog_cartao(self, metodo: str, lbl_err_cart=None):
        subtotal = self.carrinho.total()
        opts = calcular_parcelas(subtotal)

        outer, body = self._form_card(
            "Dados do Cartao",
            back_fn=self._view_carrinho,
            back_label="← Voltar ao Carrinho",
        )

        ctk.CTkLabel(
            body, text=f"Subtotal: R${subtotal:.2f}  |  Metodo: {metodo}",
            font=ctk.CTkFont("Arial", 12), text_color="#706e78",
        ).pack(anchor="w", pady=(0, 10))

        def ifield(label, placeholder="", show=""):
            ctk.CTkLabel(body, text=label, anchor="w",
                         font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
                         ).pack(fill="x", pady=(6, 0))
            e = ctk.CTkEntry(body, placeholder_text=placeholder, show=show, height=38)
            e.pack(fill="x", pady=(2, 2))
            return e

        e_num  = ifield("Numero do Cartao", "0000 0000 0000 0000")
        e_nome = ifield("Nome no Cartao", "NOME SOBRENOME")

        row2 = ctk.CTkFrame(body, fg_color="transparent")
        row2.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row2, text="Validade", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980").pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(row2, text="CVV", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980").pack(side="left", expand=True, fill="x", padx=(10, 0))
        row2e = ctk.CTkFrame(body, fg_color="transparent")
        row2e.pack(fill="x", pady=(2, 4))
        e_val = ctk.CTkEntry(row2e, height=38, placeholder_text="MM/AA")
        e_val.pack(side="left", expand=True, fill="x")
        cvv_wrap = ctk.CTkFrame(row2e, fg_color="transparent")
        cvv_wrap.pack(side="left", expand=True, fill="x", padx=(10, 0))
        e_cvv = ctk.CTkEntry(cvv_wrap, height=38, placeholder_text="CVV", show="*")
        e_cvv.pack(side="left", fill="x", expand=True)
        _cvv_vis = [False]
        def _toggle_cvv():
            _cvv_vis[0] = not _cvv_vis[0]
            e_cvv.configure(show="" if _cvv_vis[0] else "*")
            btn_cvv.configure(text="👁" if _cvv_vis[0] else "👁̸")
        btn_cvv = ctk.CTkButton(
            cvv_wrap, text="👁̸", width=42, height=38,
            fg_color="#3f3d58", hover_color="#575267",
            font=ctk.CTkFont("Arial", 16), text_color="#8d8980",
            command=_toggle_cvv, corner_radius=8,
        )
        btn_cvv.pack(side="left", padx=(4, 0))

        ctk.CTkLabel(body, text="Parcelamento", anchor="w",
                     font=ctk.CTkFont("Arial", 12), text_color="#8d8980",
                     ).pack(fill="x", pady=(6, 0))
        parcelas_labels = [o["label"] for o in opts]
        combo_parc = ctk.CTkComboBox(body, values=parcelas_labels, state="readonly", height=38)
        combo_parc.set(parcelas_labels[0])
        combo_parc.pack(fill="x", pady=(2, 4))

        lbl_err = self._ierr(body)

        def validate_card_number(num: str) -> bool:
            digits = num.replace(" ", "")
            return digits.isdigit() and len(digits) == 16

        def validate_expiry(val: str) -> bool:
            import re
            return bool(re.match(r"^(0[1-9]|1[0-2])/\d{2}$", val.strip()))

        def confirm():
            num  = e_num.get().strip()
            nome = e_nome.get().strip()
            val  = e_val.get().strip()
            cvv  = e_cvv.get().strip()
            if not validate_card_number(num):
                lbl_err.configure(text="Numero do cartao invalido (deve ter 16 digitos).")
                return
            if not nome:
                lbl_err.configure(text="Informe o nome no cartao.")
                return
            if not validate_expiry(val):
                lbl_err.configure(text="Validade invalida (use MM/AA, ex: 12/27).")
                return
            if not cvv.isdigit() or len(cvv) not in (3, 4):
                lbl_err.configure(text="CVV invalido (3 ou 4 digitos).")
                return
            idx = combo_parc.get()
            n_parcelas = opts[parcelas_labels.index(idx)]["n"]
            try:
                pedido = processar_pagamento(self.carrinho, metodo, parcelas=n_parcelas)
            except ValueError as ex:
                lbl_err.configure(text=str(ex))
                return
            self._update_cart_bar()
            self._show_success(pedido)

        self._ibtn(body, "Confirmar Pagamento", confirm)


    def _dialog_descontos(self):
        outer, body = self._form_card("Configurar Descontos", back_fn=self._show_welcome)
        ctk.CTkLabel(
            body, text="Define o % de desconto por metodo (0 a 100)",
            font=ctk.CTkFont("Arial", 11), text_color="#706e78",
        ).pack(anchor="w", pady=(0, 10))

        entries = {}
        for metodo in [m for m in METODOS_DISPONIVEIS if m != "Parcelado"]:
            row = ctk.CTkFrame(body, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row, text=metodo, width=200, anchor="w",
                font=ctk.CTkFont("Arial", 13), text_color="#d1d5db",
            ).pack(side="left")
            e = ctk.CTkEntry(row, width=90, height=32)
            e.insert(0, str(int(get_desconto(metodo) * 100)))
            e.pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row, text="%", text_color="#8d8980",
                         font=ctk.CTkFont("Arial", 13)).pack(side="left", padx=4)
            entries[metodo] = e

        lbl_status = ctk.CTkLabel(
            body, text="",
            font=ctk.CTkFont("Arial", 11), text_color="#f87171",
        )
        lbl_status.pack(anchor="w", pady=(6, 0))

        def salvar():
            try:
                for metodo, e in entries.items():
                    pct = float(e.get())
                    if not (0 <= pct <= 100):
                        raise ValueError(f"{metodo}: valor fora do intervalo 0-100.")
                    set_desconto(metodo, pct / 100)
            except ValueError as ex:
                lbl_status.configure(text=str(ex), text_color="#f87171")
                return
            lbl_status.configure(text="Descontos salvos com sucesso!", text_color="#6ee7b7")

        self._ibtn(body, "Salvar", salvar)


    def _dialog_parcelas(self):
        cfg = get_parcelas_config()
        outer, body = self._form_card("Configurar Parcelamento", back_fn=self._show_welcome)
        ctk.CTkLabel(
            body, text="Configuracoes de parcelamento no cartao",
            font=ctk.CTkFont("Arial", 11), text_color="#706e78",
        ).pack(anchor="w", pady=(0, 10))

        def row_entry(label, val, placeholder=""):
            r = ctk.CTkFrame(body, fg_color="transparent")
            r.pack(fill="x", pady=3)
            ctk.CTkLabel(r, text=label, width=260, anchor="w",
                         font=ctk.CTkFont("Arial", 12), text_color="#d1d5db").pack(side="left")
            e = ctk.CTkEntry(r, width=130, height=32, placeholder_text=placeholder)
            e.insert(0, str(val))
            e.pack(side="left", padx=(8, 0))
            return e

        e_max   = row_entry("Maximo de parcelas", cfg["max_parcelas"], "ex: 12")
        e_sjate = row_entry("Sem juros ate (parcelas)", cfg["sem_juros_ate"], "ex: 3")
        e_taxa  = row_entry("Taxa de juros por parcela (%)", int(cfg["taxa_mensal"] * 100), "ex: 2")

        lbl_status = ctk.CTkLabel(
            body, text="",
            font=ctk.CTkFont("Arial", 11), text_color="#f87171",
        )
        lbl_status.pack(anchor="w", pady=(6, 0))

        def salvar():
            try:
                max_p = int(e_max.get())
                sja   = int(e_sjate.get())
                taxa  = float(e_taxa.get()) / 100.0
                set_parcelas_config(max_p, sja, "juros", taxa)
            except ValueError as ex:
                lbl_status.configure(text=str(ex), text_color="#f87171")
                return
            lbl_status.configure(text="Configuracao salva com sucesso!", text_color="#6ee7b7")

        self._ibtn(body, "Salvar", salvar)


    def _logout(self):
        self.admin_logado = False
        self.lbl_status.configure(text="Visitante", text_color="#8d8980")
        self._build_sidebar()
        self._show_welcome()
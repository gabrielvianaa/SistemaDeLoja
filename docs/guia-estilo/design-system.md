# Guia de Estilo / Design System — Hardware Commerce
**Versão:** 2.0 | **Framework:** CustomTkinter (Python Desktop)

---

## 1. Identidade Visual

O Hardware Commerce adota um tema **dark mode exclusivo**, com paleta inspirada em ambientes de terminal profissional. O visual remete ao universo de hardware e tecnologia: sóbrio, denso de informação, com acentos de cor funcionais.

---

## 2. Paleta de Cores

### Cores Base

| Token | Hex | Uso |
|-------|-----|-----|
| `bg-primary` | `#1e1d2e` | Fundo principal, área de conteúdo, header |
| `bg-secondary` | `#2c2a40` | Sidebar, footer, cards e barras |
| `bg-tertiary` | `#282636` | Fundos de tabelas e listas scrolláveis |
| `bg-row-even` | `#2e2c44` | Linhas pares de tabela |
| `bg-row-odd` | `#242238` | Linhas ímpares de tabela |
| `bg-row-selected` | `#67648a` | Linha selecionada |
| `bg-header-row` | `#575267` | Cabeçalho de tabela |

### Cores de Texto

| Token | Hex | Uso |
|-------|-----|-----|
| `text-primary` | `#f3f4f6` | Títulos, nomes de produtos, texto principal |
| `text-secondary` | `#d1d5db` | Quantidades, campos gerais |
| `text-muted` | `#8d8980` | Labels de formulário, status "Visitante", hints |
| `text-disabled` | `#706e78` | Texto inativo, textos de seção da sidebar |
| `text-category` | `#b0adc8` | Categoria, informações secundárias |
| `text-section` | `#575267` | Labels de seção da sidebar |

### Cores Semânticas

| Token | Hex | Uso |
|-------|-----|-----|
| `accent-primary` | `#860029` | Botão primário (fundo) |
| `accent-primary-hover` | `#5e001c` | Botão primário hover |
| `accent-success` | `#6ee7b7` | Preços, totais, confirmações, admin logado |
| `accent-warning` | `#fbbf24` | Descontos, alertas de seleção |
| `accent-error` | `#f87171` | Erros, estoque baixo, ações destrutivas |
| `accent-info` | `#a5b4fc` | Usuário logado, links |
| `accent-danger-bg` | `#3b1515` | Fundo de botão de perigo |
| `accent-danger-hover` | `#5c2020` | Hover de botão de perigo |
| `accent-remove-bg` | `#7f1d1d` | Botão remover do carrinho |
| `accent-checkout` | `#15803d` | Botão finalizar compra |
| `accent-checkout-hover` | `#166534` | Hover finalizar compra |

### Bordas e Separadores

| Token | Hex | Uso |
|-------|-----|-----|
| `border-sidebar` | `#3f3d58` | Dividers da sidebar |
| `border-table-header` | `#575267` | Fundo do header de tabela |

---

## 3. Tipografia

O sistema utiliza **Arial** como família tipográfica exclusiva (disponibilidade garantida em Windows, Linux e macOS).

### Escala Tipográfica

| Nível | Tamanho | Peso | Cor | Uso |
|-------|---------|------|-----|-----|
| Display | 30px | Bold | `#3d3b54` → `#f3f4f6` (animado) | Título da tela de boas-vindas |
| H1 / Título de tela | 20px | Bold | `#f3f4f6` | Cabeçalho de cada view (`_content_frame`) |
| Body / Nav button | 13px | Regular | `#d1d5db` | Botões da sidebar, textos gerais |
| Table header | 12px | Bold | `#b0adc8` | Cabeçalhos de colunas |
| Table body | 12px | Regular | varia | Conteúdo de células |
| Form label | 12px | Regular | `#8d8980` | Labels acima de campos |
| Button primary | 13px | Bold | `#ffffff` | Texto de botões primários |
| Hint / Error | 11px | Regular | `#f87171` / `#706e78` | Mensagens de erro, dicas |
| Section label | 10px | Bold | `#575267` | Labels de seção da sidebar |

---

## 4. Componentes

### Botão Primário (Ação Principal)

```
Dimensões:  altura 40px, largura fill (formulários) ou fixa
Background: #860029
Hover:      #5e001c
Texto:      13px bold, branco
Radius:     8px
```

### Botão Secundário / Navegação (Sidebar)

```
Dimensões:  210 × 38px
Background: transparent
Hover:      #3f3d58
Texto:      13px, #d1d5db, alinhado à esquerda
Radius:     8px
```

### Botão Destrutivo (Remover / Sair)

```
Background: #3b1515
Hover:      #5c2020
Texto:      #f87171
```

### Campo de Entrada (Entry)

```
Altura:       38px
Placeholder:  texto em #8d8980
Radius:       padrão CTk (8px)
```

### Toggle de Senha

```
Botão:        42 × 38px, fg=#3f3d58, hover=#575267
Ícone OFF:    👁̸ (senha oculta)
Ícone ON:     👁  (senha visível)
```

### Tabela de Dados

```
Fundo geral:      #282636, radius 8
Header row:       #575267, radius 6, padding 10px H × 7px V
Linha par:        #2e2c44
Linha ímpar:      #242238
Linha selecionada: #67648a
Padding de célula: 10px H × 6px V
```

### Tab (TabView)

```
fg_color:                          #282636
segmented_button_fg_color:         #2c2a40
segmented_button_selected_color:   #860029
segmented_button_selected_hover:   #5e001c
segmented_button_unselected_color: #2c2a40
segmented_button_unselected_hover: #3f3d58
text_color:                        #d1d5db
corner_radius:                     10
```

### ComboBox (Seletor)

```
Altura:      38px (formulários) / 34px (checkout bar)
State:       readonly
```

### Barra de Rodapé (Cart Bar)

```
Altura:      42px
Background:  #2c2a40
Vazio:       "Carrinho vazio" — 12px, #8d8980
Com itens:   "N itens | Total: R$X.XX" — #6ee7b7
```

---

## 5. Layout e Espaçamento

### Grid Principal

```
Header:      row=0, columnspan=2, height=56px
Sidebar:     row=1, column=0, width=230px
Conteúdo:    row=1, column=1, expande
Footer:      row=2, columnspan=2, height=42px
```

### Espaçamentos Internos

| Contexto | Valor |
|----------|-------|
| Padding externo da view de conteúdo | 28px H, 22px V |
| Espaço após título de view | 14px |
| Padding interno de cards de formulário | 36px H, 22px V |
| Espaço entre itens da sidebar | 2px (pady) |
| Padding lateral dos botões da sidebar | 10px |
| Espaço entre campos de formulário | 6px topo |
| Padding interno das barras de ação | 14px H, 10px V |

---

## 6. Animações

| Animação | Duração | Elemento | Técnica |
|----------|---------|----------|---------|
| Fade-in título boas-vindas | 480ms total (6 × 80ms) | Label título | Troca de `text_color` |
| Expansão da barra decorativa | ~300ms (20px/18ms até 340px) | Frame separator | Troca de `width` |
| Rotação de emoji (boas-vindas) | 700ms/frame | Label emoji | Troca de `text` |
| Rotação de emoji (sucesso) | 400ms/frame | Label emoji | Troca de `text` |

Todas as animações usam o método `.after()` do Tkinter com try/except para prevenir erros após destruição de widgets.

---

## 7. Ícones e Símbolos

O sistema utiliza **emoji Unicode** para ícones visuais (compatível com todos os SOs suportados):

| Ícone | Uso |
|-------|-----|
| 🛍️ | Ícone principal do sistema (boas-vindas) |
| 🛒 | Variação no ciclo de animação |
| 🏪 | Variação no ciclo de animação |
| ✨ | Variação no ciclo de animação |
| 🎉 | Sucesso de compra |
| 🎊 | Variação ciclo sucesso |
| 👁 | Toggle senha visível |
| 👁̸ | Toggle senha oculta |

---

## 8. Estados de Interface

| Estado | Indicação Visual |
|--------|-----------------|
| Visitante | Status header: "Visitante" (#8d8980); sem "Ver Carrinho" na sidebar |
| Usuário logado | Status header: "[Nome Sobrenome]" (#a5b4fc); exibe "Ver Carrinho" |
| Admin logado | Status header: "[username] (Admin)" (#6ee7b7); seção ADMIN na sidebar |
| Estoque baixo | Quantidade em vermelho `#f87171` |
| Estoque OK | Quantidade em cinza `#d1d5db` |
| Botão desabilitado | `state="disabled"` — aparência nativa CTk |
| Linha selecionada | Fundo `#67648a` (neutro/roxo) |
| Linha destrutiva selecionada | Fundo `#3b1515` (vermelho escuro) |

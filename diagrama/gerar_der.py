#!/usr/bin/env python3
"""
Gerador do Diagrama Entidade-Relacionamento — Barbearia Pro
Execute: python3 gerar_der.py
Tire um print/screenshot da janela para usar como der.png
"""

import tkinter as tk

# ── Paleta de cores ──────────────────────────────────────────
BG        = "#1a1a2e"
C_HEADER  = "#e94560"
C_BODY    = "#16213e"
C_TEXT    = "#ffffff"
C_PK      = "#f39c12"
C_FK      = "#3498db"
C_ATTR    = "#bdc3c7"
C_LINE    = "#e94560"
C_LABEL   = "#ecf0f1"

# ── Entidades: (x, y, largura, altura, nome, [(campo, tipo, nota)]) ──
ENTITIES = [
    # (cx, cy, w, h, name, fields)
    (130, 120, 220, 180, "USUARIOS", [
        ("id",         "SERIAL",       "PK"),
        ("username",   "VARCHAR(50)",  "UNIQUE"),
        ("senha",      "VARCHAR(64)",  "SHA-256"),
        ("nivel",      "VARCHAR(20)",  ""),
        ("criado_em",  "TIMESTAMP",    ""),
    ]),
    (130, 400, 220, 200, "CLIENTES", [
        ("id",               "SERIAL",       "PK"),
        ("nome",             "VARCHAR(100)", "NOT NULL"),
        ("telefone",         "VARCHAR(20)",  ""),
        ("email",            "VARCHAR(100)", ""),
        ("data_nascimento",  "DATE",         ""),
        ("criado_em",        "TIMESTAMP",    ""),
    ]),
    (460, 120, 230, 200, "BARBEIROS", [
        ("id",            "SERIAL",       "PK"),
        ("nome",          "VARCHAR(100)", "NOT NULL"),
        ("especialidade", "VARCHAR(100)", ""),
        ("telefone",      "VARCHAR(20)",  ""),
        ("ativo",         "BOOLEAN",      "DEFAULT TRUE"),
        ("criado_em",     "TIMESTAMP",    ""),
    ]),
    (790, 120, 230, 190, "SERVICOS", [
        ("id",          "SERIAL",      "PK"),
        ("nome",        "VARCHAR(100)","NOT NULL"),
        ("preco",       "NUMERIC(8,2)","CHECK > 0"),
        ("duracao_min", "INTEGER",     "CHECK > 0"),
        ("criado_em",   "TIMESTAMP",   ""),
    ]),
    (460, 420, 260, 230, "AGENDAMENTOS", [
        ("id",          "SERIAL",     "PK"),
        ("cliente_id",  "INTEGER",    "FK → clientes"),
        ("barbeiro_id", "INTEGER",    "FK → barbeiros"),
        ("servico_id",  "INTEGER",    "FK → servicos"),
        ("data_hora",   "TIMESTAMP",  "NOT NULL"),
        ("status",      "VARCHAR(20)","agendado|concluido|cancelado"),
        ("observacao",  "TEXT",       ""),
        ("criado_em",   "TIMESTAMP",  ""),
    ]),
]

HEADER_H = 32
ROW_H    = 22
PAD      = 10

def draw_entity(canvas, ex, ey, ew, eh, name, fields):
    """Desenha uma entidade (tabela) no canvas."""
    # Sombra
    canvas.create_rectangle(ex+4, ey+4, ex+ew+4, ey+eh+4,
                             fill="#000000", outline="", stipple="gray25")
    # Corpo
    canvas.create_rectangle(ex, ey, ex+ew, ey+eh,
                             fill=C_BODY, outline=C_LINE, width=2)
    # Cabeçalho
    canvas.create_rectangle(ex, ey, ex+ew, ey+HEADER_H,
                             fill=C_HEADER, outline=C_LINE, width=2)
    canvas.create_text(ex + ew//2, ey + HEADER_H//2,
                       text=name, fill=WHITE, font=("Helvetica", 11, "bold"))

    # Campos
    for i, (fname, ftype, fnote) in enumerate(fields):
        row_y = ey + HEADER_H + i * ROW_H
        # Zebra
        if i % 2 == 0:
            canvas.create_rectangle(ex+1, row_y, ex+ew-1, row_y+ROW_H,
                                     fill="#1f2a48", outline="")

        # Ícone PK / FK
        if fnote.startswith("PK"):
            tag_color, tag = C_PK, "🔑"
        elif fnote.startswith("FK"):
            tag_color, tag = C_FK, "🔗"
        else:
            tag_color, tag = C_ATTR, "  "

        canvas.create_text(ex + PAD + 6, row_y + ROW_H//2,
                           text=tag, fill=tag_color,
                           font=("Helvetica", 9), anchor="w")
        canvas.create_text(ex + PAD + 22, row_y + ROW_H//2,
                           text=fname, fill=C_TEXT,
                           font=("Helvetica", 9, "bold"), anchor="w")
        canvas.create_text(ex + ew - PAD, row_y + ROW_H//2,
                           text=ftype, fill=C_ATTR,
                           font=("Helvetica", 8), anchor="e")


def center_of(entity):
    ex, ey, ew, eh, *_ = entity
    return ex + ew//2, ey + eh//2

def bottom_center(entity):
    ex, ey, ew, eh, *_ = entity
    return ex + ew//2, ey + eh

def top_center(entity):
    ex, ey, ew, eh, *_ = entity
    return ex + ew//2, ey

def right_center(entity):
    ex, ey, ew, eh, *_ = entity
    return ex + ew, ey + eh//2

def left_center(entity):
    ex, ey, ew, eh, *_ = entity
    return ex, ey + eh//2

WHITE = "#ffffff"

def draw_arrow(canvas, x1, y1, x2, y2, label=""):
    canvas.create_line(x1, y1, x2, y2,
                       fill=C_LINE, width=2, dash=(6, 3),
                       arrow=tk.LAST, arrowshape=(10, 12, 4))
    if label:
        mx, my = (x1+x2)//2, (y1+y2)//2
        canvas.create_rectangle(mx-22, my-9, mx+22, my+9,
                                 fill=BG, outline=C_LINE, width=1)
        canvas.create_text(mx, my, text=label, fill=C_LABEL,
                           font=("Helvetica", 8, "bold"))


def main():
    root = tk.Tk()
    root.title("DER — Barbearia Pro")
    root.configure(bg=BG)

    W, H = 1080, 720
    root.geometry(f"{W}x{H}")

    canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Título
    canvas.create_text(W//2, 24, text="✂  BARBEARIA PRO — Diagrama Entidade-Relacionamento",
                       fill=C_HEADER, font=("Helvetica", 14, "bold"))

    # Calcular altura real de cada entidade
    sized = []
    for ex, ey, ew, _, name, fields in ENTITIES:
        eh = HEADER_H + len(fields) * ROW_H + 4
        sized.append((ex, ey, ew, eh, name, fields))

    # Desenhar entidades
    for ent in sized:
        ex, ey, ew, eh, name, fields = ent
        draw_entity(canvas, ex, ey, ew, eh, name, fields)

    # Atalhos para os índices
    USUARIOS, CLIENTES, BARBEIROS, SERVICOS, AGENDAMENTOS = sized

    # Relacionamentos (setas de FK para tabela referenciada)
    # CLIENTES → AGENDAMENTOS (bottom de clientes → left de agendamentos)
    x1, y1 = bottom_center(CLIENTES)
    x2, y2 = left_center(AGENDAMENTOS)
    draw_arrow(canvas, x1, y1, x2, y2, "1:N")

    # BARBEIROS → AGENDAMENTOS (bottom de barbeiros → top de agendamentos)
    x1, y1 = bottom_center(BARBEIROS)
    x2, y2 = top_center(AGENDAMENTOS)
    draw_arrow(canvas, x1, y1, x2, y2, "1:N")

    # SERVICOS → AGENDAMENTOS
    x1, y1 = bottom_center(SERVICOS)
    bx, by = bottom_center(AGENDAMENTOS)
    # vai até mesma linha de agendamentos topo-direita
    x2 = AGENDAMENTOS[0] + AGENDAMENTOS[2]   # right edge x
    y2 = AGENDAMENTOS[1] + HEADER_H + 3 * ROW_H  # ~ servico_id row
    draw_arrow(canvas, x1, y1, x2, y2, "1:N")

    # Legenda
    lx, ly = 790, 380
    canvas.create_rectangle(lx, ly, lx+220, ly+110,
                             fill=C_BODY, outline=C_LINE, width=1)
    canvas.create_text(lx+110, ly+14, text="LEGENDA",
                       fill=C_HEADER, font=("Helvetica", 10, "bold"))
    for i, (symbol, desc, color) in enumerate([
        ("🔑", "Chave Primária (PK)", C_PK),
        ("🔗", "Chave Estrangeira (FK)", C_FK),
        ("---►", "Relacionamento 1:N", C_LINE),
    ]):
        canvas.create_text(lx+14, ly+36+i*24, text=symbol,
                           fill=color, font=("Helvetica", 10), anchor="w")
        canvas.create_text(lx+44, ly+36+i*24, text=desc,
                           fill=C_LABEL, font=("Helvetica", 9), anchor="w")

    tk.Button(root, text="✕  Fechar", bg=C_HEADER, fg=WHITE,
              font=("Helvetica", 10, "bold"), relief="flat",
              cursor="hand2", command=root.destroy,
              padx=12, pady=4).place(x=W-110, y=H-40)

    root.mainloop()


if __name__ == "__main__":
    main()

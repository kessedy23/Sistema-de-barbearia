#!/usr/bin/env python3
"""
Sistema de Gestão de Barbearia
Disciplina: Banco de Dados — UNIFSA
Interface gráfica: Tkinter + PostgreSQL (psycopg2)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import hashlib

# ============================================================
#  CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================
DB = {
    "host":     "localhost",
    "database": "barbearia",
    "user":     "postgres",
    "password": "postgres",
    "port":     "5432",
}

def get_conn():
    return psycopg2.connect(**DB)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# ============================================================
#  PALETA DE CORES
# ============================================================
BG      = "#1a1a2e"
PANEL   = "#16213e"
ACCENT  = "#e94560"
WHITE   = "#ffffff"
LIGHT   = "#f4f6f8"
C_ADD   = "#2ecc71"
C_UPD   = "#3498db"
C_DEL   = "#e74c3c"
C_CLR   = "#95a5a6"
C_REP   = "#8e44ad"

# ============================================================
#  WIDGETS UTILITÁRIOS
# ============================================================
def _lbl(parent, text, bg=WHITE, **kw):
    return tk.Label(parent, text=text, bg=bg, font=("Helvetica", 9), **kw)

def _ent(parent, width=27):
    e = tk.Entry(parent, font=("Helvetica", 11), width=width, relief="solid", bd=1)
    e.pack(fill="x", pady=(1, 6))
    return e

def _btn(parent, text, color, cmd):
    b = tk.Button(parent, text=text, bg=color, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", command=cmd, pady=5)
    b.pack(fill="x", pady=2)
    return b

def _tree(parent, cols, heads, widths):
    f = tk.Frame(parent)
    f.pack(fill="both", expand=True)
    sy = ttk.Scrollbar(f, orient="vertical")
    sx = ttk.Scrollbar(f, orient="horizontal")
    tv = ttk.Treeview(f, columns=cols, show="headings",
                      yscrollcommand=sy.set, xscrollcommand=sx.set,
                      selectmode="browse")
    sy.config(command=tv.yview)
    sx.config(command=tv.xview)
    sy.pack(side="right", fill="y")
    sx.pack(side="bottom", fill="x")
    tv.pack(fill="both", expand=True)
    for col, head, w in zip(cols, heads, widths):
        tv.heading(col, text=head)
        tv.column(col, width=w, anchor="w", minwidth=40)
    return tv

# ============================================================
#  JANELA DE LOGIN
# ============================================================
class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Barbearia Pro — Login")
        self.root.geometry("420x320")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.eval("tk::PlaceWindow . center")

        tk.Label(self.root, text="✂  BARBEARIA PRO",
                 font=("Helvetica", 21, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(30, 4))
        tk.Label(self.root, text="Sistema de Gestão",
                 font=("Helvetica", 10), bg=BG, fg="#aaaaaa").pack()

        frm = tk.Frame(self.root, bg=PANEL, padx=30, pady=22)
        frm.pack(padx=36, pady=18, fill="x")

        for label, attr, kw in [("Usuário", "eu", {}),
                                  ("Senha",   "ep", {"show": "•"})]:
            tk.Label(frm, text=label, bg=PANEL, fg=WHITE,
                     font=("Helvetica", 9)).pack(anchor="w")
            e = tk.Entry(frm, font=("Helvetica", 12), relief="flat",
                         bg="#0f3460", fg=WHITE,
                         insertbackground=WHITE, **kw)
            e.pack(fill="x", ipady=5, pady=(2, 10))
            setattr(self, attr, e)

        tk.Button(frm, text="ENTRAR", bg=ACCENT, fg=WHITE,
                  font=("Helvetica", 11, "bold"), relief="flat",
                  cursor="hand2", command=self._login).pack(fill="x", ipady=7)

        self.ep.bind("<Return>", lambda _: self._login())
        self.eu.focus_set()
        self.root.mainloop()

    def _login(self):
        u = self.eu.get().strip()
        p = self.ep.get().strip()
        if not u or not p:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT id, username FROM usuarios WHERE username=%s AND senha=%s",
                (u, sha256(p))
            )
            row = cur.fetchone()
            c.close()
            if row:
                self.root.destroy()
                App(row)
            else:
                messagebox.showerror("Login", "Usuário ou senha incorretos!")
        except Exception as e:
            messagebox.showerror("Conexão",
                                  f"Não foi possível conectar ao banco:\n{e}\n\n"
                                  "Verifique as configurações em DB no topo do arquivo app.py")

# ============================================================
#  APLICAÇÃO PRINCIPAL
# ============================================================
class App:
    def __init__(self, user):
        self.root = tk.Tk()
        self.root.title(f"Barbearia Pro  —  {user[1]}")
        self.root.geometry("1100x670")
        self.root.configure(bg=BG)

        hdr = tk.Frame(self.root, bg=BG, height=52)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✂  BARBEARIA PRO",
                 font=("Helvetica", 15, "bold"),
                 bg=BG, fg=ACCENT).pack(side="left", padx=20, pady=10)
        tk.Label(hdr, text=f"Usuário: {user[1]}",
                 bg=BG, fg="#aaaaaa",
                 font=("Helvetica", 10)).pack(side="right", padx=20)
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x")

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=0)
        s.configure("TNotebook.Tab", background=PANEL, foreground=WHITE,
                    padding=[14, 7], font=("Helvetica", 10, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", WHITE)])
        s.configure("Treeview", rowheight=25, font=("Helvetica", 10),
                    background=WHITE, fieldbackground=WHITE)
        s.configure("Treeview.Heading", font=("Helvetica", 10, "bold"),
                    background=PANEL, foreground=WHITE)
        s.map("Treeview", background=[("selected", ACCENT)])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True)

        ClientesTab(nb)
        BarbeirosTab(nb)
        ServicosTab(nb)
        AgendamentosTab(nb)
        RelatoriosTab(nb)
        UsuariosTab(nb)

        self.root.mainloop()

# ============================================================
#  ABA: CLIENTES
# ============================================================
class ClientesTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Clientes  ")
        self.sid = None
        self._build()
        self.load()

    def _build(self):
        top = tk.Frame(self, bg=LIGHT, pady=7)
        top.pack(fill="x", padx=10)
        tk.Label(top, text="Buscar:", bg=LIGHT).pack(side="left")
        self.sv_q = tk.StringVar()
        tk.Entry(top, textvariable=self.sv_q, width=28,
                 font=("Helvetica", 10)).pack(side="left", padx=4)
        for txt, color, cmd in [("Buscar", C_UPD, self.search),
                                  ("Todos",  C_CLR, self.load)]:
            tk.Button(top, text=txt, bg=color, fg=WHITE,
                      font=("Helvetica", 9, "bold"), relief="flat",
                      cursor="hand2", command=cmd, padx=8).pack(side="left", padx=2)
        tk.Label(top, text="  Ordenar:", bg=LIGHT).pack(side="left", padx=(12, 2))
        self.sv_ord = tk.StringVar(value="nome")
        ttk.Combobox(top, textvariable=self.sv_ord,
                     values=["nome", "id", "email", "data_nascimento"],
                     width=14, state="readonly").pack(side="left")
        tk.Button(top, text="OK", bg=C_REP, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", padx=6,
                  command=lambda: self.load(self.sv_ord.get())).pack(side="left", padx=4)

        m = tk.Frame(self, bg=LIGHT)
        m.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        fm = tk.LabelFrame(m, text=" Dados do Cliente ", bg=WHITE,
                            font=("Helvetica", 10, "bold"), fg=BG,
                            padx=12, pady=8)
        fm.pack(side="left", fill="y", padx=(0, 8))

        for lbl_text, attr in [("Nome *", "en"), ("Telefone", "et"),
                                 ("E-mail", "ee"),
                                 ("Nascimento (AAAA-MM-DD)", "eb")]:
            _lbl(fm, lbl_text).pack(anchor="w")
            setattr(self, attr, _ent(fm))

        bf = tk.Frame(fm, bg=WHITE)
        bf.pack(fill="x", pady=(5, 0))
        _btn(bf, "➕  Adicionar", C_ADD, self.add)
        _btn(bf, "✏️  Atualizar",  C_UPD, self.update)
        _btn(bf, "🗑️  Excluir",   C_DEL, self.delete)
        _btn(bf, "🔄  Limpar",    C_CLR, self.clear)

        tf = tk.Frame(m, bg=LIGHT)
        tf.pack(side="right", fill="both", expand=True)
        self.tv = _tree(tf,
                        ("id", "nome", "telefone", "email", "nascimento"),
                        ("ID", "Nome", "Telefone", "E-mail", "Nascimento"),
                        [40, 200, 120, 220, 110])
        self.tv.bind("<<TreeviewSelect>>", self._sel)

    def load(self, order="nome"):
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                f"SELECT id,nome,telefone,email,data_nascimento "
                f"FROM clientes ORDER BY {order}"
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def search(self):
        q = self.sv_q.get().strip()
        if not q:
            self.load()
            return
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT id,nome,telefone,email,data_nascimento FROM clientes "
                "WHERE nome ILIKE %s OR telefone ILIKE %s OR email ILIKE %s "
                "ORDER BY nome",
                (f"%{q}%", f"%{q}%", f"%{q}%")
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _sel(self, _):
        s = self.tv.selection()
        if not s:
            return
        v = self.tv.item(s[0], "values")
        self.sid = v[0]
        for entry, val in zip([self.en, self.et, self.ee, self.eb], v[1:]):
            entry.delete(0, "end")
            entry.insert(0, val or "")

    def add(self):
        nome = self.en.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "INSERT INTO clientes(nome,telefone,email,data_nascimento) "
                "VALUES(%s,%s,%s,%s)",
                (nome, self.et.get() or None,
                 self.ee.get() or None, self.eb.get() or None)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        nome = self.en.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "UPDATE clientes SET nome=%s,telefone=%s,email=%s,"
                "data_nascimento=%s WHERE id=%s",
                (nome, self.et.get() or None, self.ee.get() or None,
                 self.eb.get() or None, self.sid)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Cliente atualizado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        if not messagebox.askyesno("Confirmar",
                                    "Excluir este cliente?\n"
                                    "Os agendamentos dele também serão removidos."):
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("DELETE FROM clientes WHERE id=%s", (self.sid,))
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Cliente excluído!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear(self):
        self.sid = None
        for e in [self.en, self.et, self.ee, self.eb]:
            e.delete(0, "end")

# ============================================================
#  ABA: BARBEIROS
# ============================================================
class BarbeirosTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Barbeiros  ")
        self.sid = None
        self._build()
        self.load()

    def _build(self):
        top = tk.Frame(self, bg=LIGHT, pady=7)
        top.pack(fill="x", padx=10)
        tk.Label(top, text="Buscar:", bg=LIGHT).pack(side="left")
        self.sv_q = tk.StringVar()
        tk.Entry(top, textvariable=self.sv_q, width=28,
                 font=("Helvetica", 10)).pack(side="left", padx=4)
        for txt, color, cmd in [("Buscar", C_UPD, self.search),
                                  ("Todos",  C_CLR, self.load)]:
            tk.Button(top, text=txt, bg=color, fg=WHITE,
                      font=("Helvetica", 9, "bold"), relief="flat",
                      cursor="hand2", command=cmd, padx=8).pack(side="left", padx=2)

        m = tk.Frame(self, bg=LIGHT)
        m.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        fm = tk.LabelFrame(m, text=" Dados do Barbeiro ", bg=WHITE,
                            font=("Helvetica", 10, "bold"), fg=BG,
                            padx=12, pady=8)
        fm.pack(side="left", fill="y", padx=(0, 8))

        _lbl(fm, "Nome *").pack(anchor="w")
        self.en = _ent(fm)
        _lbl(fm, "Especialidade").pack(anchor="w")
        self.ee = _ent(fm)
        _lbl(fm, "Telefone").pack(anchor="w")
        self.et = _ent(fm)
        _lbl(fm, "Status").pack(anchor="w")
        self.sv_at = tk.StringVar(value="Ativo")
        ttk.Combobox(fm, textvariable=self.sv_at, values=["Ativo", "Inativo"],
                     state="readonly", width=25,
                     font=("Helvetica", 11)).pack(fill="x", pady=(1, 6))

        bf = tk.Frame(fm, bg=WHITE)
        bf.pack(fill="x", pady=(5, 0))
        _btn(bf, "➕  Adicionar", C_ADD, self.add)
        _btn(bf, "✏️  Atualizar",  C_UPD, self.update)
        _btn(bf, "🗑️  Excluir",   C_DEL, self.delete)
        _btn(bf, "🔄  Limpar",    C_CLR, self.clear)

        tf = tk.Frame(m, bg=LIGHT)
        tf.pack(side="right", fill="both", expand=True)
        self.tv = _tree(tf,
                        ("id", "nome", "especialidade", "telefone", "status"),
                        ("ID", "Nome", "Especialidade", "Telefone", "Status"),
                        [40, 180, 170, 130, 70])
        self.tv.bind("<<TreeviewSelect>>", self._sel)

    def load(self):
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT id, nome, especialidade, telefone, "
                "CASE WHEN ativo THEN 'Ativo' ELSE 'Inativo' END "
                "FROM barbeiros ORDER BY nome"
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def search(self):
        q = self.sv_q.get().strip()
        if not q:
            self.load()
            return
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT id, nome, especialidade, telefone, "
                "CASE WHEN ativo THEN 'Ativo' ELSE 'Inativo' END "
                "FROM barbeiros WHERE nome ILIKE %s OR especialidade ILIKE %s "
                "ORDER BY nome",
                (f"%{q}%", f"%{q}%")
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _sel(self, _):
        s = self.tv.selection()
        if not s:
            return
        v = self.tv.item(s[0], "values")
        self.sid = v[0]
        self.en.delete(0, "end"); self.en.insert(0, v[1])
        self.ee.delete(0, "end"); self.ee.insert(0, v[2] or "")
        self.et.delete(0, "end"); self.et.insert(0, v[3] or "")
        self.sv_at.set(v[4])

    def add(self):
        nome = self.en.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "INSERT INTO barbeiros(nome,especialidade,telefone,ativo) "
                "VALUES(%s,%s,%s,%s)",
                (nome, self.ee.get() or None,
                 self.et.get() or None, self.sv_at.get() == "Ativo")
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Barbeiro cadastrado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um barbeiro!")
            return
        nome = self.en.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "UPDATE barbeiros SET nome=%s,especialidade=%s,"
                "telefone=%s,ativo=%s WHERE id=%s",
                (nome, self.ee.get() or None, self.et.get() or None,
                 self.sv_at.get() == "Ativo", self.sid)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Barbeiro atualizado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um barbeiro!")
            return
        if not messagebox.askyesno("Confirmar", "Excluir este barbeiro?"):
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("DELETE FROM barbeiros WHERE id=%s", (self.sid,))
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Barbeiro excluído!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear(self):
        self.sid = None
        for e in [self.en, self.ee, self.et]:
            e.delete(0, "end")
        self.sv_at.set("Ativo")

# ============================================================
#  ABA: SERVIÇOS
# ============================================================
class ServicosTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Serviços  ")
        self.sid = None
        self._build()
        self.load()

    def _build(self):
        top = tk.Frame(self, bg=LIGHT, pady=7)
        top.pack(fill="x", padx=10)
        tk.Label(top, text="Buscar:", bg=LIGHT).pack(side="left")
        self.sv_q = tk.StringVar()
        tk.Entry(top, textvariable=self.sv_q, width=28,
                 font=("Helvetica", 10)).pack(side="left", padx=4)
        for txt, color, cmd in [("Buscar", C_UPD, self.search),
                                  ("Todos",  C_CLR, self.load)]:
            tk.Button(top, text=txt, bg=color, fg=WHITE,
                      font=("Helvetica", 9, "bold"), relief="flat",
                      cursor="hand2", command=cmd, padx=8).pack(side="left", padx=2)
        tk.Label(top, text="  Ordenar:", bg=LIGHT).pack(side="left", padx=(12, 2))
        self.sv_ord = tk.StringVar(value="nome")
        ttk.Combobox(top, textvariable=self.sv_ord,
                     values=["nome", "preco", "duracao_min"],
                     width=13, state="readonly").pack(side="left")
        tk.Button(top, text="OK", bg=C_REP, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", padx=6,
                  command=lambda: self.load(self.sv_ord.get())).pack(side="left", padx=4)

        m = tk.Frame(self, bg=LIGHT)
        m.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        fm = tk.LabelFrame(m, text=" Dados do Serviço ", bg=WHITE,
                            font=("Helvetica", 10, "bold"), fg=BG,
                            padx=12, pady=8)
        fm.pack(side="left", fill="y", padx=(0, 8))

        _lbl(fm, "Nome *").pack(anchor="w")
        self.en = _ent(fm)
        _lbl(fm, "Preço (R$) *").pack(anchor="w")
        self.ep = _ent(fm)
        _lbl(fm, "Duração (minutos) *").pack(anchor="w")
        self.ed = _ent(fm)

        bf = tk.Frame(fm, bg=WHITE)
        bf.pack(fill="x", pady=(5, 0))
        _btn(bf, "➕  Adicionar", C_ADD, self.add)
        _btn(bf, "✏️  Atualizar",  C_UPD, self.update)
        _btn(bf, "🗑️  Excluir",   C_DEL, self.delete)
        _btn(bf, "🔄  Limpar",    C_CLR, self.clear)

        tf = tk.Frame(m, bg=LIGHT)
        tf.pack(side="right", fill="both", expand=True)
        self.tv = _tree(tf,
                        ("id", "nome", "preco", "duracao"),
                        ("ID", "Nome do Serviço", "Preço (R$)", "Duração (min)"),
                        [40, 240, 100, 120])
        self.tv.bind("<<TreeviewSelect>>", self._sel)

    def load(self, order="nome"):
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                f"SELECT id,nome,preco,duracao_min FROM servicos ORDER BY {order}"
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def search(self):
        q = self.sv_q.get().strip()
        if not q:
            self.load()
            return
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT id,nome,preco,duracao_min FROM servicos "
                "WHERE nome ILIKE %s ORDER BY nome",
                (f"%{q}%",)
            )
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _sel(self, _):
        s = self.tv.selection()
        if not s:
            return
        v = self.tv.item(s[0], "values")
        self.sid = v[0]
        self.en.delete(0, "end"); self.en.insert(0, v[1])
        self.ep.delete(0, "end"); self.ep.insert(0, v[2])
        self.ed.delete(0, "end"); self.ed.insert(0, v[3])

    def add(self):
        nome = self.en.get().strip()
        preco = self.ep.get().strip()
        dur = self.ed.get().strip()
        if not nome or not preco or not dur:
            messagebox.showwarning("Aviso", "Nome, Preço e Duração são obrigatórios!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "INSERT INTO servicos(nome,preco,duracao_min) VALUES(%s,%s,%s)",
                (nome, float(preco), int(dur))
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Serviço cadastrado!")
            self.clear()
            self.load()
        except ValueError:
            messagebox.showerror("Erro", "Preço e duração devem ser valores numéricos!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um serviço!")
            return
        nome = self.en.get().strip()
        preco = self.ep.get().strip()
        dur = self.ed.get().strip()
        if not nome or not preco or not dur:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "UPDATE servicos SET nome=%s,preco=%s,duracao_min=%s WHERE id=%s",
                (nome, float(preco), int(dur), self.sid)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Serviço atualizado!")
            self.clear()
            self.load()
        except ValueError:
            messagebox.showerror("Erro", "Preço e duração devem ser valores numéricos!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um serviço!")
            return
        if not messagebox.askyesno("Confirmar", "Excluir este serviço?"):
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("DELETE FROM servicos WHERE id=%s", (self.sid,))
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Serviço excluído!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear(self):
        self.sid = None
        for e in [self.en, self.ep, self.ed]:
            e.delete(0, "end")

# ============================================================
#  ABA: AGENDAMENTOS
# ============================================================
class AgendamentosTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Agendamentos  ")
        self.sid = None
        self._clientes  = {}
        self._barbeiros = {}
        self._servicos  = {}
        self._build()
        self._refresh_combos()
        self.load()

    def _build(self):
        top = tk.Frame(self, bg=LIGHT, pady=7)
        top.pack(fill="x", padx=10)
        tk.Label(top, text="Filtrar status:", bg=LIGHT).pack(side="left")
        self.sv_filt = tk.StringVar(value="Todos")
        ttk.Combobox(top, textvariable=self.sv_filt,
                     values=["Todos", "agendado", "concluido", "cancelado"],
                     width=11, state="readonly").pack(side="left", padx=4)
        tk.Button(top, text="Filtrar", bg=C_UPD, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", command=self.filter_status,
                  padx=8).pack(side="left")
        tk.Button(top, text="Todos", bg=C_CLR, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", command=self.load,
                  padx=8).pack(side="left", padx=4)
        tk.Label(top, text="  Ordenar:", bg=LIGHT).pack(side="left", padx=(12, 2))
        self.sv_ord = tk.StringVar(value="a.data_hora DESC")
        ttk.Combobox(top, textvariable=self.sv_ord,
                     values=["a.data_hora DESC", "a.data_hora ASC",
                              "a.status", "cl.nome"],
                     width=18, state="readonly").pack(side="left")
        tk.Button(top, text="OK", bg=C_REP, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", padx=6,
                  command=lambda: self.load(self.sv_ord.get())).pack(side="left", padx=4)

        m = tk.Frame(self, bg=LIGHT)
        m.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        fm = tk.LabelFrame(m, text=" Dados do Agendamento ", bg=WHITE,
                            font=("Helvetica", 10, "bold"), fg=BG,
                            padx=12, pady=8)
        fm.pack(side="left", fill="y", padx=(0, 8))

        _lbl(fm, "Cliente *").pack(anchor="w")
        self.sv_cli = tk.StringVar()
        self.cb_cli = ttk.Combobox(fm, textvariable=self.sv_cli, width=26,
                                    font=("Helvetica", 10), state="readonly")
        self.cb_cli.pack(fill="x", pady=(1, 6))

        _lbl(fm, "Barbeiro *").pack(anchor="w")
        self.sv_bar = tk.StringVar()
        self.cb_bar = ttk.Combobox(fm, textvariable=self.sv_bar, width=26,
                                    font=("Helvetica", 10), state="readonly")
        self.cb_bar.pack(fill="x", pady=(1, 6))

        _lbl(fm, "Serviço *").pack(anchor="w")
        self.sv_srv = tk.StringVar()
        self.cb_srv = ttk.Combobox(fm, textvariable=self.sv_srv, width=26,
                                    font=("Helvetica", 10), state="readonly")
        self.cb_srv.pack(fill="x", pady=(1, 6))

        _lbl(fm, "Data/Hora *  (AAAA-MM-DD HH:MM)").pack(anchor="w")
        self.edh = _ent(fm)

        _lbl(fm, "Status").pack(anchor="w")
        self.sv_st = tk.StringVar(value="agendado")
        ttk.Combobox(fm, textvariable=self.sv_st,
                     values=["agendado", "concluido", "cancelado"],
                     width=25, state="readonly",
                     font=("Helvetica", 10)).pack(fill="x", pady=(1, 6))

        _lbl(fm, "Observação").pack(anchor="w")
        self.eo = tk.Text(fm, height=3, width=28, font=("Helvetica", 10),
                          relief="solid", bd=1)
        self.eo.pack(fill="x", pady=(1, 6))

        tk.Button(fm, text="🔄 Recarregar Listas", bg=C_REP, fg=WHITE,
                  font=("Helvetica", 9, "bold"), relief="flat",
                  cursor="hand2", command=self._refresh_combos,
                  pady=3).pack(fill="x", pady=(4, 4))

        bf = tk.Frame(fm, bg=WHITE)
        bf.pack(fill="x")
        _btn(bf, "➕  Adicionar", C_ADD, self.add)
        _btn(bf, "✏️  Atualizar",  C_UPD, self.update)
        _btn(bf, "🗑️  Excluir",   C_DEL, self.delete)
        _btn(bf, "🔄  Limpar",    C_CLR, self.clear)

        tf = tk.Frame(m, bg=LIGHT)
        tf.pack(side="right", fill="both", expand=True)
        self.tv = _tree(tf,
                        ("id", "cliente", "barbeiro", "servico",
                         "preco", "data_hora", "status"),
                        ("ID", "Cliente", "Barbeiro", "Serviço",
                         "Preço", "Data/Hora", "Status"),
                        [40, 160, 130, 150, 70, 130, 80])
        self.tv.bind("<<TreeviewSelect>>", self._sel)

    def _refresh_combos(self):
        try:
            c = get_conn()
            cur = c.cursor()

            cur.execute("SELECT id, nome FROM clientes ORDER BY nome")
            self._clientes = {f"{r[1]} (#{r[0]})": r[0] for r in cur.fetchall()}
            self.cb_cli["values"] = list(self._clientes)

            cur.execute(
                "SELECT id, nome FROM barbeiros WHERE ativo=TRUE ORDER BY nome"
            )
            self._barbeiros = {f"{r[1]} (#{r[0]})": r[0] for r in cur.fetchall()}
            self.cb_bar["values"] = list(self._barbeiros)

            cur.execute("SELECT id, nome, preco FROM servicos ORDER BY nome")
            self._servicos = {
                f"{r[1]} — R${float(r[2]):.2f} (#{r[0]})": r[0]
                for r in cur.fetchall()
            }
            self.cb_srv["values"] = list(self._servicos)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load(self, order="a.data_hora DESC"):
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(f"""
                SELECT a.id, cl.nome, b.nome, s.nome, s.preco,
                       a.data_hora, a.status
                FROM agendamentos a
                INNER JOIN clientes  cl ON a.cliente_id  = cl.id
                INNER JOIN barbeiros b  ON a.barbeiro_id = b.id
                INNER JOIN servicos  s  ON a.servico_id  = s.id
                ORDER BY {order}
            """)
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filter_status(self):
        f = self.sv_filt.get()
        if f == "Todos":
            self.load()
            return
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("""
                SELECT a.id, cl.nome, b.nome, s.nome, s.preco,
                       a.data_hora, a.status
                FROM agendamentos a
                INNER JOIN clientes  cl ON a.cliente_id  = cl.id
                INNER JOIN barbeiros b  ON a.barbeiro_id = b.id
                INNER JOIN servicos  s  ON a.servico_id  = s.id
                WHERE a.status = %s
                ORDER BY a.data_hora DESC
            """, (f,))
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _sel(self, _):
        s = self.tv.selection()
        if not s:
            return
        v = self.tv.item(s[0], "values")
        self.sid = v[0]
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "SELECT cliente_id,barbeiro_id,servico_id,"
                "data_hora,status,observacao FROM agendamentos WHERE id=%s",
                (self.sid,)
            )
            row = cur.fetchone()
            c.close()
            if not row:
                return
            cli_id, bar_id, srv_id, dh, st, obs = row
            cli_key = next((k for k, vid in self._clientes.items()
                            if vid == cli_id), "")
            bar_key = next((k for k, vid in self._barbeiros.items()
                            if vid == bar_id), "")
            srv_key = next((k for k, vid in self._servicos.items()
                            if vid == srv_id), "")
            self.sv_cli.set(cli_key)
            self.sv_bar.set(bar_key)
            self.sv_srv.set(srv_key)
            self.edh.delete(0, "end")
            self.edh.insert(0, str(dh)[:16] if dh else "")
            self.sv_st.set(st or "agendado")
            self.eo.delete("1.0", "end")
            if obs:
                self.eo.insert("1.0", obs)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _get_ids(self):
        return (
            self._clientes.get(self.sv_cli.get()),
            self._barbeiros.get(self.sv_bar.get()),
            self._servicos.get(self.sv_srv.get()),
        )

    def add(self):
        cli, bar, srv = self._get_ids()
        dh = self.edh.get().strip()
        if not all([cli, bar, srv, dh]):
            messagebox.showwarning(
                "Aviso",
                "Cliente, Barbeiro, Serviço e Data/Hora são obrigatórios!\n"
                "Se as listas estiverem vazias, clique em 'Recarregar Listas'."
            )
            return
        obs = self.eo.get("1.0", "end").strip() or None
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "INSERT INTO agendamentos"
                "(cliente_id,barbeiro_id,servico_id,data_hora,status,observacao) "
                "VALUES(%s,%s,%s,%s,%s,%s)",
                (cli, bar, srv, dh, self.sv_st.get(), obs)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Agendamento criado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um agendamento!")
            return
        cli, bar, srv = self._get_ids()
        dh = self.edh.get().strip()
        if not all([cli, bar, srv, dh]):
            messagebox.showwarning("Aviso", "Todos os campos obrigatórios devem ser preenchidos!")
            return
        obs = self.eo.get("1.0", "end").strip() or None
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "UPDATE agendamentos SET cliente_id=%s,barbeiro_id=%s,"
                "servico_id=%s,data_hora=%s,status=%s,observacao=%s WHERE id=%s",
                (cli, bar, srv, dh, self.sv_st.get(), obs, self.sid)
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Agendamento atualizado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um agendamento!")
            return
        if not messagebox.askyesno("Confirmar", "Excluir este agendamento?"):
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("DELETE FROM agendamentos WHERE id=%s", (self.sid,))
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Agendamento excluído!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear(self):
        self.sid = None
        self.sv_cli.set("")
        self.sv_bar.set("")
        self.sv_srv.set("")
        self.edh.delete(0, "end")
        self.sv_st.set("agendado")
        self.eo.delete("1.0", "end")

# ============================================================
#  ABA: RELATÓRIOS
# ============================================================
class RelatoriosTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Relatórios  ")
        self._build()

    def _build(self):
        # Painel esquerdo — botões
        left = tk.Frame(self, bg=PANEL, width=230)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="RELATÓRIOS",
                 font=("Helvetica", 12, "bold"),
                 bg=PANEL, fg=ACCENT).pack(pady=(18, 8))
        tk.Frame(left, bg=ACCENT, height=2).pack(fill="x", padx=12)

        relatorios = [
            ("📋  Todos os Agendamentos\n    (INNER JOIN)",
             self.r_agendamentos),
            ("👥  Clientes × Agendamentos\n    (LEFT JOIN)",
             self.r_clientes_left),
            ("💈  Receita por Barbeiro\n    (LEFT JOIN)",
             self.r_receita_barbeiro),
            ("📅  Agenda do Dia\n    (INNER JOIN + Filtro)",
             self.r_agenda_dia),
            ("🏆  Serviços Mais Populares\n    (INNER JOIN + GROUP BY)",
             self.r_servicos_pop),
        ]

        for label, cmd in relatorios:
            tk.Button(left, text=label, bg=BG, fg=WHITE,
                      font=("Helvetica", 9), relief="flat",
                      cursor="hand2", command=cmd,
                      justify="left", anchor="w",
                      padx=12, pady=8).pack(fill="x", pady=2, padx=8)

        tk.Label(left, text="Data para Agenda do Dia:",
                 bg=PANEL, fg="#aaaaaa",
                 font=("Helvetica", 8)).pack(pady=(16, 2))
        self.e_data = tk.Entry(left, font=("Helvetica", 10),
                               width=14, justify="center")
        self.e_data.insert(0, "2026-04-25")
        self.e_data.pack()

        # Painel direito — resultado
        right = tk.Frame(self, bg=LIGHT)
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_title = tk.Label(
            right, text="← Selecione um relatório",
            font=("Helvetica", 13, "bold"),
            bg=LIGHT, fg=BG
        )
        self.lbl_title.pack(pady=(0, 6))

        self.lbl_sql = tk.Label(
            right, text="", font=("Courier", 8),
            bg="#e8f4fd", fg="#1a1a2e",
            justify="left", anchor="w",
            wraplength=800, padx=8, pady=6, relief="groove"
        )
        self.lbl_sql.pack(fill="x", pady=(0, 8))

        self.tree_frame = tk.Frame(right, bg=LIGHT)
        self.tree_frame.pack(fill="both", expand=True)

    def _show(self, title, sql_txt, cols, heads, widths, rows):
        self.lbl_title.config(text=title)
        self.lbl_sql.config(text=f"SQL utilizado:\n{sql_txt}")
        for w in self.tree_frame.winfo_children():
            w.destroy()
        tv = _tree(self.tree_frame, cols, heads, widths)
        for row in rows:
            tv.insert("", "end", values=row)

    # --- Relatório 1: INNER JOIN completo ---
    def r_agendamentos(self):
        sql = (
            "SELECT a.id, c.nome, b.nome, s.nome, s.preco, a.data_hora, a.status\n"
            "FROM agendamentos a\n"
            "INNER JOIN clientes  c ON a.cliente_id  = c.id\n"
            "INNER JOIN barbeiros b ON a.barbeiro_id = b.id\n"
            "INNER JOIN servicos  s ON a.servico_id  = s.id\n"
            "ORDER BY a.data_hora DESC"
        )
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            c.close()
            self._show(
                "Todos os Agendamentos — INNER JOIN",
                sql,
                ("id", "cliente", "barbeiro", "servico", "preco", "data_hora", "status"),
                ("ID", "Cliente", "Barbeiro", "Serviço", "Preço", "Data/Hora", "Status"),
                [40, 160, 130, 150, 70, 130, 80],
                rows
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- Relatório 2: LEFT JOIN clientes ---
    def r_clientes_left(self):
        sql = (
            "SELECT c.id, c.nome, c.telefone,\n"
            "       COUNT(a.id)       AS total_agendamentos,\n"
            "       MAX(a.data_hora)  AS ultimo_agendamento\n"
            "FROM clientes c\n"
            "LEFT JOIN agendamentos a ON c.id = a.cliente_id\n"
            "GROUP BY c.id, c.nome, c.telefone\n"
            "ORDER BY total_agendamentos DESC"
        )
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            c.close()
            self._show(
                "Clientes e Total de Agendamentos — LEFT JOIN",
                sql,
                ("id", "nome", "telefone", "total", "ultimo"),
                ("ID", "Nome", "Telefone", "Total Agend.", "Último Agend."),
                [40, 210, 130, 100, 160],
                rows
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- Relatório 3: LEFT JOIN barbeiros + receita ---
    def r_receita_barbeiro(self):
        sql = (
            "SELECT b.nome, b.especialidade,\n"
            "       COUNT(a.id)               AS atendimentos,\n"
            "       COALESCE(SUM(s.preco), 0) AS receita_total\n"
            "FROM barbeiros b\n"
            "LEFT JOIN agendamentos a\n"
            "       ON b.id = a.barbeiro_id AND a.status = 'concluido'\n"
            "LEFT JOIN servicos s ON a.servico_id = s.id\n"
            "GROUP BY b.id, b.nome, b.especialidade\n"
            "ORDER BY receita_total DESC"
        )
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            c.close()
            self._show(
                "Receita por Barbeiro — LEFT JOIN",
                sql,
                ("nome", "especialidade", "atendimentos", "receita"),
                ("Barbeiro", "Especialidade", "Atendimentos", "Receita (R$)"),
                [190, 170, 110, 120],
                rows
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- Relatório 4: INNER JOIN + filtro de data ---
    def r_agenda_dia(self):
        data = self.e_data.get().strip()
        sql = (
            f"SELECT cl.nome, b.nome, s.nome, s.preco,\n"
            f"       a.data_hora, a.status, a.observacao\n"
            f"FROM agendamentos a\n"
            f"INNER JOIN clientes  cl ON a.cliente_id  = cl.id\n"
            f"INNER JOIN barbeiros b  ON a.barbeiro_id = b.id\n"
            f"INNER JOIN servicos  s  ON a.servico_id  = s.id\n"
            f"WHERE DATE(a.data_hora) = '{data}'\n"
            f"ORDER BY a.data_hora"
        )
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("""
                SELECT cl.nome, b.nome, s.nome, s.preco,
                       a.data_hora, a.status, a.observacao
                FROM agendamentos a
                INNER JOIN clientes  cl ON a.cliente_id  = cl.id
                INNER JOIN barbeiros b  ON a.barbeiro_id = b.id
                INNER JOIN servicos  s  ON a.servico_id  = s.id
                WHERE DATE(a.data_hora) = %s
                ORDER BY a.data_hora
            """, (data,))
            rows = cur.fetchall()
            c.close()
            self._show(
                f"Agenda do Dia: {data} — INNER JOIN + Filtro",
                sql,
                ("cliente", "barbeiro", "servico", "preco",
                 "hora", "status", "obs"),
                ("Cliente", "Barbeiro", "Serviço", "Preço",
                 "Data/Hora", "Status", "Observação"),
                [150, 130, 140, 70, 130, 80, 200],
                rows
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- Relatório 5: INNER JOIN + GROUP BY serviços populares ---
    def r_servicos_pop(self):
        sql = (
            "SELECT s.nome, s.preco,\n"
            "       COUNT(a.id)   AS total_realizados,\n"
            "       SUM(s.preco)  AS receita_total\n"
            "FROM servicos s\n"
            "INNER JOIN agendamentos a ON s.id = a.servico_id\n"
            "WHERE a.status = 'concluido'\n"
            "GROUP BY s.id, s.nome, s.preco\n"
            "ORDER BY total_realizados DESC"
        )
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            c.close()
            self._show(
                "Serviços Mais Populares — INNER JOIN + GROUP BY",
                sql,
                ("servico", "preco", "total", "receita"),
                ("Serviço", "Preço (R$)", "Total Realizados", "Receita Total (R$)"),
                [230, 90, 130, 140],
                rows
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# ============================================================
#  ABA: USUÁRIOS
# ============================================================
class UsuariosTab(tk.Frame):
    def __init__(self, nb):
        super().__init__(nb, bg=LIGHT)
        nb.add(self, text="  Usuários  ")
        self.sid = None
        self._build()
        self.load()

    def _build(self):
        m = tk.Frame(self, bg=LIGHT)
        m.pack(fill="both", expand=True, padx=10, pady=10)

        fm = tk.LabelFrame(m, text=" Dados do Usuário ", bg=WHITE,
                           font=("Helvetica", 10, "bold"), fg=BG,
                           padx=12, pady=8)
        fm.pack(side="left", fill="y", padx=(0, 8))

        _lbl(fm, "Nome de usuário *").pack(anchor="w")
        self.eu = _ent(fm)

        _lbl(fm, "Senha *  (vazio = manter atual)").pack(anchor="w")
        self.es = tk.Entry(fm, font=("Helvetica", 11), width=27,
                           relief="solid", bd=1, show="•")
        self.es.pack(fill="x", pady=(1, 6))

        _lbl(fm, "Nível").pack(anchor="w")
        self.sv_nv = tk.StringVar(value="operador")
        ttk.Combobox(fm, textvariable=self.sv_nv,
                     values=["admin", "operador"],
                     state="readonly", width=25,
                     font=("Helvetica", 11)).pack(fill="x", pady=(1, 6))

        bf = tk.Frame(fm, bg=WHITE)
        bf.pack(fill="x", pady=(5, 0))
        _btn(bf, "➕  Adicionar", C_ADD, self.add)
        _btn(bf, "✏️  Atualizar",  C_UPD, self.update)
        _btn(bf, "🗑️  Excluir",   C_DEL, self.delete)
        _btn(bf, "🔄  Limpar",    C_CLR, self.clear)

        tf = tk.Frame(m, bg=LIGHT)
        tf.pack(side="right", fill="both", expand=True)
        self.tv = _tree(tf,
                        ("id", "username", "nivel", "criado_em"),
                        ("ID", "Usuário", "Nível", "Criado em"),
                        [40, 200, 100, 180])
        self.tv.bind("<<TreeviewSelect>>", self._sel)

    def load(self):
        self.tv.delete(*self.tv.get_children())
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("SELECT id, username, nivel, criado_em FROM usuarios ORDER BY username")
            for r in cur.fetchall():
                self.tv.insert("", "end", values=r)
            c.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _sel(self, _):
        s = self.tv.selection()
        if not s:
            return
        v = self.tv.item(s[0], "values")
        self.sid = v[0]
        self.eu.delete(0, "end"); self.eu.insert(0, v[1])
        self.es.delete(0, "end")
        self.sv_nv.set(v[2])

    def add(self):
        u = self.eu.get().strip()
        p = self.es.get().strip()
        if not u or not p:
            messagebox.showwarning("Aviso", "Usuário e senha são obrigatórios!")
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute(
                "INSERT INTO usuarios(username, senha, nivel) VALUES(%s, %s, %s)",
                (u, sha256(p), self.sv_nv.get())
            )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        u = self.eu.get().strip()
        if not u:
            messagebox.showwarning("Aviso", "Nome de usuário é obrigatório!")
            return
        p = self.es.get().strip()
        try:
            c = get_conn()
            cur = c.cursor()
            if p:
                cur.execute(
                    "UPDATE usuarios SET username=%s, senha=%s, nivel=%s WHERE id=%s",
                    (u, sha256(p), self.sv_nv.get(), self.sid)
                )
            else:
                cur.execute(
                    "UPDATE usuarios SET username=%s, nivel=%s WHERE id=%s",
                    (u, self.sv_nv.get(), self.sid)
                )
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Usuário atualizado!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete(self):
        if not self.sid:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        if not messagebox.askyesno("Confirmar", "Excluir este usuário?"):
            return
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("DELETE FROM usuarios WHERE id=%s", (self.sid,))
            c.commit()
            c.close()
            messagebox.showinfo("Sucesso", "Usuário excluído!")
            self.clear()
            self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear(self):
        self.sid = None
        self.eu.delete(0, "end")
        self.es.delete(0, "end")
        self.sv_nv.set("operador")

# ============================================================
#  PONTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    Login()

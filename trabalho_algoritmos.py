import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3

# CONFIGURAÇÕES
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# BANCO DE DADOS
conexao = sqlite3.connect("historico_alunos.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,
    ra TEXT,
    curso TEXT,
    semestre TEXT,
    frequencia REAL,

    p1 REAL,
    p2 REAL,
    t1 REAL,
    t2 REAL,

    media REAL,
    status TEXT
)
""")

conexao.commit()

# =========================================================
# CORES
# =========================================================
COR_FUNDO = "#EEF2F7"
COR_CARD = "#FFFFFF"

COR_AZUL = "#2563EB"
COR_AZUL_HOVER = "#1D4ED8"

COR_VERDE = "#16A34A"
COR_VERMELHO = "#DC2626"
COR_LARANJA = "#F59E0B"

COR_TEXTO = "#111827"
COR_CINZA = "#6B7280"
COR_BORDA = "#D1D5DB"

# =========================================================
# JANELA
# =========================================================
janela = ctk.CTk()

janela.title("Sistema de Fechamento de Média")

janela.geometry("1280x780")
janela.resizable(False, False)

janela.configure(
    fg_color=COR_FUNDO
)

# =========================================================
# FUNÇÃO ENTRY
# =========================================================
def criar_entry(frame, placeholder, largura=260):

    entry = ctk.CTkEntry(

        frame,

        width=largura,
        height=44,

        corner_radius=12,

        border_width=2,
        border_color=COR_BORDA,

        fg_color="white",

        text_color=COR_TEXTO,

        placeholder_text=placeholder,

        font=("Arial", 14)
    )

    return entry

# =========================================================
# HISTÓRICO
# =========================================================
def abrir_historico():

    janela_historico = ctk.CTkToplevel()

    janela_historico.title("Histórico de Alunos")

    janela_historico.geometry("1120x520")

    tabela = ttk.Treeview(

        janela_historico,

        columns=(

            "Nome",
            "RA",
            "Curso",
            "Semestre",
            "Media",
            "Status"
        ),

        show="headings"
    )

    tabela.heading("Nome", text="Nome")
    tabela.heading("RA", text="RA")
    tabela.heading("Curso", text="Curso")
    tabela.heading("Semestre", text="Semestre")
    tabela.heading("Media", text="Média")
    tabela.heading("Status", text="Status")

    tabela.column("Nome", width=240)
    tabela.column("RA", width=140)
    tabela.column("Curso", width=220)
    tabela.column("Semestre", width=130)
    tabela.column("Media", width=120)
    tabela.column("Status", width=180)

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    cursor.execute(
        "SELECT nome, ra, curso, semestre, media, status FROM historico"
    )

    dados = cursor.fetchall()

    for linha in dados:

        tabela.insert(
            "",
            "end",
            values=linha
        )

# =========================================================
# CALCULAR
# =========================================================
def calcular_media():

    try:

        nome = entry_nome.get()
        ra = entry_ra.get()
        curso = entry_curso.get()

        semestre_escolhido = semestre.get()

        frequencia = float(entry_frequencia.get())

        p1 = float(entry_p1.get())
        peso_p1 = float(entry_peso_p1.get())

        p2 = float(entry_p2.get())
        peso_p2 = float(entry_peso_p2.get())

        t1 = float(entry_t1.get())
        peso_t1 = float(entry_peso_t1.get())

        t2 = float(entry_t2.get())
        peso_t2 = float(entry_peso_t2.get())

        soma_pesos = (
            peso_p1 +
            peso_p2 +
            peso_t1 +
            peso_t2
        )

        media = (

            (p1 * peso_p1) +

            (p2 * peso_p2) +

            (t1 * peso_t1) +

            (t2 * peso_t2)

        ) / soma_pesos

        media = round(media, 2)

        # STATUS
        if frequencia < 75:

            status = "REPROVADO POR FALTA"

            resultado.configure(
                text=status,
                fg_color="#FEE2E2",
                text_color=COR_VERMELHO
            )

        elif media >= 7:

            status = "APROVADO"

            resultado.configure(
                text=status,
                fg_color="#DCFCE7",
                text_color=COR_VERDE
            )

        else:

            status = "EXAME"

            resultado.configure(
                text=status,
                fg_color="#FEF3C7",
                text_color=COR_LARANJA
            )

        # LABELS
        label_media.configure(
            text=f"Média Final: {media}"
        )

        label_nome.configure(
            text=f"Aluno: {nome}"
        )

        label_curso.configure(
            text=f"Curso: {curso}"
        )

        # SALVAR NO BANCO
        cursor.execute("""

        INSERT INTO historico (

            nome,
            ra,
            curso,
            semestre,
            frequencia,

            p1,
            p2,
            t1,
            t2,

            media,
            status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            nome,
            ra,
            curso,
            semestre_escolhido,
            frequencia,

            p1,
            p2,
            t1,
            t2,

            media,
            status
        ))

        conexao.commit()

    except:

        messagebox.showerror(
            "Erro",
            "Preencha os campos corretamente!"
        )

# =========================================================
# LIMPAR
# =========================================================
def limpar_campos():

    campos = [

        entry_nome,
        entry_ra,
        entry_curso,
        entry_frequencia,

        entry_p1,
        entry_peso_p1,

        entry_p2,
        entry_peso_p2,

        entry_t1,
        entry_peso_t1,

        entry_t2,
        entry_peso_t2
    ]

    for campo in campos:

        campo.delete(0, "end")

    resultado.configure(
        text="Resultado",
        fg_color="#E5E7EB",
        text_color=COR_TEXTO
    )

    label_media.configure(
        text="Média Final: --"
    )

    label_nome.configure(
        text="Aluno: --"
    )

    label_curso.configure(
        text="Curso: --"
    )

# =========================================================
# FUNÇÃO LABEL
# =========================================================
def criar_label(frame, texto):

    ctk.CTkLabel(

        frame,

        text=texto,

        font=("Arial", 15, "bold"),

        text_color=COR_CINZA

    ).pack(
        anchor="w",
        pady=(0, 6)
    )

# =========================================================
# TÍTULO
# =========================================================
titulo = ctk.CTkLabel(

    janela,

    text="SISTEMA DE FECHAMENTO DE MÉDIA",

    font=("Times New Roman", 34, "bold"),

    text_color=COR_TEXTO
)

titulo.pack(
    pady=(20, 10)
)

# =========================================================
# FRAME PRINCIPAL
# =========================================================
frame_principal = ctk.CTkFrame(

    janela,

    width=1200,
    height=620,

    corner_radius=28,

    fg_color=COR_CARD,

    border_width=2,
    border_color="#E5E7EB"
)

frame_principal.pack(
    padx=20,
    pady=10
)

frame_principal.pack_propagate(False)

# =========================================================
# CONTAINER INTERNO
# =========================================================
container = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

container.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=35
)

# =========================================================
# ESQUERDA
# =========================================================
frame_esquerda = ctk.CTkFrame(

    container,

    width=470,

    corner_radius=20,

    fg_color="#F8FAFC",

    border_width=1,
    border_color="#E5E7EB"
)

frame_esquerda.pack(
    side="left",
    fill="y",
    padx=(0, 20)
)

frame_esquerda.pack_propagate(False)

# =========================================================
# DIREITA
# =========================================================
frame_direita = ctk.CTkFrame(

    container,

    width=570,

    corner_radius=20,

    fg_color="#F8FAFC",

    border_width=1,
    border_color="#E5E7EB"
)

frame_direita.pack(
    side="right",
    fill="both",
    expand=True
)

frame_direita.pack_propagate(False)

# =========================================================
# CONTEÚDO ESQUERDA
# =========================================================
conteudo_esquerda = ctk.CTkFrame(
    frame_esquerda,
    fg_color="transparent"
)

conteudo_esquerda.pack(
    padx=28,
    pady=28,
    fill="both",
    expand=True
)

ctk.CTkLabel(

    conteudo_esquerda,

    text="Informações do Aluno",

    font=("Arial", 28, "bold"),

    text_color=COR_TEXTO

).pack(
    anchor="center",
    pady=(0, 28)
)

# NOME
criar_label(conteudo_esquerda, "Nome do aluno")

entry_nome = criar_entry(
    conteudo_esquerda,
    "Digite o nome",
    390
)

entry_nome.pack(pady=(0, 18))

# RA
criar_label(conteudo_esquerda, "RA - Matrícula")

entry_ra = criar_entry(
    conteudo_esquerda,
    "Digite o RA",
    390
)

entry_ra.pack(pady=(0, 18))

# CURSO
criar_label(conteudo_esquerda, "Curso")

entry_curso = criar_entry(
    conteudo_esquerda,
    "Digite o curso",
    390
)

entry_curso.pack(pady=(0, 18))

# SEMESTRE
criar_label(conteudo_esquerda, "Semestre")

semestre = ctk.StringVar(
    value="1º Semestre"
)

frame_radio = ctk.CTkFrame(
    conteudo_esquerda,
    fg_color="transparent"
)

frame_radio.pack(
    pady=(2, 20),
    anchor="w"
)

radio1 = ctk.CTkRadioButton(
    frame_radio,
    text="1º Semestre",
    variable=semestre,
    value="1º Semestre"
)

radio1.pack(
    side="left",
    padx=(0, 25)
)

radio2 = ctk.CTkRadioButton(
    frame_radio,
    text="2º Semestre",
    variable=semestre,
    value="2º Semestre"
)

radio2.pack(side="left")

# FREQUÊNCIA
criar_label(conteudo_esquerda, "Frequência (%)")

entry_frequencia = criar_entry(
    conteudo_esquerda,
    "Ex: 75",
    390
)

entry_frequencia.pack()

# =========================================================
# CONTEÚDO DIREITA
# =========================================================
conteudo_direita = ctk.CTkFrame(
    frame_direita,
    fg_color="transparent"
)

conteudo_direita.pack(
    padx=28,
    pady=28,
    fill="both",
    expand=True
)

ctk.CTkLabel(

    conteudo_direita,

    text="Lançamento de Notas",

    font=("Arial", 28, "bold"),

    text_color=COR_TEXTO

).pack(
    anchor="center",
    pady=(0, 28)
)

# =========================================================
# TABELA DE NOTAS
# =========================================================
frame_tabela = ctk.CTkFrame(

    conteudo_direita,

    height=280,

    corner_radius=18,

    fg_color="white",

    border_width=1,
    border_color="#E5E7EB"
)

frame_tabela.pack(
    fill="x"
)

frame_tabela.pack_propagate(False)

# CABEÇALHO
ctk.CTkLabel(
    frame_tabela,
    text="Avaliação",
    font=("Arial", 16, "bold")
).place(x=45, y=22)

ctk.CTkLabel(
    frame_tabela,
    text="Nota",
    font=("Arial", 16, "bold")
).place(x=225, y=22)

ctk.CTkLabel(
    frame_tabela,
    text="Peso",
    font=("Arial", 16, "bold")
).place(x=390, y=22)

# =========================================================
# LINHAS
# =========================================================
def criar_linha(y, texto):

    ctk.CTkLabel(
        frame_tabela,
        text=texto,
        font=("Arial", 16)
    ).place(x=50, y=y)

    nota = criar_entry(
        frame_tabela,
        "",
        120
    )

    nota.place(x=190, y=y-7)

    peso = criar_entry(
        frame_tabela,
        "",
        100
    )

    peso.place(x=355, y=y-7)

    return nota, peso

entry_p1, entry_peso_p1 = criar_linha(75, "P1")
entry_p2, entry_peso_p2 = criar_linha(125, "P2")
entry_t1, entry_peso_t1 = criar_linha(175, "T1")
entry_t2, entry_peso_t2 = criar_linha(225, "T2")

# =========================================================
# RESULTADO
# =========================================================
frame_resultado = ctk.CTkFrame(

    conteudo_direita,

    corner_radius=20,

    fg_color="white",

    border_width=1,
    border_color="#E5E7EB"
)

frame_resultado.pack(
    fill="x",
    pady=(25, 0)
)

resultado = ctk.CTkLabel(

    frame_resultado,

    text="Resultado",

    height=72,

    corner_radius=18,

    fg_color="#E5E7EB",

    text_color=COR_TEXTO,

    font=("Arial", 28, "bold")
)

resultado.pack(
    fill="x",
    padx=18,
    pady=(18, 12)
)

label_media = ctk.CTkLabel(

    frame_resultado,

    text="Média Final: --",

    font=("Arial", 19, "bold"),

    text_color=COR_TEXTO
)

label_media.pack(
    pady=(0, 5)
)

label_nome = ctk.CTkLabel(

    frame_resultado,

    text="Aluno: --",

    font=("Arial", 15),

    text_color=COR_CINZA
)

label_nome.pack(
    pady=2
)

label_curso = ctk.CTkLabel(

    frame_resultado,

    text="Curso: --",

    font=("Arial", 15),

    text_color=COR_CINZA
)

label_curso.pack(
    pady=(2, 18)
)

# =========================================================
# BOTÕES
# =========================================================
frame_botoes = ctk.CTkFrame(
    janela,
    fg_color="transparent"
)

frame_botoes.pack(
    pady=(5, 20)
)

# LIMPAR
botao_limpar = ctk.CTkButton(

    frame_botoes,

    text="Limpar Dados",

    width=220,
    height=52,

    corner_radius=15,

    fg_color="#6B7280",

    hover_color="#4B5563",

    font=("Arial", 15, "bold"),

    command=limpar_campos
)

botao_limpar.pack(
    side="left",
    padx=12
)

# CALCULAR
botao_calcular = ctk.CTkButton(

    frame_botoes,

    text="Calcular Média",

    width=220,
    height=52,

    corner_radius=15,

    fg_color=COR_AZUL,

    hover_color=COR_AZUL_HOVER,

    font=("Arial", 15, "bold"),

    command=calcular_media
)

botao_calcular.pack(
    side="left",
    padx=12
)

# HISTÓRICO
botao_historico = ctk.CTkButton(

    frame_botoes,

    text="Histórico",

    width=220,
    height=52,

    corner_radius=15,

    fg_color="#059669",

    hover_color="#047857",

    font=("Arial", 15, "bold"),

    command=abrir_historico
)

botao_historico.pack(
    side="left",
    padx=12
)

# =========================================================
# EXECUTAR
# =========================================================
janela.mainloop()
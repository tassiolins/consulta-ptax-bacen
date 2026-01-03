import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

from ptax_api import buscar_ptax_hoje, buscar_ptax_periodo
from database import criar_tabela, salvar_cotacoes
from exportacao import exportar_excel


class PtaxApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PTAX - Banco Central | Dashboard Gerencial")
        self.root.geometry("1200x820")
        self.root.configure(bg="#1e1e1e")

        criar_tabela()
        self.dados_atuais = []

        self._configurar_estilo()
        self._criar_widgets()

    # 🔹 método explícito (importante para PyInstaller)
    def mainloop(self):
        self.root.mainloop()

    # ================= ESTILO =================
    def _configurar_estilo(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=25
        )
        style.map("Treeview", background=[("selected", "#3a3a3a")])
        style.configure("TLabel", background="#1e1e1e", foreground="white")

    # ================= INTERFACE =================
    def _criar_widgets(self):
        frame_topo = tk.Frame(self.root, bg="#1e1e1e")
        frame_topo.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_topo, text="Buscar PTAX Hoje", command=self.buscar_hoje).pack(side="left", padx=5)
        ttk.Button(frame_topo, text="Buscar por Período", command=self.buscar_periodo).pack(side="left", padx=5)

        ttk.Button(
            frame_topo,
            text="Exportar Excel",
            command=lambda: exportar_excel(self.dados_atuais)
        ).pack(side="left", padx=5)

        ttk.Button(frame_topo, text="Limpar Tela", command=self.limpar_tela).pack(side="left", padx=5)

        frame_datas = tk.Frame(self.root, bg="#1e1e1e")
        frame_datas.pack(fill="x", padx=10)

        ttk.Label(frame_datas, text="Data Inicial:").pack(side="left")
        self.data_ini = DateEntry(frame_datas, date_pattern="dd-mm-yyyy")
        self.data_ini.pack(side="left", padx=5)

        ttk.Label(frame_datas, text="Data Final:").pack(side="left")
        self.data_fim = DateEntry(frame_datas, date_pattern="dd-mm-yyyy")
        self.data_fim.pack(side="left", padx=5)

        self.lbl_dashboard = ttk.Label(self.root, text="", font=("Segoe UI", 10, "bold"))
        self.lbl_dashboard.pack(fill="x", padx=10, pady=10)

        frame_tabela = tk.Frame(self.root, bg="#1e1e1e")
        frame_tabela.pack(fill="both", expand=True, padx=10)

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=("data", "compra", "venda"),
            show="headings"
        )
        self.tabela.heading("data", text="Data")
        self.tabela.heading("compra", text="Compra")
        self.tabela.heading("venda", text="Venda")
        self.tabela.pack(fill="both", expand=True)

        frame_grafico = tk.Frame(self.root, bg="#1e1e1e")
        frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.fig.patch.set_facecolor("#1e1e1e")

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ================= AÇÕES =================
    def buscar_hoje(self):
        try:
            self.dados_atuais = buscar_ptax_hoje()
            salvar_cotacoes(self.dados_atuais)
            self.atualizar_tela()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_periodo(self):
        try:
            ini = datetime.strptime(self.data_ini.get(), "%d-%m-%Y")
            fim = datetime.strptime(self.data_fim.get(), "%d-%m-%Y")

            self.dados_atuais = buscar_ptax_periodo(ini, fim)
            salvar_cotacoes(self.dados_atuais)
            self.atualizar_tela()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_tela(self):
        self.carregar_tabela()
        self.atualizar_dashboard()
        self.atualizar_grafico()

    def carregar_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        for data, compra, venda in self.dados_atuais:
            self.tabela.insert("", "end", values=(data, compra, venda))

    def atualizar_dashboard(self):
        if not self.dados_atuais:
            self.lbl_dashboard.config(text="")
            return

        vendas = [d[2] for d in self.dados_atuais]
        media = sum(vendas) / len(vendas)

        self.lbl_dashboard.config(
            text=f"Registros: {len(vendas)} | Média PTAX Venda: {media:.4f}"
        )

    def atualizar_grafico(self):
        self.ax.clear()

        if not self.dados_atuais:
            self.canvas.draw()
            return

        datas = [datetime.strptime(d[0], "%Y-%m-%d") for d in self.dados_atuais]
        vendas = [d[2] for d in self.dados_atuais]

        self.ax.plot(datas, vendas, color="#00d1ff", linewidth=2)
        self.ax.xaxis.set_major_locator(MaxNLocator(8))
        self.fig.autofmt_xdate(rotation=45)

        self.ax.set_title("Evolução da PTAX (Venda)", color="white")
        self.ax.tick_params(colors="white")
        self.ax.grid(True, color="#444444")

        self.canvas.draw()

    def limpar_tela(self):
        self.dados_atuais = []
        self.tabela.delete(*self.tabela.get_children())
        self.ax.clear()
        self.canvas.draw()
        self.lbl_dashboard.config(text="")

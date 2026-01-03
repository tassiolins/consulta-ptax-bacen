from tkinter import messagebox, filedialog
import pandas as pd


def exportar_excel(dados):
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return

    try:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )

        if not caminho:
            return

        df = pd.DataFrame(dados, columns=["Data", "Compra", "Venda"])
        df.to_excel(caminho, index=False)

        messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro ao exportar Excel", str(e))

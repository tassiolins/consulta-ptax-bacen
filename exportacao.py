import pandas as pd
from database import buscar_todas


def exportar_excel(caminho):
    dados = buscar_todas()

    if not dados:
        raise Exception("Não há dados para exportar.")

    df = pd.DataFrame(
        dados,
        columns=["Data", "PTAX Compra", "PTAX Venda"]
    )

    df.to_excel(caminho, index=False)

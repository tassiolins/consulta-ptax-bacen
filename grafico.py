import matplotlib.pyplot as plt
from database import buscar_todas


def mostrar_grafico():
    dados = buscar_todas()

    if not dados:
        raise Exception("Não há dados suficientes para gerar o gráfico.")

    datas = [d[0] for d in dados]
    vendas = [d[2] for d in dados]

    plt.figure()
    plt.plot(datas, vendas, marker="o")
    plt.title("Evolução da PTAX Venda")
    plt.xlabel("Data")
    plt.ylabel("PTAX Venda")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

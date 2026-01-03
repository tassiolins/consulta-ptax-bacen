import requests
from datetime import datetime

BASE_URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata"


def buscar_ptax_hoje():
    hoje = datetime.today().strftime("%m-%d-%Y")

    url = (
        f"{BASE_URL}/CotacaoDolarDia(dataCotacao=@dataCotacao)?"
        f"@dataCotacao='{hoje}'&$format=json"
    )

    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Não foi possível buscar PTAX hoje")

    dados = r.json().get("value", [])
    resultado = []

    for item in dados:
        data = item["dataHoraCotacao"][:10]
        compra = item["cotacaoCompra"]
        venda = item["cotacaoVenda"]
        resultado.append((data, compra, venda))

    return resultado


def buscar_ptax_periodo(data_ini, data_fim):
    ini = data_ini.strftime("%m-%d-%Y")
    fim = data_fim.strftime("%m-%d-%Y")

    url = (
        f"{BASE_URL}/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
        f"@dataInicial='{ini}'&@dataFinalCotacao='{fim}'&$format=json"
    )

    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Erro ao buscar PTAX por período")

    dados = r.json().get("value", [])
    resultado = []

    for item in dados:
        data = item["dataHoraCotacao"][:10]
        compra = item["cotacaoCompra"]
        venda = item["cotacaoVenda"]
        resultado.append((data, compra, venda))

    return resultado

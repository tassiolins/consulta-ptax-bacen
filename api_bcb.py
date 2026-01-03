import requests
from datetime import datetime, timedelta
from urllib.parse import quote

BASE_URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata"


def _buscar_periodo_bruto(data_inicio, data_fim):
    data_inicio = quote(data_inicio)
    data_fim = quote(data_fim)

    url = (
        f"{BASE_URL}/CotacaoDolarPeriodo("
        f"dataInicial=@dataInicial,"
        f"dataFinalCotacao=@dataFinalCotacao)?"
        f"@dataInicial='{data_inicio}'&"
        f"@dataFinalCotacao='{data_fim}'&"
        f"$orderby=dataHoraCotacao asc&"
        f"$format=json"
    )

    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    return resp.json().get("value", [])


def obter_ptax_hoje():
    """
    Busca PTAX usando período (método estável).
    Retorna o último dia útil disponível.
    """
    hoje = datetime.today().date()
    inicio = (hoje - timedelta(days=10)).strftime("%m-%d-%Y")
    fim = hoje.strftime("%m-%d-%Y")

    dados = _buscar_periodo_bruto(inicio, fim)

    if not dados:
        raise Exception("Não foi possível buscar PTAX recente.")

    ultimo = dados[-1]

    return [
        (
            ultimo["dataHoraCotacao"][:10],
            ultimo["cotacaoCompra"],
            ultimo["cotacaoVenda"]
        )
    ]


def obter_ptax_periodo(data_inicio, data_fim):
    """
    data_inicio e data_fim no formato YYYY-MM-DD
    """

    inicio = datetime.strptime(data_inicio, "%Y-%m-%d") - timedelta(days=5)
    fim = datetime.strptime(data_fim, "%Y-%m-%d") + timedelta(days=5)

    dados = _buscar_periodo_bruto(
        inicio.strftime("%m-%d-%Y"),
        fim.strftime("%m-%d-%Y")
    )

    if not dados:
        raise Exception("Nenhuma cotação encontrada.")

    resultado = []

    for item in dados:
        data = item["dataHoraCotacao"][:10]

        if data_inicio <= data <= data_fim:
            resultado.append(
                (
                    data,
                    item["cotacaoCompra"],
                    item["cotacaoVenda"]
                )
            )

    if not resultado:
        raise Exception("Período sem dias úteis com cotação.")

    return resultado

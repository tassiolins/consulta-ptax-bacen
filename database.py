import sqlite3


def conectar():
    return sqlite3.connect("ptax.db")


def criar_tabela():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ptax (
            data TEXT PRIMARY KEY,
            compra REAL,
            venda REAL
        )
    """)

    conn.commit()
    conn.close()


def salvar_cotacoes(cotacoes):
    conn = conectar()
    cur = conn.cursor()

    for data, compra, venda in cotacoes:
        cur.execute("""
            INSERT OR REPLACE INTO ptax (data, compra, venda)
            VALUES (?, ?, ?)
        """, (data, compra, venda))

    conn.commit()
    conn.close()


def buscar_todas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT data, compra, venda
        FROM ptax
        ORDER BY data
    """)

    dados = cur.fetchall()
    conn.close()
    return dados


def dashboard():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*),
            AVG(venda),
            MIN(venda),
            MAX(venda),
            SUM(venda)
        FROM ptax
    """)

    resultado = cur.fetchone()
    conn.close()

    return resultado

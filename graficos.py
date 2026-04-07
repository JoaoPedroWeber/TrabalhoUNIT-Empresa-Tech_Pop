import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# conexão com DW
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/dw_fatorv")


# =========================
# 1. PRODUTOS MAIS VENDIDOS
# =========================
query = """
SELECT p.nome_produto, SUM(f.quantidade) AS total
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.nome_produto
ORDER BY total DESC
LIMIT 10
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["nome_produto"], df["total"])
plt.xticks(rotation=45)
plt.title("Produtos Mais Vendidos")
plt.tight_layout()
plt.show()


# =========================
# 2. FATURAMENTO TOTAL
# =========================
query = "SELECT SUM(subtotal) AS total FROM fato_vendas"
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(["Total"], df["total"])
plt.title("Faturamento Total")
plt.tight_layout()
plt.show()


# =========================
# 3. FATURAMENTO POR CATEGORIA
# =========================
query = """
SELECT p.categoria, SUM(f.subtotal) AS total
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.categoria
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["categoria"], df["total"])
plt.xticks(rotation=45)
plt.title("Faturamento por Categoria")
plt.tight_layout()
plt.show()


# =========================
# 4. FATURAMENTO POR PRODUTO
# =========================
query = """
SELECT p.nome_produto, SUM(f.subtotal) AS total
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.nome_produto
ORDER BY total DESC
LIMIT 10
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["nome_produto"], df["total"])
plt.xticks(rotation=45)
plt.title("Faturamento por Produto")
plt.tight_layout()
plt.show()


# =========================
# 5. COMISSÃO POR VENDEDOR
# =========================
query = """
SELECT v.nome_vendedor, SUM(f.comissao) AS total
FROM fato_vendas f
JOIN dim_vendedor v ON f.id_vendedor = v.id_vendedor
GROUP BY v.nome_vendedor
ORDER BY total DESC
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["nome_vendedor"], df["total"])
plt.xticks(rotation=45)
plt.title("Comissão por Vendedor")
plt.tight_layout()
plt.show()


# =========================
# 6. FORNECEDORES POR ESTADO
# =========================
query = """
SELECT estado, COUNT(*) AS total
FROM dim_fornecedor
GROUP BY estado
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["estado"], df["total"])
plt.title("Fornecedores por Estado")
plt.tight_layout()
plt.show()


# =========================
# 7. CLIENTES POR ESTADO
# =========================
query = """
SELECT estado, COUNT(*) AS total
FROM dim_cliente
GROUP BY estado
"""
df = pd.read_sql(query, engine)

plt.figure()
plt.bar(df["estado"], df["total"])
plt.title("Clientes por Estado")
plt.tight_layout()
plt.show()
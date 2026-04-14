import pandas as pd
from sqlalchemy import create_engine, text

#.\venv\Scripts\Activate

# conexão com OLTP (fatorv)
engine_oltp = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/fatorv")

# conexão com DW
engine_dw = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/dw_fatorv")


# =========================
# LIMPEZA (EVITAR DUPLICIDADE)
# =========================
with engine_dw.connect() as conn:
    conn.execute(text("TRUNCATE TABLE fato_vendas CASCADE"))
    conn.execute(text("TRUNCATE TABLE dim_cliente CASCADE"))
    conn.execute(text("TRUNCATE TABLE dim_vendedor CASCADE"))
    conn.execute(text("TRUNCATE TABLE dim_produto CASCADE"))
    conn.execute(text("TRUNCATE TABLE dim_fornecedor CASCADE"))
    conn.execute(text("TRUNCATE TABLE dim_tempo CASCADE"))
    conn.commit()


# =========================
# EXTRAÇÃO (JOIN PRINCIPAL)
# =========================
query = """
SELECT 
    s.sale_id,
    s.date,
    c.customer_id,
    c.customer_name,
    c.state AS customer_state,
    se.seller_id,
    se.seller_name,
    se.state AS seller_state,
    se.tx_commission,
    p.product_id,
    p.product_name,
    cat.category_name,
    si.quantity,
    si.price,
    sup.supplier_id,
    sup.supplier_name,
    sup.state AS supplier_state
FROM sales s
JOIN sales_items si ON s.sale_id = si.sales_id
JOIN products p ON si.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
JOIN customers c ON s.customer_id = c.customer_id
JOIN sellers se ON s.seller_id = se.seller_id
JOIN suppliers sup ON p.supplier_id = sup.supplier_id
"""

df = pd.read_sql(query, engine_oltp)


# =========================
# TRANSFORMAÇÕES
# =========================

# textos em maiúsculo
for col in ["customer_name", "seller_name", "product_name", "category_name", "supplier_name"]:
    df[col] = df[col].str.upper()

# subtotal
df["subtotal"] = df["quantity"] * df["price"]

# comissão
df["comissao"] = df["subtotal"] * (df["tx_commission"] / 100)


# função de região
def get_region(estado):
    norte = ["AC","AP","AM","PA","RO","RR","TO"]
    nordeste = ["MA","PI","CE","RN","PB","PE","AL","SE","BA"]
    centro = ["MT","MS","GO","DF"]
    sudeste = ["SP","RJ","ES","MG"]
    sul = ["PR","SC","RS"]

    if estado in norte: return "NORTE"
    if estado in nordeste: return "NORDESTE"
    if estado in centro: return "CENTRO-OESTE"
    if estado in sudeste: return "SUDESTE"
    if estado in sul: return "SUL"

df["customer_region"] = df["customer_state"].apply(get_region)
df["supplier_region"] = df["supplier_state"].apply(get_region)


# =========================
# DIMENSÕES
# =========================

# TEMPO
dim_tempo = df[["date"]].drop_duplicates().copy()
dim_tempo.rename(columns={"date": "data"}, inplace=True)

dim_tempo["ano"] = pd.to_datetime(dim_tempo["data"]).dt.year
dim_tempo["mes"] = pd.to_datetime(dim_tempo["data"]).dt.month
dim_tempo["trimestre"] = pd.to_datetime(dim_tempo["data"]).dt.quarter

dim_tempo.reset_index(drop=True, inplace=True)
dim_tempo["id_tempo"] = dim_tempo.index + 1

df = df.merge(dim_tempo, left_on="date", right_on="data", how="left")

dim_tempo[["id_tempo","data","ano","mes","trimestre"]].to_sql(
    "dim_tempo", engine_dw, if_exists="append", index=False
)

# PRODUTO
dim_produto = df[["product_id", "product_name", "category_name"]].drop_duplicates()
dim_produto.columns = ["id_produto", "nome_produto", "categoria"]

dim_produto.to_sql("dim_produto", engine_dw, if_exists="append", index=False)


# CLIENTE
dim_cliente = df[["customer_id", "customer_name", "customer_state", "customer_region"]].drop_duplicates()
dim_cliente.columns = ["id_cliente", "nome_cliente", "estado", "region"]

dim_cliente.to_sql("dim_cliente", engine_dw, if_exists="append", index=False)


# VENDEDOR
dim_vendedor = df[["seller_id", "seller_name", "seller_state", "tx_commission"]].drop_duplicates()
dim_vendedor.columns = ["id_vendedor", "nome_vendedor", "estado", "tx_comissao"]

dim_vendedor.to_sql("dim_vendedor", engine_dw, if_exists="append", index=False)


# FORNECEDOR
dim_fornecedor = df[["supplier_id", "supplier_name", "supplier_state", "supplier_region"]].drop_duplicates()
dim_fornecedor.columns = ["id_fornecedor", "nome_fornecedor", "estado", "region"]

dim_fornecedor.to_sql("dim_fornecedor", engine_dw, if_exists="append", index=False)


# =========================
# FATO 
# =========================

fato = df[[
    "id_tempo", "product_id", "customer_id", "seller_id", "supplier_id",
    "quantity", "price", "subtotal", "comissao"
]]

fato.columns = [
    "id_tempo", "id_produto", "id_cliente", "id_vendedor", "id_fornecedor",
    "quantidade", "preco", "subtotal", "comissao"
]

fato.to_sql("fato_vendas", engine_dw, if_exists="append", index=False)


print("ETL FINALIZADO COM SUCESSO!")
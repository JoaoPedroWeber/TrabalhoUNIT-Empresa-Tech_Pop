# 📊 Projeto ETL + Data Warehouse (Modelo Estrela)

Esse projeto foi desenvolvido como parte de uma atividade acadêmica com o objetivo de praticar conceitos de **ETL (Extract, Transform, Load)** e **modelagem dimensional (modelo estrela)**.

---

## 🚀 O que o projeto faz

Basicamente:

1. Extrai dados de um banco OLTP (transacional)
2. Faz transformações (padronização, cálculos, etc.)
3. Carrega os dados em um Data Warehouse (DW)
4. Gera algumas análises e gráficos com base nesses dados

---

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* SQLAlchemy
* PostgreSQL
* Matplotlib

---

## 🧠 Modelagem

O projeto utiliza um **modelo estrela**, com:

* ⭐ **fato_vendas** (tabela fato)
* 📦 Dimensões:

  * dim_cliente
  * dim_produto
  * dim_vendedor
  * dim_fornecedor
  * dim_tempo

---

## 🔄 ETL

O processo ETL inclui:

* JOIN entre várias tabelas do banco OLTP
* Padronização de textos (uppercase)
* Cálculo de:

  * subtotal
  * comissão
* Criação de regiões (Norte, Nordeste, etc.)
* Separação em dimensões e fato

---

## 📈 Análises geradas

* Produtos mais vendidos
* Faturamento total
* Faturamento por categoria e produto
* Maiores comissões de vendedores
* Quantidade de fornecedores por estado
* Quantidade de clientes por estado

---

## ▶️ Como rodar

1. Criar e ativar um ambiente virtual:

```
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependências:

```
pip install pandas sqlalchemy psycopg2 matplotlib
```

3. Rodar o ETL:

```
python ETL.py
```

4. Rodar os gráficos:

```
python graficos.py
```

---

## 💡 Observações

* O projeto é simples e focado em aprendizado
* Não segue padrões de produção
* Algumas melhorias poderiam ser feitas (tratamento de duplicidade, logs, etc.)

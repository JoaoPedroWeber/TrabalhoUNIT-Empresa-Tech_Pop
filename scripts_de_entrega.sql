--PRODUTOS MAIS VENDIDOS

SELECT 
    p.nome_produto,
    SUM(f.quantidade) AS total_vendido
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.nome_produto
ORDER BY total_vendido DESC;

-- FATURAMENTO TOTAL

SELECT 
    SUM(subtotal) AS faturamento_total
FROM fato_vendas;

--FATURAMENTO POR CATEGORIA

SELECT 
    p.categoria,
    SUM(f.subtotal) AS faturamento
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.categoria
ORDER BY faturamento DESC;

--FATURAMENTO POR PRODUTO

SELECT 
    p.nome_produto,
    SUM(f.subtotal) AS faturamento
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.nome_produto
ORDER BY faturamento DESC;

--MAIORES COMISSÕES DE VENDEDORES

SELECT 
    v.nome_vendedor,
    SUM(f.comissao) AS total_comissao
FROM fato_vendas f
JOIN dim_vendedor v ON f.id_vendedor = v.id_vendedor
GROUP BY v.nome_vendedor
ORDER BY total_comissao DESC;

--QUANTIDADE DE FORNECEDORES POR ESTADO

SELECT 
    estado,
    COUNT(*) AS total_fornecedores
FROM dim_fornecedor
GROUP BY estado
ORDER BY total_fornecedores DESC;

--QUANTIDADE DE CLIENTES POR ESTADO

SELECT 
    estado,
    COUNT(*) AS total_clientes
FROM dim_cliente
GROUP BY estado
ORDER BY total_clientes DESC;
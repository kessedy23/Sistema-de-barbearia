-- ============================================================
--  SISTEMA DE GESTÃO DE BARBEARIA — DQL
--  Consultas: SELECTs com filtros, JOINs e ordenações
-- ============================================================

-- ============================================================
--  1. SELECT simples com filtro e ordenação
-- ============================================================

-- Todos os clientes ordenados por nome
SELECT id, nome, telefone, email, data_nascimento
FROM clientes
ORDER BY nome ASC;

-- Clientes filtrados por nome (busca parcial)
SELECT id, nome, telefone, email
FROM clientes
WHERE nome ILIKE '%carlos%'
ORDER BY nome;

-- Barbeiros ativos, ordenados por nome
SELECT id, nome, especialidade, telefone
FROM barbeiros
WHERE ativo = TRUE
ORDER BY nome;

-- Serviços ordenados por preço (mais baratos primeiro)
SELECT id, nome, preco, duracao_min
FROM servicos
ORDER BY preco ASC;

-- Agendamentos com status "agendado", ordenados por data
SELECT id, cliente_id, barbeiro_id, data_hora, status
FROM agendamentos
WHERE status = 'agendado'
ORDER BY data_hora ASC;

-- ============================================================
--  2. INNER JOIN — apenas registros com correspondência nos dois lados
-- ============================================================

-- Todos os agendamentos com detalhes completos (3 JOINs)
SELECT
    a.id                        AS agendamento_id,
    c.nome                      AS cliente,
    b.nome                      AS barbeiro,
    s.nome                      AS servico,
    s.preco                     AS preco_rs,
    a.data_hora,
    a.status,
    a.observacao
FROM agendamentos a
INNER JOIN clientes   c ON a.cliente_id  = c.id
INNER JOIN barbeiros  b ON a.barbeiro_id = b.id
INNER JOIN servicos   s ON a.servico_id  = s.id
ORDER BY a.data_hora DESC;

-- Agenda do dia (filtrando por data específica)
SELECT
    c.nome          AS cliente,
    b.nome          AS barbeiro,
    s.nome          AS servico,
    s.preco,
    a.data_hora,
    a.status,
    a.observacao
FROM agendamentos a
INNER JOIN clientes  c ON a.cliente_id  = c.id
INNER JOIN barbeiros b ON a.barbeiro_id = b.id
INNER JOIN servicos  s ON a.servico_id  = s.id
WHERE DATE(a.data_hora) = CURRENT_DATE
ORDER BY a.data_hora ASC;

-- Serviços mais populares (somente concluídos)
SELECT
    s.nome              AS servico,
    s.preco,
    COUNT(a.id)         AS total_realizados,
    SUM(s.preco)        AS receita_total
FROM servicos s
INNER JOIN agendamentos a ON s.id = a.servico_id
WHERE a.status = 'concluido'
GROUP BY s.id, s.nome, s.preco
ORDER BY total_realizados DESC;

-- ============================================================
--  3. LEFT JOIN — inclui registros sem correspondência na tabela direita
-- ============================================================

-- Todos os clientes e quantos agendamentos cada um tem
-- (inclui clientes que NUNCA agendaram — LEFT JOIN mostra NULL)
SELECT
    c.id,
    c.nome,
    c.telefone,
    COUNT(a.id)         AS total_agendamentos,
    MAX(a.data_hora)    AS ultimo_agendamento
FROM clientes c
LEFT JOIN agendamentos a ON c.id = a.cliente_id
GROUP BY c.id, c.nome, c.telefone
ORDER BY total_agendamentos DESC;

-- Clientes que NUNCA fizeram um agendamento
SELECT c.id, c.nome, c.telefone
FROM clientes c
LEFT JOIN agendamentos a ON c.id = a.cliente_id
WHERE a.id IS NULL
ORDER BY c.nome;

-- Receita gerada por cada barbeiro (inclui barbeiros sem atendimentos)
SELECT
    b.nome              AS barbeiro,
    b.especialidade,
    COUNT(a.id)         AS total_atendimentos,
    COALESCE(SUM(s.preco), 0)  AS receita_total
FROM barbeiros b
LEFT JOIN agendamentos a ON b.id = a.barbeiro_id AND a.status = 'concluido'
LEFT JOIN servicos     s ON a.servico_id = s.id
GROUP BY b.id, b.nome, b.especialidade
ORDER BY receita_total DESC;

-- ============================================================
--  4. Consultas com GROUP BY, HAVING e ORDER BY
-- ============================================================

-- Barbeiros com mais de 2 atendimentos concluídos
SELECT
    b.nome,
    COUNT(a.id) AS atendimentos
FROM barbeiros b
INNER JOIN agendamentos a ON b.id = a.barbeiro_id
WHERE a.status = 'concluido'
GROUP BY b.id, b.nome
HAVING COUNT(a.id) > 2
ORDER BY atendimentos DESC;

-- Faturamento total por mês
SELECT
    TO_CHAR(a.data_hora, 'YYYY-MM') AS mes,
    COUNT(a.id)                      AS total_atendimentos,
    SUM(s.preco)                     AS faturamento
FROM agendamentos a
INNER JOIN servicos s ON a.servico_id = s.id
WHERE a.status = 'concluido'
GROUP BY TO_CHAR(a.data_hora, 'YYYY-MM')
ORDER BY mes DESC;

-- ============================================================
--  SISTEMA DE GESTÃO DE BARBEARIA — DML
--  Exemplos de INSERT, UPDATE e DELETE
-- ============================================================

-- ============================================================
--  INSERTS
-- ============================================================

-- Usuários do sistema
-- Senha "admin123"  → SHA-256: 240be518fabd2724ddb6f04eeb1da5967448d7e831186afd31779a4c17489d38 (corrigido abaixo)
-- Senha "admin123"  → use: python3 -c "import hashlib; print(hashlib.sha256(b'admin123').hexdigest())"
INSERT INTO usuarios (username, senha, nivel) VALUES
  ('admin',    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'),
  ('operador', '1657938151c0d18bba2dd33109251099d99ac7bcdad1cc5d1ec2ee5028665adb', 'operador');
-- Senha do admin: "admin123" | Senha do operador: "op1234"

-- Clientes
INSERT INTO clientes (nome, telefone, email, data_nascimento) VALUES
  ('Carlos Alberto',  '(86) 99111-2233', 'carlos.alberto@email.com', '1990-05-15'),
  ('Marcos Vinicius', '(86) 98222-3344', 'marcos.v@email.com',       '1995-08-22'),
  ('João Paulo',      '(86) 99333-4455', NULL,                        '1988-12-01'),
  ('Rafael Souza',    '(86) 98444-5566', 'rafael.s@email.com',       '2000-03-10'),
  ('Lucas Henrique',  '(86) 99555-6677', 'lucas.h@email.com',        '1998-07-30'),
  ('Felipe Costa',    '(86) 98666-7788', NULL,                        '1985-11-05'),
  ('André Oliveira',  '(86) 99777-8899', 'andre.o@email.com',        '1993-02-18'),
  ('Tiago Almeida',   '(86) 98888-9900', 'tiago.a@email.com',        '2002-09-25');

-- Barbeiros
INSERT INTO barbeiros (nome, especialidade, telefone, ativo) VALUES
  ('Rodrigo Lima',    'Corte Degradê',        '(86) 99100-0011', TRUE),
  ('Fábio Mendes',    'Barba e Bigode',       '(86) 98200-0022', TRUE),
  ('Eduardo Santos',  'Corte Clássico',       '(86) 99300-0033', TRUE),
  ('Henrique Nunes',  'Coloração Masculina',  '(86) 98400-0044', FALSE);

-- Serviços
INSERT INTO servicos (nome, preco, duracao_min) VALUES
  ('Corte Simples',       25.00,  30),
  ('Corte Degradê',       40.00,  45),
  ('Barba Completa',      30.00,  30),
  ('Corte + Barba',       60.00,  60),
  ('Hidratação Capilar',  50.00,  45),
  ('Coloração Masculina', 80.00,  90),
  ('Sobrancelha',         15.00,  15),
  ('Corte Infantil',      20.00,  25);

-- Agendamentos (com datas variadas para demonstrar filtros)
INSERT INTO agendamentos (cliente_id, barbeiro_id, servico_id, data_hora, status, observacao) VALUES
  (1, 1, 2, '2026-04-20 09:00:00', 'concluido',  'Cliente preferiu degradê alto'),
  (2, 2, 3, '2026-04-20 10:00:00', 'concluido',  NULL),
  (3, 3, 1, '2026-04-20 11:00:00', 'concluido',  NULL),
  (4, 1, 4, '2026-04-21 09:30:00', 'concluido',  'Barba fazer no sentido do fio'),
  (5, 2, 5, '2026-04-21 14:00:00', 'cancelado',  'Cliente cancelou por compromisso'),
  (6, 3, 1, '2026-04-22 10:00:00', 'concluido',  NULL),
  (7, 1, 6, '2026-04-22 15:00:00', 'concluido',  'Coloração loiro platinado'),
  (1, 2, 3, '2026-04-25 09:00:00', 'agendado',   NULL),
  (3, 1, 2, '2026-04-25 10:30:00', 'agendado',   NULL),
  (8, 3, 8, '2026-04-25 11:00:00', 'agendado',   'Primeiro corte do cliente'),
  (2, 1, 4, '2026-04-26 09:00:00', 'agendado',   NULL),
  (4, 2, 7, '2026-04-26 10:00:00', 'agendado',   NULL),
  (5, 3, 2, '2026-04-27 09:30:00', 'agendado',   NULL);

-- ============================================================
--  UPDATES
-- ============================================================

-- Atualizar telefone de um cliente
UPDATE clientes
SET telefone = '(86) 99999-0000'
WHERE nome = 'João Paulo';

-- Marcar barbeiro como inativo
UPDATE barbeiros
SET ativo = FALSE
WHERE nome = 'Henrique Nunes';

-- Concluir um agendamento
UPDATE agendamentos
SET status = 'concluido'
WHERE id = 8;

-- Alterar preço de um serviço
UPDATE servicos
SET preco = 45.00
WHERE nome = 'Corte Degradê';

-- ============================================================
--  DELETES (exemplos — usar com cautela em produção)
-- ============================================================

-- Remover agendamentos cancelados mais antigos que 30 dias
-- DELETE FROM agendamentos
-- WHERE status = 'cancelado'
--   AND data_hora < NOW() - INTERVAL '30 days';

-- Remover cliente específico (cascata remove seus agendamentos)
-- DELETE FROM clientes WHERE id = 99;

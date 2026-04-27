-- ============================================================
--  SISTEMA DE GESTÃO DE BARBEARIA — DDL
--  Disciplina: Banco de Dados | UNIFSA
-- ============================================================

-- Extensão para UUIDs (opcional, usamos SERIAL)
-- DROP SCHEMA public CASCADE; CREATE SCHEMA public;

-- ============================================================
--  TABELA: usuarios  (autenticação do sistema)
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id          SERIAL          PRIMARY KEY,
    username    VARCHAR(50)     NOT NULL UNIQUE,
    senha       VARCHAR(64)     NOT NULL,   -- SHA-256 hex
    nivel       VARCHAR(20)     NOT NULL DEFAULT 'operador'
                                    CHECK (nivel IN ('admin','operador')),
    criado_em   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABELA: clientes
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id              SERIAL          PRIMARY KEY,
    nome            VARCHAR(100)    NOT NULL,
    telefone        VARCHAR(20),
    email           VARCHAR(100),
    data_nascimento DATE,
    criado_em       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABELA: barbeiros
-- ============================================================
CREATE TABLE IF NOT EXISTS barbeiros (
    id              SERIAL          PRIMARY KEY,
    nome            VARCHAR(100)    NOT NULL,
    especialidade   VARCHAR(100),
    telefone        VARCHAR(20),
    ativo           BOOLEAN         NOT NULL DEFAULT TRUE,
    criado_em       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABELA: servicos
-- ============================================================
CREATE TABLE IF NOT EXISTS servicos (
    id              SERIAL              PRIMARY KEY,
    nome            VARCHAR(100)        NOT NULL UNIQUE,
    preco           NUMERIC(8,2)        NOT NULL CHECK (preco > 0),
    duracao_min     INTEGER             NOT NULL CHECK (duracao_min > 0),
    criado_em       TIMESTAMP           NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABELA: agendamentos  (tabela central — FKs para as 3 acima)
-- ============================================================
CREATE TABLE IF NOT EXISTS agendamentos (
    id              SERIAL          PRIMARY KEY,
    cliente_id      INTEGER         NOT NULL
                        REFERENCES clientes(id)  ON DELETE CASCADE,
    barbeiro_id     INTEGER         NOT NULL
                        REFERENCES barbeiros(id) ON DELETE RESTRICT,
    servico_id      INTEGER         NOT NULL
                        REFERENCES servicos(id)  ON DELETE RESTRICT,
    data_hora       TIMESTAMP       NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'agendado'
                        CHECK (status IN ('agendado','concluido','cancelado')),
    observacao      TEXT,
    criado_em       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance nas JOINs e filtros frequentes
CREATE INDEX IF NOT EXISTS idx_agend_cliente  ON agendamentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_agend_barbeiro ON agendamentos(barbeiro_id);
CREATE INDEX IF NOT EXISTS idx_agend_servico  ON agendamentos(servico_id);
CREATE INDEX IF NOT EXISTS idx_agend_data     ON agendamentos(data_hora);
CREATE INDEX IF NOT EXISTS idx_agend_status   ON agendamentos(status);

-- ============================================================
-- PROJETO: Elo - Adesão ao Tratamento da Hanseníase (3FN)
-- COMPONENTE: Banco de Dados Relacional Normalizado
-- ============================================================

-- 1. Criação da Tabela de Unidades de Saúde (UBS / Municípios)
CREATE TABLE IF NOT EXISTS unidades_saude (
    id_unidade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_ubs TEXT NOT NULL,
    municipio TEXT NOT NULL,
    uf TEXT NOT NULL DEFAULT 'SP'
);

-- 2. Criação da Tabela de Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_paciente TEXT NOT NULL,
    idade INTEGER NOT NULL,
    sexo CHAR(1) CHECK(sexo IN ('M', 'F')),
    id_unidade INTEGER,
    FOREIGN KEY (id_unidade) REFERENCES unidades_saude(id_unidade)
);

-- 3. Criação da Tabela de Notificações / Casos SINAN
CREATE TABLE IF NOT EXISTS notificacoes_hanseniase (
    id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    data_notificacao DATE NOT NULL,
    forma_clinica TEXT CHECK(forma_clinica IN ('Indeterminada', 'Tuberculóide', 'Dimorfa', 'Virchowiana')),
    classificacao_operacional TEXT CHECK(classificacao_operacional IN ('Paucibacilar', 'Multibacilar')),
    esquema_terapeutico TEXT NOT NULL,
    status_adesao TEXT DEFAULT 'Em Acompanhamento',
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
);

-- ============================================================
-- INSERÇÃO DE DADOS DE TESTE (Tema: Hanseníase / ODS 3)
-- ============================================================

INSERT INTO unidades_saude (nome_ubs, municipio, uf) VALUES 
('UBS Penha de França', 'São Paulo', 'SP'),
('UBS Liberdade', 'São Paulo', 'SP');

INSERT INTO pacientes (nome_paciente, idade, sexo, id_unidade) VALUES 
('João da Silva', 45, 'M', 1),
('Maria Souza', 32, 'F', 2);

INSERT INTO notificacoes_hanseniase (id_paciente, data_notificacao, forma_clinica, classificacao_operacional, esquema_terapeutico, status_adesao) VALUES 
(1, '2026-10-15', 'Dimorfa', 'Multibacilar', 'PBM/12 doses', 'Em Acompanhamento'),
(2, '2026-11-01', 'Tuberculóide', 'Paucibacilar', 'PB/6 doses', 'Aderente');
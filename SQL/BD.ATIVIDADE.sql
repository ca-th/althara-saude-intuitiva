-- Use o banco de dados correto
USE consultorio;
 INSERT INTO medicos (nome, id_especialidade) VALUES ('Dr. Fernando Mendes', 9);  -- Gastroenterologia
INSERT INTO medicos (nome, id_especialidade) VALUES ('Dra. Luisa Neves', 7);  -- Neurologia
INSERT INTO medicos (nome, id_especialidade) VALUES ('Dr. Roberto Lima', 8); -- Pneumologia


SELECT * FROM datas WHERE data = '2025-08-01';
SELECT * FROM consultas WHERE hora = '15:00:00';
SELECT * FROM agendamentos;


-- Apaga as tabelas na ordem inversa para evitar erros de dependência
DROP TABLE IF EXISTS verificacoes;
DROP TABLE IF EXISTS agendamentos;
DROP TABLE IF EXISTS consultas;
DROP TABLE IF EXISTS agenda; -- Apaga a tabela 'agenda' se ela existir
DROP TABLE IF EXISTS medicos;
DROP TABLE IF EXISTS especialidades;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS horarios;
DROP TABLE IF EXISTS datas;

-- Agora, cria tudo novamente na ordem correta

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR (50),
    telefone VARCHAR(20)
);

CREATE TABLE especialidades (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_especialidade INT NOT NULL,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade)
);

CREATE TABLE datas (
    id_data INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL UNIQUE
);

CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    hora TIME NOT NULL UNIQUE
);

CREATE TABLE agenda (
    id_agenda INT AUTO_INCREMENT PRIMARY KEY,
    id_medico INT NOT NULL,
    id_data INT NOT NULL,
    id_horario INT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    FOREIGN KEY (id_data) REFERENCES datas(id_data),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    UNIQUE (id_medico, id_data, id_horario)
);

CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_data INT NOT NULL,
    id_horario INT NOT NULL,
    id_especialidade INT NOT NULL,
    id_medico INT NOT NULL,
    motivo_consulta VARCHAR(255),
    nome_paciente VARCHAR(100) NOT NULL,
    email_paciente VARCHAR(100),
    FOREIGN KEY (id_data) REFERENCES datas(id_data),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE especialidades;
-- Inserindo os dados de exemplo
INSERT INTO especialidades (nome) VALUES
('Clínica Geral'), 
('Cardiologia'), 
('Dermatologia'), 
('Pediatria'),
('Ortopedia'), 
('Ginecologia'), 
('Neurologia'), 
('Pneumologia'), 
('Gastroenterologia'),
('Endocrinologia'),
('Obstetrícia'),
('Urologia'),
('Oftalmologia');

SET FOREIGN_KEY_CHECKS=1;
TRUNCATE TABLE medicos;
INSERT INTO medicos (nome, id_especialidade) VALUES
('Dra. Alessandra Borges', 1),  -- 1: Clínica Geral
('Dr. João Cardoso', 2),        -- 2: Cardiologia
('Dra. Ana Luiza Mattos', 3),   -- 3: Dermatologia
('Dr. Carlos Andrade', 4),      -- 4: Pediatria
('Dra. Paula Costa', 5),        -- 5: Ortopedia
('Dr. Ricardo Alves', 6),       -- 6: Ginecologia
('Dra. Luisa Neves', 7),        -- 7: Neurologia
('Dr. Fábio Medeiros', 8),      -- 8: Pneumologia
('Dra. Carolina Faria', 9),     -- 9: Gastroenterologia
('Dr. Marcos Vinicius', 10),    -- 10: Endocrinologia
('Dra. Renata Gusmão', 11),     -- 11: Obstetrícia
('Dr. Bruno Valente', 12),      -- 12: Urologia
('Dra. Sofia Monteiro', 13);    -- 13: Oftalmologia

TRUNCATE TABLE horarios;

INSERT INTO horarios (hora) VALUES
('08:00:00'), ('08:30:00'),
('09:00:00'), ('09:30:00'),
('10:00:00'), ('10:30:00'),
('11:00:00'), ('11:30:00'),
('12:00:00'), ('12:30:00'),
('13:00:00'), ('13:30:00'),
('14:00:00'), ('14:30:00'),
('15:00:00'), ('15:30:00'),
('16:00:00'), ('16:30:00'),
('17:00:00'), ('17:30:00'),
('18:00:00'), ('18:30:00'),
('19:00:00');

-- Adicionando algumas datas de exemplo para Agosto de 2025
INSERT INTO datas (data) VALUES
('2025-08-01'), ('2025-08-04'), ('2025-08-05'), ('2025-08-06'),
('2025-08-07'), ('2025-08-08');

-- Populando a agenda (exemplo simples: todos os médicos em todas as datas e horários)
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT m.id_medico, d.id_data, h.id_horario
FROM medicos m, datas d, horarios h;
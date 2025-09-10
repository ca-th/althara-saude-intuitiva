SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS especialidades (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    cpf VARCHAR(20) UNIQUE,
    telefone VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_especialidade INT NOT NULL,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS datas (
    id_data INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    hora TIME NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS agenda (
    id_agenda INT AUTO_INCREMENT PRIMARY KEY,
    id_medico INT NOT NULL,
    id_data INT NOT NULL,
    id_horario INT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    FOREIGN KEY (id_data) REFERENCES datas(id_data),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    UNIQUE (id_medico, id_data, id_horario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS consultas (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO especialidades (nome) VALUES
('Clínica Geral'), ('Cardiologia'), ('Dermatologia'), ('Pediatria'),
('Ortopedia'), ('Ginecologia'), ('Neurologia'), ('Pneumologia'),
('Gastroenterologia'), ('Endocrinologia'), ('Obstetrícia'), ('Urologia'), ('Oftalmologia');

INSERT INTO medicos (nome, id_especialidade) VALUES
('Dra. Alessandra Borges', 1), ('Dr. João Cardoso', 2), ('Dra. Ana Luiza Mattos', 3),
('Dr. Carlos Andrade', 4), ('Dra. Paula Costa', 5), ('Dr. Ricardo Alves', 6),
('Dra. Luisa Neves', 7), ('Dr. Fábio Medeiros', 8), ('Dra. Carolina Faria', 9),
('Dr. Marcos Vinicius', 10), ('Dra. Renata Gusmão', 11), ('Dr. Bruno Valente', 12),
('Dra. Sofia Monteiro', 13);

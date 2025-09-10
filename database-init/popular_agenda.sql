INSERT INTO agenda (id_medico, id_data, id_horario, disponivel)
SELECT 
    m.id_medico, 
    d.id_data, 
    h.id_horario, 
    TRUE -- Marca como disponível
FROM 
    medicos m
CROSS JOIN 
    datas d
CROSS JOIN 
    horarios h;
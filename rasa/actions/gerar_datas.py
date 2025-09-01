import datetime


DIAS_PARA_GERAR = 365

NOME_ARQUIVO_SQL = "popular_datas.sql"

data_inicial = datetime.date.today()


lista_datas_validas = []

print(f"Gerando datas a partir de {data_inicial.strftime('%d/%m/%Y')}...")

# Loop por cada dia no período definido
for i in range(DIAS_PARA_GERAR):
    data_atual = data_inicial + datetime.timedelta(days=i)
    
    # weekday() -> Segunda é 0, Terça é 1, ..., Sábado é 5, Domingo é 6.
    # apenas se for de Segunda a Sexta (0 a 4).
    if data_atual.weekday() < 5:
        
        data_formatada = data_atual.strftime("('%Y-%m-%d')")
        lista_datas_validas.append(data_formatada)

print(f"{len(lista_datas_validas)} dias úteis encontrados.")


valores_sql = ",\n".join(lista_datas_validas)

script_sql_completo = f"""
-- Script gerado automaticamente para popular a tabela de datas.

-- Desabilita a verificação de chaves estrangeiras para permitir o TRUNCATE
SET FOREIGN_KEY_CHECKS=0;

-- Limpa a tabela de datas antigas
TRUNCATE TABLE datas;

-- Insere todas as datas de dias úteis para o próximo ano
INSERT INTO datas (data) VALUES
{valores_sql};

-- Reabilita a verificação de chaves estrangeiras
SET FOREIGN_KEY_CHECKS=1;

"""

with open(NOME_ARQUIVO_SQL, "w") as f:
    f.write(script_sql_completo)

print(f"\nPronto! O arquivo '{NOME_ARQUIVO_SQL}' foi criado com sucesso.")
print("Agora, abra este arquivo no seu programa de banco de dados e execute o script.")
import pandas as pd
import sqlite3
from datetime import datetime 

# lendo o arquivo json
df = pd.read_json("../../data/data.jsonl", lines=False)

# apresentar todas as colunas
pd.options.display.max_columns = None

# adicionar a coluna _source com valor fixo
df ["_source"] = "https://lista.mercadolivre.com.br/notebook"

# adicionar a coluna _data_coleta com a data e horario atuais
df ["_data_coleta"] = datetime.now()

# Tratando os valores nulos para colunas numericas e de texto
df["old_price_reais"] = df["old_price_reais"].fillna(0).astype(float) 
df["new_price_reais"] = df["new_price_reais"].fillna(0).astype(float) 
df["reviews_rating_number"] = df["reviews_rating_number"].fillna(0).astype(float) 

# remover parenteses do review_amount
df["reviews_amount"] = df["reviews_amount"].str.replace('[\(\)]', '', regex=True)
df["reviews_amount"] = df["reviews_amount"].fillna(0).astype(float)

# conectar/criar banco de dados SQLite 
conn = sqlite3.connect("../../data/quotes.db")

# salvar o dataframe no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# fechar conexão com banco de dados 
conn.close()

print(df.head())



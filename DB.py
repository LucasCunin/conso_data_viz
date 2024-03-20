import pandas as pd
import os
import psycopg2

# Connexion à la base de données PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)

# Lecture des données de la table t_consommation dans un DataFrame
query = "SELECT * FROM t_consommation"
df = pd.read_sql(query, connection)

# Affichage du DataFrame
print(df)
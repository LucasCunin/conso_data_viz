import pandas as pd
import os
from sqlalchemy import create_engine

# Connexion à la base de données PostgreSQL
#url dans le code (à ne pas faire mais pour les besoins du projet)

#DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = 'postgresql://gema:7jj3ZrNfd1VdmGrfx3wJ2283XyneTBOU@dpg-cntb0cacn0vc73f0f9rg-a.frankfurt-postgres.render.com:5432/dbconsommation'

engine = create_engine(DATABASE_URL)


# Lecture des données de la table t_consommation dans un DataFrame
query_c = "SELECT * FROM t_consommation_commune"
query_d = "SELECT * FROM t_consommation_departement"
query_r = "SELECT * FROM t_consommation_region"

df_commune = pd.read_sql(query_c, engine)
df_departement = pd.read_sql(query_d, engine)
df_region = pd.read_sql(query_r, engine)

print(df_commune.head())
print(df_departement.head())
print(df_region.head())



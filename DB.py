import pandas as pd
import os
from sqlalchemy import create_engine

# Connexion à la base de données PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# Lecture des données de la table t_consommation dans un DataFrame
query = "SELECT * FROM t_consommation"
df = pd.read_sql(query, engine)

# Affichage du DataFrame
print(df.shape)
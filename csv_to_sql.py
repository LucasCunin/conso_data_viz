import psycopg2
from table_omogène import super_data


reg, dep, com = super_data()

# Connect to the database
conn = psycopg2.connect(database="energie", user="postgres", host="localhost", port="5432")

cur = conn.cursor()

def create_table_query(table_name, columns, primary_key):
    query = f"CREATE TABLE {table_name} ("
    query += ", ".join([f"{col} TEXT" for col in columns])
    query += f", PRIMARY KEY ({primary_key})"
    query += ")"
    return query


for df, table_name, primary_key in zip([reg, dep, com], ["region", "departement", "commune"], ["code_region", "code_departement", "code_commune"]):
    querry = create_table_query(table_name, df.columns, primary_key)
    cur.execute(querry)

conn.commit()

cur.close()
conn.close()
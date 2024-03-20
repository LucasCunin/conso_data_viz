import psycopg2

DATABASE_URL = 'postgres://gema:7jj3ZrNfd1VdmGrfx3wJ2283XyneTBOU@dpg-cntb0cacn0vc73f0f9rg-a.frankfurt-postgres.render.com/dbconsommation'
connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()
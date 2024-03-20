import pandas as pd
import numpy as np
import requests
import json
import os

def get_url(code_commune):
    url = f'https://geo.api.gouv.fr/communes/{code_commune}?fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=geojson&geometry=centre'
    return url

def get_coordinates(com):

    unique_codes = com['code_commune'].unique()
    coordinates_dict = {}

    # Charger les coordonnées déjà obtenues si elles existent
    if os.path.exists('coordinates.json'):
        with open('coordinates.json', 'r') as f:
            coordinates_dict = json.load(f)

    total = len(unique_codes)

    for i, code in enumerate(unique_codes, 1):

        # Passer les codes déjà traités
        if code in coordinates_dict:
            continue

        url = get_url(code)
        response = requests.get(url)
        
        print(f"Traitement du code de commune {i} sur {total}: {code}, statut de la réponse: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            coordinates = data['geometry']['coordinates']
            coordinates_dict[code] = coordinates
        else:
            print(f"Erreur lors de la récupération des coordonnées pour le code de commune {code}")
            coordinates_dict[code] = [np.nan, np.nan]

        # Sauvegarder les coordonnées après chaque requête
        with open('coordinates.json', 'w') as f:
            json.dump(coordinates_dict, f)

    return coordinates_dict
    

def df_lon_lat(com, coordinates_dict):

    com['lon'] = com['code_commune'].map(coordinates_dict).apply(lambda x: x[0])
    com['lat'] = com['code_commune'].map(coordinates_dict).apply(lambda x: x[1])
        
    return com

if __name__ == '__main__':
    com = pd.read_csv('conso-elec-gaz-commune.csv', sep=';')
    coordinates_dict = get_coordinates(com)
    new_com = df_lon_lat(com, coordinates_dict)

    new_com.to_csv('new_com.csv', index=False)
    print('csv enregistré')

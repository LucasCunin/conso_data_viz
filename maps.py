import geopandas as gpd
import streamlit_folium as sf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import folium
import random

# Charger le fichier GeoJSON + data frame region
regions = gpd.read_file('regions.geojson')
regions_df = pd.read_csv('conso-elec-gaz-region.csv', sep=';')

consommation_electrique = regions_df[regions_df['filiere'] == 'Electricité'].groupby('libelle_region')['conso'].sum()
consomaation_gaz = regions_df[regions_df['filiere'] == 'Gaz'].groupby('libelle_region')['conso'].sum()

# Définir une fonction pour générer une couleur aléatoire
def random_color():
    return '#%06x' % random.randint(0, 0xFFFFFF)

# Définir une fonction pour styliser la couche GeoJSON
def style_function(feature):
    return {
        'fillOpacity': 0.5,
        'weight': 0,
        'fillColor': random_color(),
        'color': 'black'
    }

# Définir une fonction pour mettre en évidence la région au survol de la souris
def highlight_function(feature):
    return {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }


# permet de zoomer sur une partie différente de la map en cliquant sur une région
def on_each_feature(feature, layer):
    layer.on_click(lambda x: display(folium.Map(location=[46.603354, 1.888334], zoom_start=6)))


# Fonction pour créer le graphique à barres
def create_plot(region, conso_electricite=consommation_electrique , conso_gaz=consomaation_gaz):
    
    df_region = pd.DataFrame({
        'type_consommation': ['Electricité', 'Gaz'],
        'conso': [conso_electricite.loc[region], conso_gaz.loc[region]]
    })
    
    fig, ax = plt.subplots()
    sns.barplot(data=df_region, x='type_consommation', y='conso', ax=ax)
    plt.close(fig)
    return fig

# Fonction pour encoder le graphique en image PNG
def fig_to_png_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    return base64.b64encode(buf.getvalue()).decode()

# Ajouter les régions à la carte
for feature in regions['features']:
    region_name = feature['properties']['nom']
    
    # Créer le graphique pour la région
    fig = create_plot(region_name)
    
    # Encoder le graphique en image PNG
    png = fig_to_png_base64(fig)
    
    # Créer l'élément HTML pour le graphique
    html = '<img src="data:image/png;base64,{}">'.format(png)


def main():
    # Créer une carte
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter la couche GeoJSON à la carte
    folium.GeoJson(
        regions,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['nom'], labels=True),
        popup=folium.Popup(html)
    ).add_to(m)

    # Afficher la carte
    #m

    #Aficher la carte dans streamlit
    sf.folium_static(m)

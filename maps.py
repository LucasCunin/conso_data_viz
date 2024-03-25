import geopandas as gpd
import streamlit_folium as sf
import folium
import random

# Charger le fichier GeoJSON
regions = gpd.read_file('regions.geojson')

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



def main():
    # Créer une carte
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter la couche GeoJSON à la carte
    folium.GeoJson(
        regions,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['nom'], labels=True)
    ).add_to(m)

    # Afficher la carte
    #m

    #Aficher la carte dans streamlit
    sf.folium_static(m)

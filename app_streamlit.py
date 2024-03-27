import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from maps import main
#from DB import df # import du DataFrame df depuis la DB


#récupération des dataframe
region_df = pd.read_csv('conso-elec-gaz-region.csv', sep=';')
departement_df = pd.read_csv('conso-elec-gaz-departement.csv', sep = ';')

# Définir les pages
##############################################_Page 1_##############################################
def page1(df = region_df):
    st.title("Carte de la consommation d'électricité par région")
    main()


##############################################_Page 2_##############################################
def page2(df = region_df):
    st.title("Graph région")

    #dataframe pour les graph
    grouped_data = df.groupby(['annee', 'libelle_region'])['conso'].sum().unstack()

    df_electricite_sum = df[df['filiere'] == 'Electricité'].groupby(['annee', 'libelle_region'])['conso'].sum().unstack()
    df_gaz_sum = df[df['filiere'] == 'Gaz'].groupby(['annee', 'libelle_region'])['conso'].sum().unstack()

    df_electricite = df[df['filiere'] == 'Electricité']
    df_gaz = df[df['filiere'] == 'Gaz']

    conso_par_code_electricite = df_electricite.groupby('libelle_categorie_consommation')['conso'].sum()
    conso_par_code_gaz = df_gaz.groupby('libelle_categorie_consommation')['conso'].sum()

    consommation_evolution_electricite = df_electricite.groupby(['annee', 'libelle_categorie_consommation'])['conso'].sum().unstack()
    consommation_evolution_gaz = df_gaz.groupby(['annee', 'libelle_categorie_consommation'])['conso'].sum().unstack()

    #graph1: Consomation total GAz + elec au fil des année
    
    st.markdown("<center>Consommation par région au fil des années</center>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    sns.lineplot(data=grouped_data, markers=True, ax=ax)
    plt.xlabel('Année')
    plt.ylabel('Consommation')
    #plt.title('Consommation par région au fil des années')
    plt.grid(True)
    plt.legend(title='Région', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    st.markdown("""--------------
    
    """)

    #graph2: meme chose mais séparer par filière (gaz et elec)
    st.markdown("<center>Consommation d'electricité par région au fil des années</center>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    sns.lineplot(data=df_electricite_sum, markers=True, ax=ax)
    plt.xlabel('Année')
    plt.ylabel('Consommation Electricité')
    #plt.title('Consommation d\'electricité par région au fil des années')
    plt.grid(True)
    plt.legend(title='Région', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    st.markdown("<center>Consommation de gaz par région au fil des années</center>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    sns.lineplot(data=df_gaz_sum, markers=True, ax=ax)
    plt.xlabel('Année')
    plt.ylabel('Consommation Gaz')
    #plt.title('Consommation de gaz par région au fil des années')
    plt.grid(True)
    plt.legend(title='Région', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

    st.markdown("""--------------
    
    """)

    #graph 3 : consommation elec (camamber) par catégorie
    st.markdown("<center>Répartition de la consommation d'électricité par type de consomateur</center>", unsafe_allow_html=True)
    # Créer le pie chart pour la filière Electricité
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.pie(conso_par_code_electricite, labels=conso_par_code_electricite.index, autopct='%1.1f%%', colors=sns.color_palette("cool"))
    #plt.title('Répartition de la consommation par code de catégorie (Électricité)')
    plt.axis('equal')
    st.pyplot(fig1)

    #graph 4 : consommation gaz (camamber) par catégorie
    st.markdown("<center>Répartition de la consommation de gaz par type de consomateur</center>", unsafe_allow_html=True)
    # Créer le pie chart pour la filière Gaz
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.pie(conso_par_code_gaz, labels=conso_par_code_gaz.index, autopct='%1.1f%%', colors=sns.color_palette("YlOrRd"))
    #plt.title('Répartition de la consommation par code de catégorie (Gaz)')
    plt.axis('equal')
    st.pyplot(fig2)

    
    st.markdown("""--------------
    
    """) 

    #graph 5 et 6 evolution du tyoe de consomateur en focntion de l'année
    st.markdown('<center>Évolution de la consommation par catégorie pour l\'électricité</center>', unsafe_allow_html=True)
    #elec
    plt.figure(figsize=(12, 8))
    consommation_evolution_electricite.plot(kind='bar', stacked=True, ax=plt.subplot(211), colormap="cool")
    #plt.title("Évolution de la consommation par catégorie pour l'électricité")
    plt.xlabel("Année")
    plt.ylabel("Consommation")
    plt.legend(title='Code catégorie', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown('<center>Évolution de la consommation par catégorie pour le gaz</center>', unsafe_allow_html=True)
    #gaz
    plt.figure(figsize=(12, 8))
    consommation_evolution_gaz.plot(kind='bar', stacked=True, ax=plt.subplot(212), colormap="YlOrRd")
    #plt.title("Évolution de la consommation par catégorie pour le gaz")
    plt.xlabel("Année")
    plt.ylabel("Consommation")
    plt.legend(title='Code catégorie', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)



##############################################_Page 3_##############################################

def page3(df = departement_df):
    st.title("consommation par département")

    #plot 1 : consommation par département au fil des années
    regions = df['libelle_region'].unique()
    #drop les dom 
    dom_tom = ['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte']
    regions = [region for region in regions if region not in dom_tom]

    # Ajout de l'option 'All'
    regions = list(regions)
    regions.insert(0, 'All')

    # Création du menu déroulant
    selected_region = st.selectbox('Choisissez une région', regions)

    if selected_region == 'All':
        for region in regions[1:]:
            # Filter the data for the specific region
            region_data = df[df['libelle_region'] == region]
            # Group the consumption by year and by department
            grouped_data = region_data.groupby(['annee', 'libelle_departement'])['consototale'].sum().unstack()

            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=grouped_data, markers=True, ax=ax)
            plt.xlabel('Année')
            plt.ylabel('Consommation')
            plt.title(f'{region}')
            plt.legend(title='Département', bbox_to_anchor=(1, 1))
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(fig)

    else:
        # Filter the data for the selected region
        region_data = df[df['libelle_region'] == selected_region]
        # Group the consumption by year and by department
        grouped_data = region_data.groupby(['annee', 'libelle_departement'])['consototale'].sum().unstack()

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=grouped_data, markers=True, ax=ax)
        plt.xlabel('Année')
        plt.ylabel('Consommation')
        plt.title(f'{selected_region}')
        plt.legend(title='Département', bbox_to_anchor=(1, 1))
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("""--------------
    """)

    #plot 2 : par de la conssomation par filière 
    sum_conso_by_operator = df.groupby('operateur')['consototale'].sum()
    total_sum = sum_conso_by_operator.sum()

    #regrouper les plus petits opérateurs ceux en dessous de 5% de la consommation totale
    filtered_operators = sum_conso_by_operator[sum_conso_by_operator >= 0.05 * total_sum]
    autres = sum_conso_by_operator[sum_conso_by_operator < 0.05 * total_sum].sum()
    filtered_operators = pd.concat([filtered_operators, pd.Series(autres, index=['Autres'])])

    # Création du pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(filtered_operators, labels=filtered_operators.index, 
            autopct='%1.1f%%', colors=sns.color_palette('coolwarm'))
    plt.title('Part de la consommation par opérateur')
    plt.axis('equal') 
    st.pyplot(plt)

####################################################################################################


# Créer un dictionnaire pour mapper les noms de pages aux fonctions
pages = {
    "Carte des conso !": page1,
    "La consommation par régions": page2,
    "La consommation par département": page3,
}

# Créer une barre latérale pour la navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller à", list(pages.keys()))

# Appeler la fonction de page correspondante
page = pages[selection]()
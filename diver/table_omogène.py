import pandas as pd

def super_data():
    #importé les CSV
    reg = pd.read_csv('conso-elec-gaz-region.csv', sep=';')
    dep = pd.read_csv('conso-elec-gaz-departement.csv', sep=';')
    com = pd.read_csv('conso-elec-gaz-commune.csv', sep=';')

    #faire en sorte d'avoir les meme valeur pour opérateur dans les 3 table
    reg.operateur = reg.operateur.replace("Régie d'électricité de Montvalezan-la-Rosière", "Régie d’électricité de Montvalezan-La-Rosière")

    #faire en sorte d'avoir les meme type pour code régions dans les 3 table
    reg = reg[reg['code_region'] != 'Fr']
    reg = reg[reg['code_region'] != 'XX']
    reg.code_region = reg.code_region.astype(int)

    #print(np.sort(reg.code_region.unique()))
    #print(np.sort(dep.code_region.unique()))

    #Avoir le meme ype de code département dans les 2 talbe
    lst_to_drop = [i for i in com.code_departement.unique() if i not in dep.code_departement.unique()]
    com = com[~com.code_departement.isin(lst_to_drop)]

    com = com[~com.code_departement.str.contains('[a-zA-Z]', regex=True)]
    dep = dep[~dep.code_departement.str.contains('[a-zA-Z]', regex=True)]

    com.code_departement = com.code_departement.astype(int)
    dep.code_departement = dep.code_departement.astype(int)

    #print(np.sort(com.code_departement.unique()))
    #print(np.sort(dep.code_departement.unique()))

    return reg, dep, com



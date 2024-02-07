from utils.utils import *
from utils.scenarios import get_data
import pandas as pd

def simulation(scenario, graph, Pathway_Feedstock=None):
    error = 'Simulation successful'
    
    #Get SAF prices according to pathway selected
    if Pathway_Feedstock == None :
        P_SAF_selected = pd.read_excel('utils/Base prix.xlsx', usecols=[2], sheet_name='Price modeling ADEME', header=0).iloc[0:8].values.flatten().tolist()
    else:
        SAF_prices = pd.read_excel('utils/Base prix.xlsx', usecols=[2, 7], sheet_name='Price', header=0).iloc[4:19]
        SAF_unique_price = SAF_prices.loc[SAF_prices['Pathway_Feedstock'] == Pathway_Feedstock, 'Price upbound (USD/L)'].values[0]
        P_SAF_selected = [SAF_unique_price, SAF_unique_price, SAF_unique_price, SAF_unique_price, SAF_unique_price, SAF_unique_price, SAF_unique_price, SAF_unique_price]

    # Check if some arguments are incorrects 
    if scenario not in ['luftansa', 'skyalp', 'ryanair']:
        print('ERROR, scenario not in [luftansa, skyalp, ryanair]')
        error = 'Simulation failed'
    if graph not in ['all', 'prices', 'carbon', 'hypotheses']:
        print('ERROR, graph not in [all, prices, carbon, hypotheses]')
        error = 'Simulation failed'

    # Get data from simulation
    data = get_data(scenario, P_SAF_selected)

    #Print graphs of the simulation
    if graph == 'all':
        graphique(*data['graphique'])
        graphique_emissionscarbone(*data['emissionscarbone'])
        graphique_hypotheses(*data['hypotheses'])
    elif graph == 'prices':
        graphique(*data['graphique'])
    elif graph == 'carbon':
        graphique_emissionscarbone(*data['emissionscarbone'])
    elif graph == 'hypotheses':
        graphique_hypotheses(*data['hypotheses'])
    return error


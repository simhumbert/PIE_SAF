from utils.data import *
import matplotlib.pyplot as plt

def calculs_with_saf(beg,             # int : Année de départ
                     end,             # int : Année de fin
                     V,               # array : Volume de carburant / an (hypothèse)
                     I,               # array : taux d'incorporation / an (hypothèse)
                     A,               # float : allowance d'émissions gratuites en 2023 (hypothèse)
                     Q,               # array : quotat carbones pour l'Europe (hypothèse)
                     P_CO2,           # array : prix de la tonne carbone chaque année (hypothèse)
                     P_SAF,           # float : prix du SAF au litre (hypothèse)
                     P_k,             # float : prix du kérosène au litre (hypothèse)
                     R):              # float : allowance gratuite de réduction du surcoût lié au SAF (hypothèse)               
    years = beg - end +1
    # Cas sans SAF : 
    C_MP_k0 = V * P_k
    C_CO2_k0 = (alpha*V - A*Q) * P_CO2

    # Cas avec SAF : 
    V_SAF = np.zeros(years)
    V_k = np.zeros(years)

    for y in range(len(V)):
        V_SAF[y]    = V[y]*I[y]
        V_k[y]  = V[y]*(1-I[y])

    C_CO2_k = (alpha*V_k - A*Q) * P_CO2
    C_MP_SAF = V_SAF * P_SAF
    C_MP_k = V_k * P_k
    R_UE = -R *(C_MP_k+ C_MP_SAF - C_MP_k0 )

    return C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0

def graphique(data, labels, debut, fin):         # Diagramme batôns des coûts
  years = np.arange(debut, fin+1)

  # Tracer le graphique
  fig = plt.figure(figsize=(20, 6))
  width = 0.1

  colors =['#A9CCE3',
           '#E74C3C',
          '#7FB3D5',
          '#5499C7',
          '#2980B9',
          '#7F8C8D']

  bottoms = np.array([np.zeros(len(data[0])),
                      data[0,:],
                      data[0,:]+data[1,:],
                      data[0,:]+data[1,:]+data[2,:],
                      np.zeros(len(data[0,:])),
                      np.zeros(len(data[0,:]))])

  for i in range(0,len(data[:,0])-1):
    bar = plt.bar(years+i*width, data[i,:], label=labels[i], width=width, bottom=bottoms[i,:], align='center', color=colors[i])
    plt.bar_label(bar, label_type='center')

  # Affichage du scénario de référence
  bar = plt.bar(years+(len(data[:,0])+1)*width, data[-1,:], label=labels[-1], width=width, bottom=bottoms[-1,:], align='center', color=colors[-1])
  plt.bar_label(bar, label_type='center')

  # Personnaliser le graphique
  plt.xlabel('Années')
  plt.ylabel('Prix (m$)')
  plt.legend()
  plt.xticks(years + 1.5*width, years)

  # Afficher le graphique
  plt.show()
  
def graphique_emissionscarbone(emissions_carbone):       # Fonction pour tracer les emissions carbone des 3 différents scénarios
  annees = list(range(2023, 2031))  # Créer une liste d'années de 2023 à 2030
  figc = plt.figure(figsize=(20, 6))
  
  plt.plot(annees, emissions_carbone[0], marker='s', label='Scénario 1 : No SAF')
  plt.plot(annees, emissions_carbone[1], marker='o', label='Scénario 2 : Incorporation suivant les mandats européens')
  plt.plot(annees, emissions_carbone[2], marker='^', label='Scénario 3 : Incorporation custom')
  
  plt.title('Émissions de carbone de 2023 à 2030')
  plt.xlabel('Année')
  plt.ylabel('Émissions de carbone')
  plt.legend()  # Afficher la légende
  
  plt.grid(True)
  plt.tight_layout()
  plt.show()
  


def fleet_carbu(annee_start, annee_end,       # int : Années de début et fin de simulation (hypothèse)
                CO2_em_start,                 # float : Emissions de CO2 à l'année de départ (donnée)
                nbr_old_start,                # int : nombre d'anciens modèles au départ (donnée)
                nbr_new_start,                # int : nombre de nouveaux modèles au départ (donnée)
                replacement_nbr,              # int : nombre d'avions remplacés annuellement (hypothèse)
                em_reduction_rate,            # float : pourcentage de réduction d'émissions des nouveaux modèles (hypothèse)
                nbr_add_annual                # int : augmentation annuelle du nombre total d'appareils (hypothèse)
                ):
    
    
    nbr_annee = annee_end - annee_start +1
    CO2_em = np.zeros(nbr_annee)
    CO2_em[0] = CO2_em_start
    nbr_old = nbr_old_start
    nbr_new = nbr_new_start
    em_factor_old = (CO2_em_start*nbr_old/(nbr_old+nbr_new*(1-em_reduction_rate)))/nbr_old
    em_factor_new = (CO2_em_start*nbr_new*(1-em_reduction_rate)/(nbr_old+nbr_new*(1-em_reduction_rate)))/nbr_new
    
    for i in range(1, nbr_annee):
        nbr_old = max(nbr_old-replacement_nbr, 0)
        nbr_new = nbr_new+replacement_nbr+nbr_add_annual
        CO2_em_old = nbr_old*em_factor_old
        CO2_em_new = nbr_new*em_factor_new
        
        if nbr_old==0:
            replacement_nbr = 0
        
        CO2_em[i] = CO2_em_old + CO2_em_new
    
    volume_carbu_an = CO2_em * 1000000/(nrj_volum_kero * core_lca_kero)
    
    return volume_carbu_an, CO2_em



def graphique_hypotheses(debut, fin, carbonprice, quota_eu, incorpo_saf):
  # Prix du carbone
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.plot(range(debut, fin + 1), carbonprice, label='Prix du Carbone (€/tCO2eq.)', marker='o')
  ax.set_xlabel('Années')
  ax.set_ylabel('Prix (€/tCO2eq.)')
  ax.set_title('Évolution du Prix du Carbone')
  ax.legend()
  plt.grid(True)
  plt.show()


  # Quota carbone EU
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.plot(range(debut, fin + 1), quota_eu*100, label='Quota Carbone de l\'UE (%)', marker='s')
  ax.set_xlabel('Année')
  ax.set_ylabel('Proportion du quota carbone couvert par les allowances gratuites (%)')
  ax.set_title('Évolution du Quota Carbone de l\'UE')
  ax.legend()
  plt.grid(True)
  plt.show()

  # Incorporation des SAF en Eu
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.plot(range(debut, fin + 1), incorpo_saf*100, label='Incorporation SAF de l\'UE (%)', marker='^')
  ax.set_xlabel('Année')
  ax.set_ylabel('Incorporations SAF (%)')
  ax.set_title('Évolution de l\'Incorporation SAF de l\'UE')
  ax.legend()
  plt.grid(True)
  plt.tight_layout()
  plt.show()   
from utils.hypothesis import *
import matplotlib.pyplot as plt

def calculs_with_saf(years,           # int : Nombre d'années (hypothèse)
                     V,               # array : Volume de carburant / an (hypothèse)
                     I,               # array : taux d'incorporation / an (hypothèse)
                     A,               # float : allowance d'émissions gratuites en 2023 (hypothèse)
                     Q,               # array : quotat carbones pour l'Europe (hypothèse)
                     P_CO2,           # array : prix de la tonne carbone chaque année (hypothèse)
                     P_SAF,           # float : prix du SAF au litre (hypothèse)
                     P_k,             # float : prix du kérosène au litre (hypothèse)
                     R):              # float : allowance gratuite de réduction du surcoût lié au SAF (hypothèse)
                     

    # Cas sans SAF : 
    prix_kero_an = V * P_k
    prix_carbone_kero_an = (CO2_em - A*Q) * P_CO2

    # Cas avec SAF : 
    volume_saf_an = np.zeros(years)
    volume_kero_saf_an = np.zeros(years)

    for y in range(len(V)):
        volume_saf_an[y]    = V[y]*I[y]
        volume_kero_saf_an[y]  = V[y]*(1-I[y])

    # Calcul cout carbone kérosène
    CO2_em_kero = volume_kero_saf_an * nrj_volum_kero * core_lca_kero /1000000
    prix_carbone_kero_saf = ( CO2_em_kero - A*Q) * P_CO2

    # Calcul surcoût SAF
    prix_saf_an = volume_saf_an * P_SAF
    prix_kero_saf_an = volume_kero_saf_an * P_k

    prix_total_an = prix_saf_an + prix_kero_saf_an

    prix_extra_an =  prix_total_an - prix_kero_an

    allowances_extra_an = -prix_extra_an * R

    prix_ap_allowances_an = prix_total_an + allowances_extra_an

    return prix_kero_saf_an, prix_carbone_kero_saf, prix_saf_an, allowances_extra_an, prix_ap_allowances_an, prix_kero_an, prix_carbone_kero_an

def graphique(data, labels):         # Diagramme batôns des coûts
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
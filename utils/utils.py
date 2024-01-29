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
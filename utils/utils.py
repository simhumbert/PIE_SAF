from hypothesis import *
import matplotlib as plt

def calculs_with_saf(nbr_annee,           # int : Nombre d'années (hypothèse)
                     volume_carbu_an,     # array : Volume de carburant / an (hypothèse)
                     incorpo_saf,         # array : taux d'incorporation / an (hypothèse)
                     allowance_free_2023, # float : allowance d'émissions gratuites en 2023 (hypothèse)
                     quota_eu,            # array : quotat carbones pour l'Europe (hypothèse)
                     carbonprice,         # array : prix de la tonne carbone chaque année (hypothèse)
                     price_saf,           # float : prix du SAF au litre (hypothèse)
                     price_kero,          # float : prix du kérosène au litre (hypothèse)
                     allowance_SAF        # float : allowance gratuite de réduction du surcoût lié au SAF (hypothèse)
                     ):

    # Cas sans SAF : 
    prix_kero_an = volume_carbu_an * price_kero
    prix_carbone_kero_an = (CO2_em - allowance_free_2023*quota_eu) * carbonprice

    # Cas avec SAF : 
    volume_saf_an = np.zeros(nbr_annee)
    volume_kero_saf_an = np.zeros(nbr_annee)

    for y in range(len(volume_carbu_an)):
        volume_saf_an[y]    = volume_carbu_an[y]*incorpo_saf[y]
        volume_kero_saf_an[y]  = volume_carbu_an[y]*(1-incorpo_saf[y])

    # Calcul cout carbone kérosène
    CO2_em_kero = volume_kero_saf_an * nrj_volum_kero * core_lca_kero /1000000
    prix_carbone_kero_saf = ( CO2_em_kero - allowance_free_2023*quota_eu) * carbonprice

    # Calcul surcoût SAF
    prix_saf_an = volume_saf_an * price_saf
    prix_kero_saf_an = volume_kero_saf_an * price_kero

    prix_total_an = prix_saf_an + prix_kero_saf_an

    prix_extra_an =  prix_total_an - prix_kero_an

    allowances_extra_an = -prix_extra_an * allowance_SAF

    prix_ap_allowances_an = prix_total_an + allowances_extra_an

    return prix_kero_saf_an, prix_carbone_kero_saf, prix_saf_an, allowances_extra_an, prix_ap_allowances_an, prix_kero_an, prix_carbone_kero_an

def graphique(data, labels):
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
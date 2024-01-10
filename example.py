from hypothesis import *
from utils import *

"""## Scénario 1 : No SAF
"""

"""1. Calculs"""

prix_kero_an = volume_kero_an * price_kero
prix_carbone_kero = (CO2_em - allowance_free_2023*quota_eu) * carbonprice

"""2. Graphique"""

labels =['Kérosène',
        'Cout carbone du kérosène',
         'Prix final après allowances gratuites']

data = np.array([np.round(prix_kero_an/1000000,2),
                 np.round(CO2_em*carbonprice/1000000,2),
                 np.round((prix_carbone_kero + prix_kero_an)/1000000,2)])

years = np.arange(debut, fin+1)

# Tracer le graphique
fig = plt.figure(figsize=(20, 6))
width = 0.1

colors =['#5499C7',
         '#2980B9',
        '#7F8C8D']

bottoms = np.array([np.zeros(len(data[0])),
                    data[0,:],
                   np.zeros(len(data[0]))])

for i in range(0,len(data[:,0])):
  bar = plt.bar(years+0.1*i, data[i,:],bottom=bottoms[i], label=labels[i], width=width, align='center', color=colors[i])
  plt.bar_label(bar, label_type='center')


# Personnaliser le graphique
plt.xlabel('Années')
plt.ylabel('Prix (m$)')
plt.legend()
plt.xticks(years, years)

# Afficher le graphique
plt.show()

"""## Scénario 2 : Incorporation en ligne avec les mandats européens

1. Calculs
"""

# Calcul des volumes de SAF et de kéro
volume_saf_an = np.zeros(nbr_annee)
volume_kero_saf_an = np.zeros(nbr_annee)
for y in range(len(volume_kero_an)):
  volume_saf_an[y]    = volume_kero_an[y]*incorpo_saf_eu[y]
  volume_kero_saf_an[y]  = volume_kero_an[y]*(1-incorpo_saf_eu[y])

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


"""2. Graphique"""

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

labels =['Kérosène',
         ' Coût carbone kérosène (après quotas gratuits)',
          'SAF',
          'Allowances',
          'Prix Final',
          'Scénario NO SAF']

data = np.array([np.round(prix_kero_saf_an/1000000,2),
                 np.round(prix_carbone_kero_saf/1000000,2),
                  np.round(prix_saf_an/1000000,2),
                  np.round(allowances_extra_an/1000000,2),
                  np.round((prix_ap_allowances_an+prix_carbone_kero_saf)/1000000,2),
                  np.round((prix_carbone_kero + prix_kero_an)/1000000,2)])

graphique(data, labels)

"""## Scénario 3 : incorporations modifiables

1. Hypothèses d'incorporation supplémentaires
"""

# Incorporations
incorpo_2023 = 0              # *100 %
incorpo_2024 = 0.05           # *100 %
incorpo_2025 = 0.10           # *100 %
incorpo_2026 = 0.15           # *100 %
incorpo_2027 = 0.20           # *100 %
incorpo_2028 = 0.30           # *100 %
incorpo_2029 = 0.40           # *100 %
incorpo_2030 = 0.50           # *100 %

incorpo_saf = [incorpo_2023, incorpo_2024, incorpo_2025, incorpo_2026, incorpo_2027, incorpo_2028, incorpo_2029, incorpo_2030]

"""Calcul :"""

# Calcul des volumes de SAF et de kéro
volume_saf_an_3 = np.zeros(nbr_annee)
volume_kero_saf_an_3 = np.zeros(nbr_annee)
for y in range(len(volume_kero_an)):
  volume_saf_an_3[y]    = volume_kero_an[y]*incorpo_saf[y]
  volume_kero_saf_an_3[y]  = volume_kero_an[y]*(1-incorpo_saf[y])

# Calcul cout carbone kérosène
CO2_em_kero_3 = volume_kero_saf_an_3 * nrj_volum_kero * core_lca_kero /1000000
prix_carbone_kero_saf_3 = ( CO2_em_kero_3 - allowance_free_2023*quota_eu) * carbonprice

# Calcul surcoût SAF
prix_saf_an_3 = volume_saf_an_3 * price_saf
prix_kero_saf_an_3 = volume_kero_saf_an_3 * price_kero

prix_total_an_3 = prix_saf_an_3 + prix_kero_saf_an_3

prix_extra_an_3 =  prix_total_an_3 - prix_kero_an

allowances_extra_an_3 = -prix_extra_an * allowance_SAF

prix_ap_allowances_an_3 = prix_total_an_3 + allowances_extra_an_3

"""Graphique :"""

labels = ['Kérosène',
          ' Coût carbone kérosène (après quotas gratuits)',
          'SAF',
          'Allowances',
          'Prix Final',
          'Scénario NO SAF']

data = np.array([np.round(prix_kero_saf_an_3/1000000,2),
                 np.round(prix_carbone_kero_saf_3/1000000,2),
                 np.round(prix_saf_an_3/1000000,2),
                 np.round(allowances_extra_an_3/1000000,2),
                 np.round((prix_ap_allowances_an_3+prix_carbone_kero_saf_3)/1000000,2),
                 np.round((prix_carbone_kero + prix_kero_an)/1000000,2)])

graphique(data, labels)


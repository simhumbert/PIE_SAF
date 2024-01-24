from utils.hypothesis import *
from utils.utils import *

"""## Scénario 1 : No SAF
"""

"""1. Calculs"""

prix_kero_an = volume_carbu_an * price_kero
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





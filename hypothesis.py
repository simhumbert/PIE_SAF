# Importations
import numpy as np
import matplotlib.pyplot as plt

"""## Hypothèses et Calculs préliminaires

1. Hypothèses
"""

# Emissions de CO2 en 2023
CO2_2023 = 10000.0        # tCO2/an

# Augmentation des emissions en tC02 / an
CO2_supp = 10000.0        # tCO2/an

# Période considérée
debut = 2023
fin = 2030

# Carburant : ENI biofuel HEFA Waste Oil
price_saf = 1.92          # USD/L
core_lca_SAF = 13.9       # gCO2eq./MJ

# Référent kérosène
price_kero = 0.7         # USD/L
core_lca_kero = 88.8      # gCO2eq./MJ

# Compensation du surcoût lié à l'achat de SAF
allowance_SAF = 0.70      # *100 % : proportion du surcoût couvert par le don d'allowances gratuites

# Quota carbone EU ETS (fin des quotas gratuits)
quota_2023 = 1            # *100 %
quota_2024 = 0.75         # *100 %
quota_2025 = 0.50         # *100 %
quota_2026 = 0            # *100 %

# Coût total d'une tonne de carbone
carbonprice_2023 = 84.    # €/tCo2eq.
carbonprice_2030 = 150.   # €/tCo2eq.
carbonprice_2035 = 125.   # €/tCo2eq.

# Allowance gratuite en 2023 : émissions de CO2 2023
allowance_free_2023 = CO2_2023

# Objectifs incorporation SAF d'après les mandats européens
obj_2023 = 0              # *100 %
obj_2025 = 0.02           # *100 %
obj_2030 = 0.05           # *100 %

"""2. Données"""

nrj_combu_kero = 43.15                          # MJ/kg
densite_kero = 0.81                             # kg/L
nrj_volum_kero = nrj_combu_kero * densite_kero  # MJ/L

"""3. Calculs préliminaires"""

# Tableau des émissions / an
nbr_annee = fin - debut +1
CO2_em = np.linspace(CO2_2023, CO2_supp * nbr_annee, nbr_annee)

volume_carbu_an = CO2_em * 1000000/(nrj_volum_kero * core_lca_kero)

# Objectifs incorporations saf EU
incorpo_saf_eu = np.concatenate((np.linspace(obj_2023, obj_2025, 2025-debut+1)[:-1],
                                 np.linspace(obj_2025, obj_2030, fin-2025+1)))

# Quotas carbone
quota_eu = np.array([quota_2023, quota_2024, quota_2025, quota_2026, 0, 0, 0, 0])

# Carbon price
carbonprice = np.linspace(carbonprice_2023, carbonprice_2030, fin-debut+1)

"""4. Affichage des hypothèses"""

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
ax.plot(range(debut, fin + 1), incorpo_saf_eu*100, label='Incorporation SAF de l\'UE (%)', marker='^')
ax.set_xlabel('Année')
ax.set_ylabel('Incorporations SAF (%)')
ax.set_title('Évolution de l\'Incorporation SAF de l\'UE')
ax.legend()
plt.grid(True)
plt.show()
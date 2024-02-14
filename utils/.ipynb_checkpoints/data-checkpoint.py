import numpy as np


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

# Objectifs incorporation SAF d'après les mandats européens
obj_2023 = 0              # *100 %
obj_2025 = 0.02           # *100 %
obj_2030 = 0.05           # *100 %

nrj_combu_kero = 43.15                          # MJ/kg
densite_kero = 0.81                             # kg/L
nrj_volum_kero = nrj_combu_kero * densite_kero  # MJ/L
alpha = nrj_volum_kero*core_lca_kero/1000000    # tCO2eq./L



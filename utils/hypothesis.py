import numpy as np
from data import *


# Emissions de CO2 en 2023
CO2_2023 = 10000.0        # tCO2/an

# Augmentation des emissions en tC02 / an
CO2_supp = 10000.0        # tCO2/an

# Période considérée
debut = 2023
fin = 2030

# Allowance gratuite en 2023 : émissions de CO2 2023
allowance_free_2023 = CO2_2023

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

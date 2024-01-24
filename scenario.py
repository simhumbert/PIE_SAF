from utils.hypothesis import *
from utils.utils import *


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


prix_kero_saf_an, prix_carbone_kero_saf, prix_saf_an, allowances_extra_an, prix_ap_allowances_an, prix_kero_an, prix_carbone_kero_an = calculs_with_saf(nbr_annee,
                                                                                                                                                        volume_carbu_an,
                                                                                                                                                        incorpo_saf,
                                                                                                                                                        allowance_free_2023,
                                                                                                                                                        quota_eu,
                                                                                                                                                        carbonprice,
                                                                                                                                                        price_saf,
                                                                                                                                                        price_kero,
                                                                                                                                                        allowance_SAF)


"""Graphique :"""

labels = ['Kérosène',
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
                 np.round((prix_carbone_kero_an + prix_kero_an)/1000000,2)])

if __name__ == '__main__':
    
    graphique(data, labels)
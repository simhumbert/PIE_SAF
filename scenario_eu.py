from hypothesis import *
from utils import *

"""## Scénario : Incorporation en ligne avec les mandats européens"""


"""1. Calculs"""

prix_kero_saf_an, prix_carbone_kero_saf, prix_saf_an, allowances_extra_an, prix_ap_allowances_an, prix_kero_an, prix_carbone_kero_an = calculs_with_saf(nbr_annee,
                                                                                                                                                        volume_carbu_an,
                                                                                                                                                        incorpo_saf_eu,
                                                                                                                                                        allowance_free_2023,
                                                                                                                                                        quota_eu,
                                                                                                                                                        carbonprice,
                                                                                                                                                        price_saf,
                                                                                                                                                        price_kero,
                                                                                                                                                        allowance_SAF)

"""2. Graphique"""

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
                  np.round((prix_carbone_kero_an + prix_kero_an)/1000000,2)])

graphique(data, labels)

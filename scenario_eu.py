from utils.hypothesis import *
from utils.utils import *

"""## Scénario : Incorporation en ligne avec les mandats européens"""


"""1. Calculs"""

C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0 = calculs_with_saf(nbr_annee, volume_carbu_an,incorpo_saf_eu, allowance_free_2023, quota_eu, carbonprice, price_saf, price_kero, allowance_SAF)

"""2. Graphique"""

labels =['Kérosène',
         'Coût carbone kérosène (après quotas gratuits)',
          'SAF',
          'Allowances',
          'Prix Final',
          'Scénario NO SAF']

data = np.array([np.round(C_MP_k/1000000,2),
                 np.round(C_CO2_k/1000000,2),
                 np.round(C_MP_SAF/1000000,2),
                 np.round(R_UE/1000000,2),
                 np.round((C_MP_k+C_CO2_k+C_MP_SAF+R_UE)/1000000,2),
                 np.round((C_MP_k0 + C_CO2_k0)/1000000,2)])


if __name__ == '__main__':
    
    graphique(data, labels)

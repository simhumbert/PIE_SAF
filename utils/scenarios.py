from utils.utils import *
from utils.data import *



"""## Scénario Skyalp : incorporations modifiables

1. Hypothèses 
"""
def get_data(scenario, P_SAF_selected):
    
    #### Code commun aux différents scénarios  ####
    
    # Période considérée
    debut = 2023
    fin = 2030

    # Incorporations
    incorpo_2023 = 0              # *100 %
    incorpo_2024 = 0.05           # *100 %
    incorpo_2025 = 0.10           # *100 %
    incorpo_2026 = 0.15           # *100 %
    incorpo_2027 = 0.20           # *100 %
    incorpo_2028 = 0.30           # *100 %
    incorpo_2029 = 0.40           # *100 %
    incorpo_2030 = 0.50           # *100 %

    # Objectifs incorporations saf EU
    incorpo_saf_eu = np.concatenate((np.linspace(obj_2023, obj_2025, 2025-debut+1)[:-1],
                                 np.linspace(obj_2025, obj_2030, fin-2025+1)))

    # Quotas carbone
    quota_eu = np.array([quota_2023, quota_2024, quota_2025, quota_2026, 0, 0, 0, 0])

    # Carbon price
    carbonprice = np.linspace(carbonprice_2023, carbonprice_2030, fin-debut+1)
    incorpo_saf = np.array([incorpo_2023, incorpo_2024, incorpo_2025, incorpo_2026, incorpo_2027, incorpo_2028, incorpo_2029, incorpo_2030])

    labels = ['Kérosène',
          ' Coût carbone kérosène (après quotas gratuits)',
          'SAF',
          'Allowances',
          'Prix Final',
          'Scénario NO SAF']
    
    #### Codes relatifs aux différents scénarios
    
    if scenario == 'lufthansa':
        # Emissions de CO2 en 2023
        CO2_2023 = 22.0 * 10**6        # tCO2/an

        # Hypothèses flotte A320
        nbr_old_start = 126
        nbr_new_start = 39
        replacement_nbr = 17
        em_reduction_rate = 0.15
        nbr_add_annual = 0

        # Part du marché dans l'UE
        market_eu = 0.43

        # Augmentation des emissions en tC02 / an
        CO2_supp = 0       # tCO2/an

        # Allowance gratuite en 2023 : émissions de CO2 2023
        allowance_free_2023 = CO2_2023 * market_eu

        # Tableau des émissions / an
        volume_carbu_an, CO2_emission = fleet_carbu(debut, fin, CO2_2023, nbr_old_start, nbr_new_start, replacement_nbr, em_reduction_rate, nbr_add_annual)

        # Tableau emission
        emission_euets_luft = np.array([round(market_eu * i,2) for i in CO2_emission])
        volume_euets_luft = np.array([round(market_eu*i,2) for i in volume_carbu_an])

        """Calculs :"""

        C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0 = calculs_with_saf(debut, fin, volume_euets_luft,incorpo_saf_eu, allowance_free_2023, quota_eu, carbonprice, P_SAF_selected, price_kero, allowance_SAF)

        data = np.array([np.round(C_MP_k/1000000,2),
                 np.round(C_CO2_k/1000000,2),
                 np.round(C_MP_SAF/1000000,2),
                 np.round(R_UE/1000000,2),
                 np.round((C_MP_k+C_CO2_k+C_MP_SAF+R_UE)/1000000,2),
                 np.round((C_MP_k0 + C_CO2_k0)/1000000,2)])


        to_return = {'graphique' : [data, labels, debut, fin],
                 'emissionscarbone' : [emission_euets_luft, incorpo_saf_eu, incorpo_saf],
                 'hypotheses' : [debut, fin, carbonprice, quota_eu, incorpo_saf_eu]}
    
    elif scenario == 'skyalp':

        # Emissions de CO2 en 2023
        CO2_2023 = 10000.0        # tCO2/an

        # Augmentation des emissions en tC02 / an
        CO2_supp = 10000.0        # tCO2/an

        # Allowance gratuite en 2023 : émissions de CO2 2023
        allowance_free_2023 = CO2_2023

        # Tableau des émissions / an
        nbr_annee = fin - debut +1
        CO2_em = np.linspace(CO2_2023, CO2_supp * nbr_annee, nbr_annee)

        volume_carbu_an = CO2_em * 1000000/(nrj_volum_kero * core_lca_kero)

        """Calculs :"""

        C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0 = calculs_with_saf(debut, fin, volume_carbu_an,incorpo_saf, allowance_free_2023, quota_eu, carbonprice, P_SAF_selected, price_kero, allowance_SAF)

        data = np.array([np.round(C_MP_k/1000000,2),
                 np.round(C_CO2_k/1000000,2),
                 np.round(C_MP_SAF/1000000,2),
                 np.round(R_UE/1000000,2),
                 np.round((C_MP_k+C_CO2_k+C_MP_SAF+R_UE)/1000000,2),
                 np.round((C_MP_k0 + C_CO2_k0)/1000000,2)])

        to_return = {'graphique' : [data, labels, debut, fin],
                 'emissionscarbone' : [CO2_em, incorpo_saf_eu, incorpo_saf],
                 'hypotheses' : [debut, fin, carbonprice, quota_eu, incorpo_saf]}
    
    elif scenario =='ryanair':
        # Emissions de CO2 en 2023
        CO2_2023 = 14.2*10**6       # tCO2/an

        # Hypothèses d'évolution de flotte
        B737_NG_0 = 213             # Nombre d'anciens avions dans la flotte en 2023
        B737_MAX_0 = 85             # Nombre de nouveaux avions dans la flotte en 2023
        replacement_nbr = 15        # Nombre d'anciens avions remplacés chaque année
        nbr_add_annual = 15         # Augmentation annuelle de la taille de la flotte
        em_reduction_rate = 0.2     # Taux de réduction des émissions des nouveaux avions

        # Part du marché dans l'UE
        market_eu = 0.9

        # Allowance gratuite en 2023 : émissions de CO2 2023
        allowance_free_2023 = CO2_2023*market_eu

        # Tableau des émissions / an et émissions de CO2 sans SAF
        volume_carbu_world, CO2_em_world = fleet_carbu(debut, fin, CO2_2023, B737_NG_0, B737_MAX_0, replacement_nbr, em_reduction_rate, nbr_add_annual)

        # Extraction des données pour le marché européen
        CO2_em = np.array([round(market_eu * i,2) for i in CO2_em_world])
        volume_carbu = np.array([round(market_eu * i,2) for i in volume_carbu_world])

        """Calculs :"""

        C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0 = calculs_with_saf(debut, fin, volume_carbu,incorpo_saf, allowance_free_2023, quota_eu, carbonprice, P_SAF_selected, price_kero, allowance_SAF)

        data = np.array([np.round(C_MP_k/1000000,2),
                 np.round(C_CO2_k/1000000,2),
                 np.round(C_MP_SAF/1000000,2),
                 np.round(R_UE/1000000,2),
                 np.round((C_MP_k+C_CO2_k+C_MP_SAF+R_UE)/1000000,2),
                 np.round((C_MP_k0 + C_CO2_k0)/1000000,2)])
        to_return = {'graphique' : [data, labels, debut, fin],
                 'emissionscarbone' : [CO2_em, incorpo_saf_eu, incorpo_saf],
                 'hypotheses' : [debut, fin, carbonprice, quota_eu, incorpo_saf]}
    return to_return

    
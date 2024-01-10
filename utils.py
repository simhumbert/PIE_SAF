from hypothesis import *


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

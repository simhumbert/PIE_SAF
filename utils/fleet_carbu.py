import numpy as np
from utils.data import *


def fleet_carbu(annee_start, annee_end,       # int : Années de début et fin de simulation (hypothèse)
                CO2_em_start,                 # float : Emissions de CO2 à l'année de départ (donnée)
                nbr_old_start,                # int : nombre d'anciens modèles au départ (donnée)
                nbr_new_start,                # int : nombre de nouveaux modèles au départ (donnée)
                replacement_nbr,              # int : nombre d'avions remplacés annuellement (hypothèse)
                em_reduction_rate,            # float : pourcentage de réduction d'émissions des nouveaux modèles (hypothèse)
                ):
    
    
    nbr_annee = annee_end - annee_start +1
    CO2_em = np.zeros(nbr_annee)
    CO2_em[0] = CO2_em_start
    nbr_old = nbr_old_start
    nbr_new = nbr_new_start
    CO2_em_old = CO2_em_start*nbr_old/(nbr_old+nbr_new*(1-em_reduction_rate))
    CO2_em_new = CO2_em_start*nbr_new*(1-em_reduction_rate)/(nbr_old+nbr_new*(1-em_reduction_rate))
    
    for i in range(1, nbr_annee):
        CO2_em_old = CO2_em_old - replacement_nbr*CO2_em_old/nbr_old
        CO2_em_new = CO2_em_new + replacement_nbr*CO2_em_new/nbr_new
        nbr_old = max(nbr_old-replacement_nbr, 0)
        nbr_new = nbr_new+replacement_nbr
        CO2_em[i] = CO2_em_old + CO2_em_new
    
    volume_carbu_an = CO2_em * 1000000/(nrj_volum_kero * core_lca_kero)
    
    return volume_carbu_an, CO2_em
    
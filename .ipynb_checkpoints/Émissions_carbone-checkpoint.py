from utils.utils import *
from scenario import incorpo_saf

#from scenario_nosaf import CO2_em
#from scenario_eu import incorpo_saf_eu
#from scenario import incorpo_saf

emissions_carbone_scénarios = []     # On réuni les émissions carbone des différents scénarios

# Scénario 1 : No SAF
emissions_carbone_scénarios.append(CO2_em)

# Scénario 2 : réglementation européenne
# Quotas carbone
emissions_carbone_scénarios.append(([1] * len(incorpo_saf_eu) - incorpo_saf_eu) * CO2_em)

# Scénario 3 : custom
# Incorpo SAF
emissions_carbone_scénarios.append((np.array([1] * len(incorpo_saf)) - np.array(incorpo_saf)) * np.array(CO2_em))

graphique_emissionscarbone(emissions_carbone_scénarios)
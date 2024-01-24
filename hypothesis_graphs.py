from utils.hypothesis import *
import matplotlib.pyplot as plt

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
plt.tight_layout()
plt.show()
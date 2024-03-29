from utils.data import *
import matplotlib.pyplot as plt
import os


def calculs_with_saf(beg,             # int : Année de départ
                     end,             # int : Année de fin
                     V,               # array : Volume de carburant / an (hypothèse)
                     I,               # array : taux d'incorporation / an (hypothèse)
                     A,               # float : allowance d'émissions gratuites en 2023 (hypothèse)
                     Q,               # array : quotat carbones pour l'Europe (hypothèse)
                     P_CO2,           # array : prix de la tonne carbone chaque année (hypothèse)
                     P_SAF,           # float : prix du SAF au litre (hypothèse)
                     P_k,             # float : prix du kérosène au litre (hypothèse)
                     R):              # float : allowance gratuite de réduction du surcoût lié au SAF (hypothèse)               
    years = end - beg +1
    # Cas sans SAF : 
    C_MP_k0 = V * P_k
    C_CO2_k0 = (alpha*V - A*Q) * P_CO2

    # Cas avec SAF : 
    V_SAF = np.zeros(years)
    V_k = np.zeros(years)

    for y in range(len(V)):
        V_SAF[y]    = V[y]*I[y]
        V_k[y]  = V[y]*(1-I[y])

    C_CO2_k = (alpha*V_k - A*Q) * P_CO2
    C_MP_SAF = V_SAF * P_SAF
    C_MP_k = V_k * P_k
    R_UE = -R *(C_MP_k+ C_MP_SAF - C_MP_k0 )

    return C_MP_k, C_CO2_k, C_MP_SAF, R_UE, C_MP_k0, C_CO2_k0



def graphique(data, labels, debut, fin, taux_incorpo, filename=None, dossier = None):
    
    
    years = np.arange(debut, fin+1)

    # parameters of the figure
    fig = plt.figure(figsize=(18, 8))
    width = 0.1

    colors =['#b57e36',
             '#8a2f2f',
             '#4fa842',
             '#f7f265',
             '#374c63',
             '#7F8C8D']

    bottoms = np.array([np.zeros(len(data[0])),
                        data[0,:],
                        data[0,:]+data[1,:],
                        data[0,:]+data[1,:]+data[2,:],
                        np.zeros(len(data[0,:])),
                        np.zeros(len(data[0,:]))])

    for i in range(0,len(data[:,0])-2):
        bar = plt.bar(years+i*width, data[i,:], label=labels[i], width=width-0.05, bottom=bottoms[i,:], align='center', color=colors[i])
        #plt.bar_label(bar, label_type='center')
    
    bar = plt.bar(years+(len(data[:,0])-1)*width, data[-2,:], label=labels[-2], width=width+0.05, bottom=bottoms[-2,:], align='center', color=colors[-2])
    #plt.bar_label(bar, padding = 0.5)
    # Affichage du scénario de référence
    bar = plt.bar(years+(len(data[:,0])+1)*width, data[-1,:], label=labels[-1], width=width+0.05, bottom=bottoms[-1,:], align='center', color=colors[-1])
    plt.bar_label(bar, label_type ='center')
    
    diff = data[-1,:] - data[-2,:]
    for i, d in enumerate(diff):
        if d > 0:
            color = 'red'
            plt.text(years[i] + (len(data[:,0])+1)*width, data[-1,i] + 0.1, f"+{d:.2f}", ha='center', color=color, fontsize = 12)
        else:
            color = 'blue'
            plt.text(years[i] + (len(data[:,0])+1)*width, data[-1,i] + 0.1, f"{d:.2f}", ha='center', color=color, fontsize = 10)


    # Personnaliser le graphique
    #plt.xlabel('Years', fontsize = 14, labelpad = 30)
    plt.ylabel('Price (M$)', fontsize = 14)
    plt.tick_params(axis='both', which='major', labelsize=12) 
    
    
    
    for i in range(len(taux_incorpo)):
        plt.text( 2023+i + 1.5*width, -3, f" SAF : {round(taux_incorpo[i]*100,)}%", ha='center', color = 'grey')


    plt.xticks(years + 1.5*width, years)
    
    # Définir le fond du graphique comme transparent
    plt.gca().set_facecolor('none')
    plt.grid(axis='y', color='lightgrey')
    plt.legend(loc='upper left', framealpha=0.75)
    # Enregistrer le graphique si un nom de fichier est spécifié
    if filename and dossier:
        chemin_fichier = os.path.join(dossier, filename)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)
    
    
    # Afficher le graphique
    plt.show()
    
    
    

def graphique_emissionscarbone(CO2_em_NoSaf, incorpo_saf_EU, incorpo_saf_CUSTOM, filename = None, dossier=None):
    # Fonction pour tracer les emissions carbone des 3 différents scénarios
    emissions_carbone = []
    emissions_carbone.append(CO2_em_NoSaf)
    emissions_carbone.append(([1] * len(incorpo_saf_EU) - incorpo_saf_EU) * CO2_em_NoSaf)
    emissions_carbone.append(([1] * len(incorpo_saf_CUSTOM) - incorpo_saf_CUSTOM) * CO2_em_NoSaf)

    annees = list(range(2023, 2031))  # Créer une liste d'années de 2023 à 2030
    figc = plt.figure(figsize=(15, 8))

    plt.plot(annees, emissions_carbone[0], marker='s', label='Scenario 1 : No SAF')
    plt.plot(annees, emissions_carbone[1], marker='o', label='Scenario 2 : Incorporation according european mandates')
    plt.plot(annees, emissions_carbone[2], marker='^', label='Scenario 3 : Incorporation from custom')

    #plt.title('Carbon emissions from 2023 to 2030', fontsize = 16, pad = 30)
    #plt.xlabel('Years', fontsize = 14)
    plt.ylabel('Carbon emissions (tCO2)', fontsize = 14, labelpad = 30)
    plt.legend()  # Afficher la légende
    plt.gca().set_facecolor('none')
    plt.legend(framealpha=0.75)
    # Enregistrer le graphique si un nom de fichier est spécifié
    plt.grid(True)
    if filename and dossier:
        chemin_fichier = os.path.join(dossier, filename)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)


    # plt.tight_layout()
    plt.show()
    


def fleet_carbu(annee_start, annee_end,       # int : Années de début et fin de simulation (hypothèse)
                CO2_em_start,                 # float : Emissions de CO2 à l'année de départ (donnée)
                nbr_old_start,                # int : nombre d'anciens modèles au départ (donnée)
                nbr_new_start,                # int : nombre de nouveaux modèles au départ (donnée)
                replacement_nbr,              # int : nombre d'avions remplacés annuellement (hypothèse)
                em_reduction_rate,            # float : pourcentage de réduction d'émissions des nouveaux modèles (hypothèse)
                nbr_add_annual                # int : augmentation annuelle du nombre total d'appareils (hypothèse)
                ):
    
    
    nbr_annee = annee_end - annee_start +1
    CO2_em = np.zeros(nbr_annee)
    CO2_em[0] = CO2_em_start
    nbr_old = nbr_old_start
    nbr_new = nbr_new_start
    em_factor_old = (CO2_em_start*nbr_old/(nbr_old+nbr_new*(1-em_reduction_rate)))/nbr_old
    em_factor_new = (CO2_em_start*nbr_new*(1-em_reduction_rate)/(nbr_old+nbr_new*(1-em_reduction_rate)))/nbr_new
    
    for i in range(1, nbr_annee):
        nbr_old = max(nbr_old-replacement_nbr, 0)
        nbr_new = nbr_new+replacement_nbr+nbr_add_annual
        CO2_em_old = nbr_old*em_factor_old
        CO2_em_new = nbr_new*em_factor_new
        
        if nbr_old==0:
            replacement_nbr = 0
        
        CO2_em[i] = CO2_em_old + CO2_em_new
    
    volume_carbu_an = CO2_em * 1000000/(nrj_volum_kero * core_lca_kero)
    
    return volume_carbu_an, CO2_em



def graphique_hypotheses(debut, fin, carbonprice, quota_eu, incorpo_saf, filename_price = None, filename_quota = None, filename_incorpo = None, dossier = None):
  # Prix du carbone
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(debut, fin + 1), carbonprice, label='Carbon Price ($/tCO2eq.)', marker='o')
    #ax.set_xlabel('Années')
    ax.set_ylabel('Price ($/tCO2eq.)', fontsize = 14, labelpad = 30)
    #ax.set_title('Carbon Price Evolution')
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    if filename_price and dossier:
        chemin_fichier = os.path.join(dossier, filename_price)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)


    # Quota carbone EU
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(debut, fin + 1), quota_eu*100, label='Carbon Quota of EU)', marker='s')
    #ax.set_xlabel('Année')
    ax.set_ylabel('Proportion of Carbon Quota \n covered by free allowances (%)', labelpad = 30)
    #ax.set_title('Carbon Quota evolution of EU')
    ax.legend()
    plt.grid(True)
    if filename_quota and dossier:
        chemin_fichier = os.path.join(dossier, filename_quota)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)
    
    plt.show()

    # Incorporation des SAF en Eu
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(debut, fin + 1), incorpo_saf*100, label='SAF Incorporation (%)', marker='^')
    #ax.set_xlabel('Année')
    ax.set_ylabel('SAF Incorporation (%)', fontsize = 14, labelpad = 30)
    #ax.set_title('Evolution of SAF incorporation')
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    if filename_incorpo and dossier:
        chemin_fichier = os.path.join(dossier, filename_incorpo)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)
    
    plt.show()
    
def graphique_carbonprice(beg, end, 
                          P_CO2,      # array : prix de la tonne carbone chaque année (hypothèse)
                          P_SAF,      # float : prix du SAF au litre (hypothèse)
                          P_k,        # float : prix du kérosène au litre (hypothèse)
                          R,           # float : allowance gratuite de réduction du surcoût lié au SAF (hypothèse) 
                          filename = None,dossier =None):
  
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(range(beg, end + 1), P_CO2, label='Price CO2 according hypothesis', marker='^')
    ax.plot(range(beg, end + 1), (end-beg+1)*[(P_SAF-P_k)*(1-R)/alpha], label='Limit of Price CO2', marker='o')
    #ax.set_xlabel('Année')
    ax.set_ylabel('Price ($)', fontsize = 14, labelpad = 20 )
    #ax.set_title('Évolution du prix de la tonne de carbone')
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    if filename and dossier:
        chemin_fichier = os.path.join(dossier, filename)
        plt.savefig(chemin_fichier)
        plt.savefig(chemin_fichier, bbox_inches='tight', transparent=True)
    
    plt.show()
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import os.path
import glob
from pylab import *
from math import *
import numpy as na
import sys

#Plus theta_s est faible, plus les courbes de reflectance sont proches et independantes de l'epaisseur optique => plus il est difficile d'estimer l'AOT dans MAJA avec une bonne precision.

#####################################################################
#
#    Classe liste pour la lecture des lignes des fichiers textes
#
#####################################################################
class liste :
    def __init__(self,lignes):
	self.val = {}
	self.dim = {}
	self.ind = {}
	self.liste_dims = []
	for il, lig in enumerate(lignes) :
	    #On vire les tabs et les sauts de lignes
	    datalist = lig.strip('\t').strip('\n').split(' ')
	    #On vire les elements vides
	    datalist = filter(lambda x: x!='', datalist)
	    #Si c'est une ligne vide, on passe a la suivante
	    if len(datalist)== 0 :
		    continue
	    #1er element correspond au nom de la variable (rtoa, tau, etc.)
	    type_donnee = datalist[0]
	    #Puis on lit les valeurs
	    values = [float(x) for x in datalist[1:]]
	    self.val[type_donnee] = np.array(values, 'Float32')
	    #L'indice dans la LUT
	    self.ind[type_donnee] = il #Car pour le moment on a rsurf en plus
	    self.dim[type_donnee] = len(self.val[type_donnee])
	    self.liste_dims.append(self.dim[type_donnee])		

########################
#
#    Prog principal
#
########################
if len(sys.argv) < 5 or len(sys.argv) > 6:
    print 'Usage :'
    print '      '+ str(sys.argv[0])+ ' satellite aerosolModel proportion_AOT_grossier bande'
    print 'ou'
    print '      '+ str(sys.argv[0])+ ' satellite aerosolModel concentrationVolumiqueCoarse concentrationVolumiqueFine bande'
    print 'Exemple :'
    print '      '+ str(sys.argv[0])+ ' LANDSAT8 zerodeux 0 0'
    print 'ou'
    print '      '+ str(sys.argv[0])+ ' S2B SeaSalt_RH30_CAMS 3.0 70.0 0'    
    sys.exit(-1)
    
#********************
#     PARAMETRES
#********************
if len(sys.argv) == 5:
    bimodalOption = 2 #Si bimodal defini par proportion_AOT_coarse
else:
    bimodalOption = 1 #Si bimodal defini par concentrations volumiques

sat     = str(sys.argv[1])
aerosol = str(sys.argv[2])

if bimodalOption == 2:
    proportion_AOT_c = float(sys.argv[3])
    num_bd           = int(sys.argv[4])
    print 'Proportion AOT grossier :', proportion_AOT_c
else:
    CVcoarse = float(sys.argv[3])
    CVfine   = float(sys.argv[4])
    num_bd   = int(sys.argv[5])
    print 'CVcoarse :',CVcoarse,', CVfine :',CVfine

#**************************************
#     Repertoire contenant les LUT
#**************************************
if sat=='S2A' :
    rep = '/mnt/data/home/rouquieb/DONNEES/LUTS/CAMScycle46R1/S2A/'
elif sat=='S2B' :
    rep = '/mnt/data/home/rouquieb/DONNEES/LUTS/CAMScycle46R1/S2B/'
elif sat=='VENUS':
    rep = '/mnt/data/home/colinj/DONNEES/LUTS/TEST_SANS_ABSORPTION/VENUS/'
elif sat=='LANDSAT8' :
    rep = '/mnt/data/home/rouquieb/DONNEES/LUTS/CAMScycle46R1/LANDSAT8/'
print '\nREPERTOIRE LUTS:',rep

#Choix du fichier de parametres
if sat=='FORMOSAT' :
    import param_luts_formosat as param_luts
elif sat=='S2' :
    import param_luts_S2 as param_luts
elif sat=='S2A' :
    path_out = '/mnt/data/home/rouquieb/LUT/PLOT_LUT/CAMScycle46R1/S2A/'
    import param_luts_S2A as param_luts
elif sat=='S2B' :
    path_out = '/mnt/data/home/rouquieb/LUT/PLOT_LUT/CAMScycle46R1/S2B/'
    import param_luts_S2B as param_luts
elif sat=='VENUS':
    path_out = '/mnt/data/home/colinj/DONNEES/LUTS/TEST_SANS_ABSORPTION/plots/'
    import param_luts_Venus as param_luts
elif sat=='LANDSAT5' :
    import param_luts_LANDSAT5 as param_luts
elif sat=='LANDSAT7' :
    import param_luts_LANDSAT7 as param_luts
elif sat=='LANDSAT8' :
    path_out = '/mnt/data/home/rouquieb/LUT/PLOT_LUT/CAMScycle46R1/LANDSAT8/'
    import param_luts_LANDSAT8 as param_luts
elif sat=='SPOT4H1' :
    import param_luts_SPOT4H1 as param_luts
elif (sat=='SPOT4TAKE5' or sat=='TAKE5') :
    import param_luts_SPOT4_TAKE5 as param_luts
elif sat=='SPOT5TAKE5' :
    import param_luts_SPOT5_TAKE5 as param_luts
elif sat=='SPOT4H2' :
    import param_luts_SPOT4H2 as param_luts
elif sat=='TEST' :
    import param_luts_SPOT4H2 as param_luts
elif sat=='DMC' :
    import param_luts_DMC as param_luts
elif sat=='RAPIDEYE' :
    import param_luts_RAPIDEYE as param_luts
else :
    print sat +" : satellite inconnu"

print '\nPATH OUT:',path_out

#Lecture du fichier parametres
bandes, bande_ref, tauRay, liste_theta_v, rmodal_f, log10var_f, rmodal_c, log10var_c, mi_f, mi_c, mr_f, mr_c = param_luts.param(aerosol)

liste_theta_s   = na.linspace(0,75,11)
ep_opt          = na.linspace(0,1.5,25)
liste_altitude  = na.arange(0,3100,1000)
liste_delta_phi = na.linspace(0,180,7)

#Nom de la LUT (et du plot de sortie)
if 'zerodeux' not in aerosol:
    chaine = 'V51_%s_%s_bande_%d'%(sat,aerosol,bandes[num_bd])
else:
    chaine='V51_%s_%s_prop_%4.2f_bande_%d'%(sat,aerosol,proportion_AOT_c,bandes[num_bd])

print 'chaine:',chaine
print 'r0 fine = ',rmodal_f
print 'r0 coarse = ',rmodal_c

#LUT inverse
#***********
#Lecture du fichier texte
f_luttxt = file(rep+'/lut_inv_'+chaine+'.txt','r') #fichier .dat
lignes = f_luttxt.readlines()
f_luttxt.close()

liste_inv = liste(lignes)

#Lecture de la LUT
nom_lut_inv = rep+'/lut_inv_'+chaine
tmp_inv = np.fromfile(nom_lut_inv,'Float32')
LUT_inv = tmp_inv.reshape(liste_inv.liste_dims)

#LUT directe
#***********
#Lecture du fichier texte
f_luttxt = file(rep+'/refl_'+chaine+'.txt','r') #fichier .dat
lignes = f_luttxt.readlines()
f_luttxt.close()

liste_dir = liste(lignes)

#Lecture de la LUT
nom_lut_dir = rep+'/refl_'+chaine
tmp_dir = np.fromfile(nom_lut_dir,'Float32')
LUT_dir = tmp_dir.reshape(liste_dir.liste_dims)

#**************
#     PLOT
#**************
#Dimensions des LUT : [rtoa(ou rsurf) x ep_opt x alt x dphi x theta_v x theta_s]

#param_luts_SPOT5TAKE5:
# - Theta_v : [  0.   7.  14.  21.  28.  35.]
# - Theta_s : [  0.    7.5  15.   22.5  30.   37.5  45.   52.5  60.   67.5  75. ]
# - Epaisseur optique : [ 0.      0.0625  0.125   0.1875  0.25    0.3125  0.375   0.4375  0.5
#  0.5625  0.625   0.6875  0.75    0.8125  0.875   0.9375  1.      1.0625
#  1.125   1.1875  1.25    1.3125  1.375   1.4375  1.5   ]

#param_luts_SPOT4TAKE5:
# - Theta_v : [  0.   7.  14.  21.  28.  35.]
# - Theta_s : idem
# - Epaisseur optique : idem

#param_luts_S2A et S2B:
# - Theta_v : [  0.  7.  13.  20.]
# - Theta_s : idem
# - Epaisseur optique : idem

#param_luts_LANDSAT8:
# - Theta_v : [  0.  7.  13.]
# - Theta_s : idem
# - Epaisseur optique : idem

#Parametrage de theta_s, theta_v et ep_opt a afficher
#****************************************************

# == Theta_v
if sat =='S2A' or sat=='LANDSAT8' or sat=='S2B':
    tv_to_plot = 13.
elif sat=='SPOT4TAKE5' or sat=='SPOT5TAKE5' or sat=='VENUS':
    tv_to_plot = 14.
else :
    print sat +" : satellite inconnu"

i_th_v, = na.where(liste_theta_v == tv_to_plot)
th_v = liste_theta_v[i_th_v]
th_v_str = str(th_v[0])
print '\ntheta_v :',th_v_str

# == Theta_s
ts_to_plot = 30.
i_th_s, = na.where(liste_theta_s == ts_to_plot)
th_s = liste_theta_s[i_th_s]
th_s_str = str(th_s[0])
print 'theta_s :',th_s_str

# == Epaisseurs optiques
tau1_to_plot = 0.0
tau2_to_plot = 0.25
tau3_to_plot = 0.5
itau1, = na.where(ep_opt == tau1_to_plot)
itau2, = na.where(ep_opt == tau2_to_plot)
itau3, = na.where(ep_opt == tau3_to_plot)
tau1 = ep_opt[itau1]
tau2 = ep_opt[itau2]
tau3 = ep_opt[itau3]
tau1_str = r'$\tau=$' + str(tau1[0])
tau2_str = r'$\tau=$' + str(tau2[0])
tau3_str = r'$\tau=$' + str(tau3[0])
print tau1_str
print tau2_str
print tau3_str

# == Range
min_rsurf = min(liste_dir.val['rsurf'])
#max_rsurf = max(liste_dir.val['rsurf'])
max_rsurf = 0.6
print 'rsurf min et max :',min_rsurf,max_rsurf

# == Longueur d'onde
bande = bandes[num_bd]
bande_str = str(bande)
print 'lambda :',bande

# == Altitude
i_alt = 0
alt = liste_altitude[i_alt]
alt_str = str(alt)
print 'altitude :',alt

# == dphi
i_dphi = 4
dphi = liste_delta_phi[i_dphi]
dphi_str = str(dphi)
print 'dphi :',dphi

# == Indice de réfraction
nr = mr_f[num_bd]
nr_str = str(nr)
ni = mi_f[num_bd]
ni_str = str(ni)
print '\nn = ',nr,ni,'i'

#********************
#Calcul du range de la reflectance critique, i.e. les 2 valeurs de rsurf au mileu desquelles rho_TOA ne depend plus de tau
#Init chaine
chaine_rcrit = ''
#Calcule rcrit ?
calc_rcrit = 1
if calc_rcrit == 1:
    rtoa_tauA = LUT_dir[:,12,i_alt,i_dphi,i_th_v,i_th_s] #rho_TOA pour tauA = 0.75
    rtoa_tauB = LUT_dir[:,4,i_alt,i_dphi,i_th_v,i_th_s]  #rho_TOA pour tauB = 0.25

    diff = rtoa_tauA - rtoa_tauB
    diff.tolist()
    #Recherche du 1er indice ou rho_TOA pour tauA est inferieure à rho_TOA pour tauB (i.e. ou la difference devient negative)
    indice = -1
    for i,current_diff in enumerate(diff):
      if indice != -1:
        break #Si l'indice est trouve on arrete la boucle
      if current_diff < 0:
        indice = i

    if indice > 0:
      rcrit_low  = liste_dir.val['rsurf'][indice-1] #Dernier rsurf ou diff > 0
      rcrit_high = liste_dir.val['rsurf'][indice]   #1er rsurf ou diff < 0
      chaine_rcrit = r', $\rho_{crit} \in [%4.2f,%4.2f]$'%(rcrit_low,rcrit_high)
      print 'rcrit_low :',rcrit_low
      print 'rcrit_high :',rcrit_high
    else:
      chaine_rcrit = r', $\rho_{crit} \notin [%4.2f,%4.2f]$'%(min_rsurf,max_rsurf)
#********************

figure(0)
titre = 'alt=' + alt_str + 'm, ' + r'$d\phi=$' + dphi_str + ', ' + r'$\theta_{v}=$' + th_v_str + ', ' + r'$\theta_{s}=$' + th_s_str + ', ' + 'n=' + nr_str + ni_str + 'i' + chaine_rcrit
title(titre)
nom_modele = aerosol
suptitle(nom_modele,fontsize=12, fontweight='bold')

#Plot LUT directe : plot rtoa en fonction de rsurf pour 3 epaisseurs optiques differentes
plot(liste_dir.val['rsurf'],LUT_dir[:,itau1,i_alt,i_dphi,i_th_v,i_th_s],label=tau1_str)
plot(liste_dir.val['rsurf'],LUT_dir[:,itau2,i_alt,i_dphi,i_th_v,i_th_s],label=tau2_str)
plot(liste_dir.val['rsurf'],LUT_dir[:,itau3,i_alt,i_dphi,i_th_v,i_th_s],label=tau3_str)

legend(loc='upper left')
ylim([min_rsurf,max_rsurf])
xlim([min_rsurf,max_rsurf])
grid()
xlabel(r'$\rho_{surface}$')
ylabel(r'$\rho_{TOA} $')

#Plot LUT inverse
#plot(LUT_inv[:,0,0,4,4,10],liste_inv.val['rtoa'],LUT_inv[:,10,0,4,4,10],liste_inv.val['rtoa'],LUT_inv[:,20,0,4,4,10],liste_inv.val['rtoa'])

#Save plot in a file
savefig(path_out+chaine+'.png')


#====================================================================
#
#     Plot la reflectance TOA en fonction de l'epaisseur optique
#
#====================================================================
rTOA_tau = False
if rTOA_tau == True:
    #rsurf : [ 0.       0.08125  0.1625   0.24375  0.325    0.40625  0.4875   0.56875
    #  0.65     0.73125  0.8125   0.89375  0.975    1.05625  1.1375   1.21875
    #  1.3    ]
    figure(10)
    #Reflectance de surface
    #rsurf_to_plot = 0.08125
    #i_rsurf, = na.where(liste_dir.val['rsurf'] == rsurf_to_plot)
    i_rsurf = 1
    rsurf = liste_dir.val['rsurf'][i_rsurf]
    #rsurf_str = r'$\rho_{surf} = $' + str(rsurf[0])
    rsurf_str = r'$\rho_{surf} = $' + str(rsurf)

    #Reshape la LUT a afficher pour qu'elle ait les memes dimensions que le tableau des epaisseurs optiques => necessaire a la fonction plot
    LUT = na.reshape(LUT_dir[i_rsurf,:,i_alt,i_dphi,i_th_v,i_th_s],ep_opt.size)

    titre_rtoa_tau = 'alt=' + alt_str + 'm, ' + r'$d\phi=$' + dphi_str + ', ' + r'$\theta_{v}=$' + th_v_str + ', ' + r'$\theta_{s}=$' + th_s_str + ', ' + 'n=' + nr_str + ni_str + 'i'
    title(titre_rtoa_tau)
    suptitle(nom_modele,fontsize=12, fontweight='bold')

    #Plot
    plot(ep_opt,LUT,label=rsurf_str)

    min_rTOA = min(LUT)
    max_rTOA = max(LUT)
    legend(loc='upper center')
    min_tau = min(ep_opt)
    max_tau = max(ep_opt)
    xlim([min_tau,max_tau])
    ylim([min_rTOA,max_rTOA])
    grid()
    ylabel(r'$\rho_{TOA} $')
    xlabel(r'$\tau$')

    chaine_rTOA_tau = chaine + '_rTOA_tau'
    savefig(path_out+'RTOA_TAU/'+chaine_rTOA_tau+'.png')

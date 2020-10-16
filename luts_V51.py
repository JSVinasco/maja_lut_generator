#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import os.path
import glob
from math import *
import numpy as na
import sys
from lib_SOS_V51 import *
    
#====================================================================
#     Calcul de pression atmospherique en fonction de l'altitude
#====================================================================
def PdeZ(Z) :
    """ 
    Calcul de pression atmospherique en fonction de l'altitude en metres
    """
    p = 1013.25 * pow( 1 - 0.0065 * Z / 288.15 , 5.31 )
    return(p)

#=============================
#     Programme principal
#=============================
if len(sys.argv) < 5 or len(sys.argv) > 6:
    print 'Usage :'
    print '      '+ str(sys.argv[0])+ ' satellite aerosolModel proportionAOTgrossier bande'
    print 'ou'
    print '      '+ str(sys.argv[0])+ ' satellite aerosolModel concentrationVolumiqueCoarse concentrationVolumiqueFine bande'
    print 'Exemple :'
    print '      '+ str(sys.argv[0])+ ' LANDSAT8 zerodeux 0 0'
    print 'ou'
    print '      '+ str(sys.argv[0])+ ' S2B SeaSalt_RH30_CAMS 3.0 70.0 0'    
    sys.exit(-1)

#============
# Parametres
#============
sat     = str(sys.argv[1])
aerosol = str(sys.argv[2])
print '\nSatellite :',sat
print 'Aerosol model :',aerosol

if len(sys.argv) == 5:
    bimodalOption = 2 #Si bimodal defini par proportionAOTcoarse
else:
    bimodalOption = 1 #Si bimodal defini par concentrations volumiques

if bimodalOption == 2:
    proportion_AOT_c = float(sys.argv[3])
    num_bd           = int(sys.argv[4])
    print 'Proportion AOT grossier :', proportion_AOT_c
else:
    CVcoarse = float(sys.argv[3])
    CVfine   = float(sys.argv[4])
    num_bd   = int(sys.argv[5])
    print 'CVcoarse :',CVcoarse,', CVfine :',CVfine
print 'Bande :', num_bd

#Fichier de parametres et chemin de sortie selon capteur
output_rootdir = '/home/colinj/code/luts_init/OUTPUTS/' # TODO: As parameter in next v
path_out = output_rootdir + sat + '/'

if sat == 'FORMOSAT':
    import param_luts_formosat as param_luts
elif sat == 'S2A':
    #path_out = None
    import param_luts_S2A as param_luts
elif sat == 'S2B':
    #path_out = None
    import param_luts_S2B as param_luts
elif sat == 'VENUS':
    #path_out = '/home/colinj/code/luts_init/OUTPUTS/'
    import resources.param_luts_Venus as param_luts
elif sat == 'LANDSAT5':
    #path_out = None
    import param_luts_LANDSAT5 as param_luts
elif sat == 'LANDSAT7':
    #path_out = None
    import param_luts_LANDSAT7 as param_luts
elif sat == 'LANDSAT8':
    #path_out = None
    import param_luts_LANDSAT8 as param_luts
elif sat == 'SPOT4H1':
    import param_luts_SPOT4H1 as param_luts
elif sat == 'SPOT4TAKE5':
    import param_luts_SPOT4_TAKE5 as param_luts
elif sat == 'SPOT5TAKE5':
    import param_luts_SPOT5_TAKE5 as param_luts
elif sat == 'SPOT4H2':
    import param_luts_SPOT4H2 as param_luts
elif sat == 'TEST':
    import param_luts_SPOT4H2 as param_luts
elif sat == 'DMC':
    import param_luts_DMC as param_luts
elif sat == 'RAPIDEYE':
    import param_luts_RAPIDEYE as param_luts
else :
    print sat +" : satellite inconnu"

print '\nPATH OUT:',path_out

#Lecture fichier parametes
bandes, bande_ref, tauRay, liste_theta_v, rmodal_f, log10var_f, rmodal_c, log10var_c, mi_f, mi_c, mr_f, mr_c = param_luts.param(aerosol)

nb_mu   = 40 #Nombre d'angles de Gauss dans les OS
nb_phi  = 7
pas_phi = 180/(nb_phi-1)

liste_theta_s   = na.linspace(0,75,11)
liste_delta_phi = na.linspace(0,180,7)
liste_altitude  = na.arange(0,3100,1000)
ep_opt          = na.linspace(0,1.5,25)
ep_opt          = na.append(ep_opt,[2.0,3.0])
liste_rsurf     = na.linspace(0,1.3,17)

print 'Bandes               :', bandes
print 'Bande ref            :', bande_ref
print 'Rayleigh             :', tauRay
print 'Theta_v              :', liste_theta_v
print 'rmodal_f             :', rmodal_f
print 'log10var_f           :', log10var_f
print 'rmodal_c             :', rmodal_c
print 'log10var_c           :', log10var_c
print 'mi_f                 :', mi_f
print 'mi_c                 :', mi_c
print 'mr_f                 :', mr_f
print 'mr_c                 :', mr_c
print 'Theta_s              :', liste_theta_s
print 'Delta phi            :', liste_delta_phi
print 'Altitude             :', liste_altitude
print 'Epaisseur optique    :', ep_opt
print 'Reflectances surface :', liste_rsurf, '\n'

P0 = 1013.25

#Echantillonnage pour la LUT inverse
liste_rtoa = na.arange(-0.2,1.2,0.07)

#==========================================
# Repertoires et variables d'environnement
#==========================================
SOS_RACINE = os.getenv('SOS_RACINE')
#maison     = os.getenv('HOME')

if SOS_RACINE is None :
    #SOS_RACINE = maison+'/code/luts_init/SOS_V51'
    #os.environ['RACINE'] = SOS_RACINE
    print 'ERROR: please specify SOS_RACINE: eg. export SOS_RACINE="/usr/local/SOS/'
    sys.exit(1)

#os.environ['SOS_RACINE'] = SOS_RACINE

#Nom fichiers de sortie
if 'zerodeux' not in aerosol:
    chaine = 'V51_%s_%s_bande_%d'%(sat,aerosol,bandes[num_bd])
else:
    chaine = 'V51_%s_%s_prop_%4.2f_bande_%d'%(sat,aerosol,proportion_AOT_c,bandes[num_bd])

#Creation des repertoires
SOS_RESULT = '/home/colinj/code/luts_init/OUTPUTS/SOS_RESULT/'+chaine

if not (os.path.exists(SOS_RESULT)):
    os.mkdir(SOS_RESULT)
    os.mkdir(SOS_RESULT+'/TRACE')
    os.mkdir(SOS_RESULT+'/MIE_V51')
    os.mkdir(SOS_RESULT+'/SURFACE')
    os.mkdir(SOS_RESULT+'/SOS')
   
SOS_RACINE_MU               = SOS_RACINE+'/fic'
os.environ['SOS_RESULT']    = SOS_RESULT
os.environ['SOS_RACINE_MU'] = SOS_RACINE_MU

if not (os.path.exists(path_out)): #JC2019
    try:
        os.makedirs(path_out)
    except:
        pass

#Fichier des angles de l'utilisateur
fic_angles = SOS_RESULT+"/SOS/fic_angles_"+chaine+".txt"
f = file(fic_angles,"w")
for tv in liste_theta_v:
    f.write("%f \n"%tv)
f.close()

(fic_res_angles,fic_res_angles_sos) = sos_angles(liste_theta_s[0],nb_mu,fic_angles)

#===================
# Pour chaque table
#===================
rho_toa     = na.zeros([len(liste_rsurf),len(ep_opt),len(liste_altitude),len(liste_delta_phi),len(liste_theta_v),len(liste_theta_s)],'Float32')
rho_surf    = na.zeros([len(liste_rtoa) ,len(ep_opt),len(liste_altitude),len(liste_delta_phi),len(liste_theta_v),len(liste_theta_s)],'Float32')
rho_surf_CS = na.zeros([ len(liste_theta_s),len(liste_theta_v),len(liste_delta_phi),len(liste_altitude),len(ep_opt),len(liste_rtoa)],'Float32')

albedo = na.zeros([len(liste_altitude),len(ep_opt)],'Float32')
Tdif   = na.zeros([len(liste_theta_s),len(liste_altitude),len(ep_opt)],'Float32')
Tdir   = na.zeros([len(liste_theta_s),len(liste_altitude),len(ep_opt)],'Float32')

nom_lut_albedo = 'albedo_'+chaine
nom_lut_Tdif   = 'Tdif_'+chaine
nom_lut_Tdir   = 'Tdir_'+chaine

#=================================================================
# Calcul du rapport d'extinction pour l'epaisseur optique aerosol
#=================================================================
tau = 0.1

#Simulation pour la bande de reference
if bimodalOption == 2:
    (ficOSup,ficAERgranu,Tdes_dir,Tdes_dif) = lance_simu_OS(fic_res_angles,fic_res_angles_sos,tauRay[bande_ref],tau,bandes[bande_ref],tau,bandes[bande_ref],proportion_AOT_c,\
                                                    mr_f[bande_ref],mi_f[bande_ref],mr_f[bande_ref],mi_f[bande_ref],rmodal_f,log10var_f,\
                                                    mr_c[bande_ref],mi_c[bande_ref],mr_c[bande_ref],mi_c[bande_ref],rmodal_c,log10var_c,\
                                                    20.0,0.,0.1)
else: #Si on utilise les Concentrations Volumiques
    (ficOSup,ficAERgranu,Tdes_dir,Tdes_dif) = lance_simu_OS_CV(fic_res_angles,fic_res_angles_sos,tauRay[bande_ref],tau,bandes[bande_ref],tau,bandes[bande_ref],CVcoarse,CVfine,\
                                                    mr_f[bande_ref],mi_f[bande_ref],mr_f[bande_ref],mi_f[bande_ref],rmodal_f,log10var_f,\
                                                    mr_c[bande_ref],mi_c[bande_ref],mr_c[bande_ref],mi_c[bande_ref],rmodal_c,log10var_c,\
                                                    20.0,0.,0.1)
f_granu  = file(ficAERgranu,'r')
ligne    = f_granu.readline()
Kext_ref = float(ligne.split()[0])
f_granu.close()

#Simulation pour la bande a simuler
if bimodalOption == 2:
    (ficOSup,ficAERgranu,Tdes_dir,Tdes_dif) = lance_simu_OS(fic_res_angles,fic_res_angles_sos,tauRay[num_bd],tau,bandes[num_bd],tau,bandes[bande_ref],proportion_AOT_c,\
                                                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                                                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c,\
                                                20.0,0.,0.1)
else: #Si on utilise les Concentrations Volumiques
    (ficOSup,ficAERgranu,Tdes_dir,Tdes_dif) = lance_simu_OS_CV(fic_res_angles,fic_res_angles_sos,tauRay[num_bd],tau,bandes[num_bd],tau,bandes[bande_ref],CVcoarse,CVfine,\
                                                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                                                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c,\
                                                20.0,0.,0.1)
f_granu = file(ficAERgranu,'r')
ligne   = f_granu.readline()
Kext_bd = float(ligne.split()[0])
f_granu.close()

#============================
# Boucle pour simuler la LUT
#============================
#Epaisseur optique
for num_tau in range(len(ep_opt)):
    tau = ep_opt[num_tau] 
    print "\n*******tau="+str(tau)

    if bimodalOption == 2:
        ficAERgranu = sos_aerosols_bimodal(fic_res_angles,tau*Kext_bd/Kext_ref,bandes[num_bd],tau,bandes[bande_ref],proportion_AOT_c,\
                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c)
    else: #Si on utilise les Concentrations Volumiques
        ficAERgranu = sos_aerosols_bimodal_CV(fic_res_angles,tau*Kext_bd/Kext_ref,bandes[num_bd],tau,bandes[bande_ref],CVcoarse,CVfine,\
                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c)

    #Altitudes
    for alt in range(len(liste_altitude)):
        press = PdeZ(liste_altitude[alt]) 
        print "altitude et pression :",alt,press
        ficPROFIL = sos_profil(tauRay[num_bd]/P0*press,tau*Kext_bd/Kext_ref)        
        
        #Calcul albedo atmospherique (independant de l'angle solaire)
        #============================================================
        theta_s = liste_theta_s[0]
        rho_surf0 = 0.
        rho_surf1 = 0.2    
        rho_surf2 = 0.4
        
        #rho_surf=0
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif) = sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf0,theta_s,0,pas_phi,False)
        f_in = file(ficOSup,'r')
        lignes = f_in.readlines()
        f_in.close
        num_ligne = 0
        rho_toa0 = float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)
        
        #rho_surf1
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif) = sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf1,theta_s,0,pas_phi,False)
        f_in = file(ficOSup,'r')
        lignes = f_in.readlines()
        f_in.close
        num_ligne = 0
        rho_toa1 = float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)

        #rho_surf2
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif) = sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf2,theta_s,0,pas_phi,False)
        f_in = file(ficOSup,'r')
        lignes = f_in.readlines()
        f_in.close
        num_ligne = 0
        rho_toa2 = float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)

	if isnan(rho_toa0) or isnan(rho_toa1) or isnan(rho_toa2):
	    #Bug sur tres faibles epaisseurs optiques
	    print "NaN * NaN * NaN * NaN * NaN * NaN *NaN * NaN *NaN * NaN"
	    albedo[alt,num_tau] = albedo[alt-1,num_tau]
	    for ts in range(len(liste_theta_s)) :
		Tdir[ts,alt,num_tau] = Tdir[ts,alt-1,num_tau]
		Tdif[ts,alt,num_tau] = Tdif[ts,alt-1,num_tau]
		for num_rho in range(len(liste_rsurf)):
		    for tv in range(len(liste_theta_v)):
			for iphi in range(len(liste_delta_phi)):
			    rho_toa[num_rho,num_tau,alt,iphi,tv,ts] = rho_toa[num_rho,num_tau,alt-1,iphi,tv,ts]
	else:
	    #Calcul de l'albedo atmospherique
	    rho_delta2 = rho_toa2-rho_toa0
	    rho_delta1 = rho_toa1-rho_toa0
	    if isnan(rho_delta2) or isnan(rho_delta1):
		albedo[alt,num_tau] = 0.0001
	    else :
		albedo[alt,num_tau] = (rho_delta2/rho_surf2-rho_delta1/rho_surf1)/(rho_delta2-rho_delta1)

	    for ts in range(len(liste_theta_s)):
		theta_s = liste_theta_s[ts]
		print "theta_s =",theta_s
		(fic_res_angles,fic_res_angles_sos) = sos_angles(theta_s,nb_mu,fic_angles)

		#Transmission directe et diffuse calculees pour rho_surf=0
		(ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif) = sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,0,theta_s,0,pas_phi,True)
		if isnan(Tdes_dif):
		    Tdir[ts,alt,num_tau] = 0.9999
		    Tdif[ts,alt,num_tau] = 0.0001
		else :
		    Tdir[ts,alt,num_tau] = Tdes_dir
		    Tdif[ts,alt,num_tau] = Tdes_dif

		print 'Tdir, Tdif =',Tdir[ts,alt,num_tau],Tdif[ts,alt,num_tau]

		#Reflectance de surface
		#======================
		for num_rho in range(len(liste_rsurf)):
		    rho = liste_rsurf[num_rho]
		    (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif) = sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho,theta_s,0,pas_phi,False)

		    #lecture du resultat
		    f_in = file(ficOSup,'r')
		    num_ligne = 0
		    lignes = f_in.readlines()

		    for ligne in lignes:
			iphi = nb_phi-num_ligne/len(liste_theta_v)-1 #180 - (phi_s-phi_v), convention OS
			if iphi>=0:
			    tv = num_ligne%len(liste_theta_v)
			    liste_ligne = ligne.split()

			    #Verification du phi et du theta_v
			    phi = 180 - liste_delta_phi[iphi] #180 - (phi_s-phi_v), convention OS
			    phi_lu = float(liste_ligne[0])
			    tv_lu = float(liste_ligne[1])
			    if (tv_lu < liste_theta_v[tv] -0.01) or (tv_lu > liste_theta_v[tv] +0.01) or (phi_lu < phi-0.1) or (phi_lu > phi+0.1):                           
				print "theta_v n est pas dans le fichier de resultats "+ ficOSup
				print ligne,phi,liste_theta_v[tv]
				print toto
			    else:
				rho_toa[num_rho,num_tau,alt,iphi,tv,ts]=float(ligne.split()[2])/cos(theta_s*pi/180.)   
			num_ligne+=1
		    f_in.close
        print "refl fonction de theta_s:",rho_toa[0,num_tau,alt,0,0,:] 

#Inversion de la lut
#==========================================
for ts in range(len(liste_theta_s)):
    for tv in range(len(liste_theta_v)):
        for iphi in range(len(liste_delta_phi)):
            for alt in range(len(liste_altitude)):
                for itau in range(len(ep_opt)):
                    coefs = na.polyfit(rho_toa[:,itau,alt,iphi,tv,ts],liste_rsurf,3);
                    rho_surf[:,itau,alt,iphi,tv,ts] = na.polyval(coefs,liste_rtoa);
                    rho_surf_CS[ts,tv,iphi,alt,itau,:] = rho_surf[:,itau,alt,iphi,tv,ts]
                    
#Ecriture des sorties pour chaque bande
#==========================================
print rho_toa[0,0,0,0,0,:]      
rho_toa.tofile(path_out+'/refl_'+chaine)           #fichier binaire
rho_surf.tofile(path_out+'/lut_inv_'+chaine)
rho_surf_CS.tofile(path_out+'/lut_inv_CS_'+chaine) #fichier binaire
albedo.tofile(path_out+'/'+nom_lut_albedo)         #fichier binaire
Tdir.tofile(path_out+'/'+nom_lut_Tdir)             #fichier binaire
Tdif.tofile(path_out+'/'+nom_lut_Tdif)             #fichier binaire

#Ecriture des 5 fichiers texte (pour refl et lut_inv, albedo, Tdir, Tdif)
#=================================================================================
#Pour la lut_inverse
f_luttxt=file(path_out+'/lut_inv_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("rtoa ")
for i in liste_rtoa :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("d_phi ")
for i in liste_delta_phi :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("th_v ")
for i in liste_theta_v :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("th_s ")
for i in liste_theta_s :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.close()
#=================================================================================
#Pour la lut_inverse
f_luttxt=file(path_out+'/lut_inv_CS_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("th_s ")
for i in liste_theta_s :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("th_v ")
for i in liste_theta_v :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("d_phi ")
for i in liste_delta_phi :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("rtoa ")
for i in liste_rtoa :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.close()

#=======================================================
#Pour la lut directe
f_luttxt=file(path_out+'/refl_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("rsurf ")
for i in liste_rsurf :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("d_phi ")
for i in liste_delta_phi :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("th_v ")
for i in liste_theta_v :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("th_s ")
for i in liste_theta_s :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')


f_luttxt.close()
#=================================
#Pour l'albedo
f_luttxt=file(path_out+'/albedo_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.close()

#=================================
#Pour Tdir
f_luttxt=file(path_out+'/Tdir_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("th ")
for i in liste_theta_s :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.close()

#=================================
#Pour Tdif
f_luttxt=file(path_out+'/Tdif_'+chaine+'.txt','w') #fichier .dat

f_luttxt.write("th ")
for i in liste_theta_s :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("alt ")
for i in liste_altitude :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.write("tau ")
for i in ep_opt :
      f_luttxt.write(str(i)+" ")
f_luttxt.write('\n')

f_luttxt.close()



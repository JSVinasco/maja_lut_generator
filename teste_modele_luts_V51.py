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

    
###########################################################
#calcul de pression atmospherique en fonction de l'altitude
##########################################################
def PdeZ(Z) :
    """ 
    calcul de pression atmospherique en fonction de l'altitude
    altitude en mètres
    """
    p = 1013.25 * pow( 1 - 0.0065 * Z / 288.15 , 5.31 )
    return(p)


###################################################
#                  prog principal
###################################################
if len(sys.argv) !=5 :
    print 'Usage :'
    print '      '+ str(sys.argv[0])+ ' satellite site proportion_AOT_grossier bande'
    print 'Exemple :'
    print '      '+ str(sys.argv[0])+ ' LANDSAT5 Lacrau 0 0'
    
    sys.exit(-1)  

sat                 =str(sys.argv[1])
site                =str(sys.argv[2])
proportion_AOT_c    =float(sys.argv[3])
num_bd              =int(sys.argv[4])

if sat=='FORMOSAT' :
    import param_luts_formosat as param_luts
elif sat=='S2' :
    import param_luts_S2 as param_luts
elif sat=='LANDSAT5' :
    import param_luts_LANDSAT5 as param_luts
elif sat=='LANDSAT7' :
    import param_luts_LANDSAT7 as param_luts
elif sat=='LANDSAT8' :
    import param_luts_LANDSAT8 as param_luts
elif sat=='SPOT4H1' :
    import param_luts_SPOT4H1 as param_luts
elif sat=='SPOT4TAKE5' :
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

    
bandes,bande_ref, tauRay,liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c=param_luts.param(site)

nb_mu =40 #nombre d'angles de gauss dans les os
nb_phi=7
pas_phi=180/(nb_phi-1)

liste_theta_s  =na.linspace(0,75,11)
#liste_theta_s  =na.linspace(0,75,2)

liste_delta_phi=na.linspace(0,180,7)



# liste_theta_v  =na.array([0.00,6.02,13.58,21.09,28.50,35.78,42.87,49.74,56.32])
# liste_mu       =na.array([1,5,11,17,23,29,35,41,47])-1
liste_altitude =na.arange(0,3100,1000)
ep_opt         =na.linspace(0,1.5,25)
#ep_opt         =na.linspace(0,1.5,2)
liste_rsurf =na.linspace(0,1.3,17)
#liste_rsurf =na.linspace(0,1.3,2)
P0             =1013.25

#echantillonnage pour la lut inverse
liste_rtoa=na.arange(-0.2,1.2,0.07)

# répertoires et variables d'environnement
#définition des répertoires
SOS_RACINE = os.getenv('RACINE')
maison      =os.getenv('HOME')


if SOS_RACINE is None :
    SOS_RACINE=maison+'/SOSV51'
    os.environ['RACINE']=SOS_RACINE

os.environ['SOS_RACINE']=SOS_RACINE

chaine='V51_%s_%s_prop_%4.2f_bande_%d'%(sat,site,proportion_AOT_c,bandes[num_bd])

#creation des repertoires

SOS_RESULT ='/mnt/data/SOS_TEST/'+ chaine
fic_trace  =SOS_RESULT+'/TRACE/Trace_AEROSOLS.txt' 
    
if not (os.path.exists(SOS_RESULT)):
    os.mkdir(SOS_RESULT)
    os.mkdir(SOS_RESULT+'/TRACE')
    os.mkdir(SOS_RESULT+'/MIE_V51')
    os.mkdir(SOS_RESULT+'/SURFACE')
    os.mkdir(SOS_RESULT+'/SOS')

print SOS_RESULT
   
SOS_RACINE_MU=SOS_RACINE+'/fic'
os.environ['SOS_RESULT']=SOS_RESULT
os.environ['SOS_RACINE_MU']=SOS_RACINE_MU


#fichier des angles de l'utilisateur
fic_angles=SOS_RESULT+"/SOS/fic_angles_"+chaine+".txt"
f=file(fic_angles,"w")
for tv in liste_theta_v:
    f.write("%f \n"%tv)
f.close()

(fic_res_angles,fic_res_angles_sos) =sos_angles(liste_theta_s[0],nb_mu,fic_angles)

###################pour chaque table   
#############################################

rho_toa =na.zeros([len(liste_rsurf),len(ep_opt),len(liste_altitude),len(liste_delta_phi),len(liste_theta_v),len(liste_theta_s)],'Float32')
rho_surf=na.zeros([len(liste_rtoa) ,len(ep_opt),len(liste_altitude),len(liste_delta_phi),len(liste_theta_v),len(liste_theta_s)],'Float32')
rho_surf_CS=na.zeros([ len(liste_theta_s),len(liste_theta_v),len(liste_delta_phi),len(liste_altitude),len(ep_opt),len(liste_rtoa)],'Float32')

albedo  =na.zeros([len(liste_altitude),len(ep_opt)],'Float32')
Tdif    =na.zeros([len(liste_theta_s),len(liste_altitude),len(ep_opt)],'Float32')
Tdir    =na.zeros([len(liste_theta_s),len(liste_altitude),len(ep_opt)],'Float32')

nom_lut_albedo='albedo_'+chaine
nom_lut_Tdif='Tdif_'+chaine
nom_lut_Tdir='Tdir_'+chaine

#calcul du rapport d'extinctions pour l'épaisseur optique aérosols
#=================================================================
tau=0.1
#simu pour la bande de référence
(ficOSup,ficAERgranu,Tdes_dir,Tdes_dif)=lance_simu_OS(fic_res_angles,fic_res_angles_sos,tauRay[bande_ref],tau,bandes[bande_ref],tau,bandes[bande_ref],proportion_AOT_c,\
                                                    mr_f[bande_ref],mi_f[bande_ref],mr_f[bande_ref],mi_f[bande_ref],rmodal_f,log10var_f,\
                                                    mr_c[bande_ref],mi_c[bande_ref],mr_c[bande_ref],mi_c[bande_ref],rmodal_c,log10var_c,\
                                                    20.0,0.,0.1)
f_granu=file(ficAERgranu,'r')
ligne=f_granu.readline()
Kext_ref=float(ligne.split()[0])
f_granu.close()

#simu pour la bande a simuler
(ficOSup,ficAERgranu,Tdes_dir,Tdes_dif)=lance_simu_OS(fic_res_angles,fic_res_angles_sos,tauRay[num_bd],tau,bandes[num_bd],tau,bandes[bande_ref],proportion_AOT_c,\
                                                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                                                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c,\
                                                20.0,0.,0.1)
f_granu=file(ficAERgranu,'r')
ligne=f_granu.readline()
Kext_bd=float(ligne.split()[0])
f_granu.close()



##############################"Boucle pour simuler la LUT
#########################################################

#epaisseur optique
for num_tau in range(len(ep_opt)):
    tau=ep_opt[num_tau] 
    print "*******tau="+str(tau)
    ficAERgranu=sos_aerosols_bimodal(fic_res_angles,tau*Kext_bd/Kext_ref,bandes[num_bd],tau,bandes[bande_ref],proportion_AOT_c,\
                mr_f[bande_ref],mi_f[bande_ref],mr_f[num_bd],mi_f[num_bd],rmodal_f,log10var_f,\
                mr_c[bande_ref],mi_c[bande_ref],mr_c[num_bd],mi_c[num_bd],rmodal_c,log10var_c)
    #altitudes
    for alt in range(len(liste_altitude)):
        press=PdeZ(liste_altitude[alt]) 
        print "altitude et pression :", alt,press
        ficPROFIL  =sos_profil(tauRay[num_bd]/P0*press,tau*Kext_bd/Kext_ref)        
        
        #calcul albedo atmospherique (independant de l'angle solaire)
        #============================
        theta_s=liste_theta_s[0]
        rho_surf0=0.
        rho_surf1=0.2    
        rho_surf2=0.4
        
        #rho_surf=0
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf0,theta_s,0,pas_phi,False)
        f_in=file(ficOSup,'r')
        lignes=f_in.readlines()
        f_in.close
        num_ligne=0
        rho_toa0=float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)
        
        #rho_surf1
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf1,theta_s,0,pas_phi,False)
        f_in=file(ficOSup,'r')
        lignes=f_in.readlines()
        f_in.close
        num_ligne=0
        rho_toa1=float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)

        #rho_surf2
        (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho_surf2,theta_s,0,pas_phi,False)
        f_in=file(ficOSup,'r')
        lignes=f_in.readlines()
        f_in.close
        num_ligne=0
        rho_toa2=float(lignes[num_ligne].split()[2])/cos(theta_s*pi/180.)


	if isnan(rho_toa0) or isnan(rho_toa1) or isnan(rho_toa2) :
	    # bug sur très faibles épaisseurs optiques
	    print "NaN * NaN * NaN * NaN * NaN * NaN *NaN * NaN *NaN * NaN"
	    albedo[alt,num_tau]=albedo[alt-1,num_tau]
	    for ts in range(len(liste_theta_s)) :
		Tdir[ts,alt,num_tau]=Tdir[ts,alt-1,num_tau]
		Tdif[ts,alt,num_tau]=Tdif[ts,alt-1,num_tau]
		for num_rho in range(len(liste_rsurf)):
		    for tv in range(len(liste_theta_v)):
			for iphi in range(len(liste_delta_phi)):
			    rho_toa[num_rho,num_tau,alt,iphi,tv,ts]=rho_toa[num_rho,num_tau,alt-1,iphi,tv,ts]
	else:
	    # calcul de l'albedo atmospherique
	    rho_delta2=rho_toa2-rho_toa0
	    rho_delta1=rho_toa1-rho_toa0
	    if isnan(rho_delta2) or isnan(rho_delta1):
		albedo[alt,num_tau]= 0.0001
	    else :
		albedo[alt,num_tau]=(rho_delta2/rho_surf2-rho_delta1/rho_surf1)/(rho_delta2-rho_delta1)


	    print rho_toa0,rho_toa1,rho_toa2
	    print 'tau, albedo atm s', tau, albedo[alt,num_tau]

	    for ts in range(len(liste_theta_s)) :
		theta_s=liste_theta_s[ts]
		print "theta_s= ",theta_s
		(fic_res_angles,fic_res_angles_sos) =sos_angles(theta_s,nb_mu,fic_angles)

		# transmission directe et diffuse calculees pour rho_surf =0
		(ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,0,theta_s,0,pas_phi,True)
		if isnan(Tdes_dif):
		    Tdir[ts,alt,num_tau]=0.9999
		    Tdif[ts,alt,num_tau]=0.0001
		else :
		    Tdir[ts,alt,num_tau]=Tdes_dir
		    Tdif[ts,alt,num_tau]=Tdes_dif

		print 'Tdir, Tdif =',Tdir[ts,alt,num_tau],Tdif[ts,alt,num_tau]
		#reflectance de surface
		#======================
		for num_rho in range(len(liste_rsurf)):
		    rho=liste_rsurf[num_rho]
		    (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho,theta_s,0,pas_phi,False)

		    #lecture du résultat
		    f_in=file(ficOSup,'r')
		    num_ligne=0
		    lignes=f_in.readlines()
    #                 print lignes[0:10]
		    for ligne in lignes :                   

			iphi      =nb_phi-num_ligne/len(liste_theta_v) -1 #180 - (phi_s-phi_v), convention OS
			if iphi>=0 :
			    tv=num_ligne%len(liste_theta_v)

			    liste_ligne=ligne.split()

			    #verification du phi et du theta_v
			    phi=180 - liste_delta_phi[iphi]  # 180 - (phi_s-phi_v), convention OS
			    phi_lu=float(liste_ligne[0])
			    tv_lu =float(liste_ligne[1])
			    if (tv_lu < liste_theta_v[tv] -0.01) or (tv_lu > liste_theta_v[tv] +0.01) or (phi_lu < phi-0.1) or (phi_lu > phi+0.1):                           
				print "theta_v n est pas dans le fichier de resultats "+ ficOSup
				print ligne,phi,liste_theta_v[tv]
				print toto
			    else :
				rho_toa[num_rho,num_tau,alt,iphi,tv,ts]=float(ligne.split()[2])/cos(theta_s*pi/180.)   
			num_ligne+=1
		    f_in.close
        print "refl fonction de theta_s:",rho_toa[0,num_tau,alt,0,0,:] 

#inversion de la lut
#==========================================

for ts in range(len(liste_theta_s)) :
    for tv in range(len(liste_theta_v)) :
        for iphi in range(len(liste_delta_phi)):
            for alt in range(len(liste_altitude)):
                for itau in range(len(ep_opt)):
                    coefs=na.polyfit(rho_toa[:,itau,alt,iphi,tv,ts],liste_rsurf,3);
                    rho_surf[:,itau,alt,iphi,tv,ts]=na.polyval(coefs,liste_rtoa);
                    rho_surf_CS[ts,tv,iphi,alt,itau,:]=rho_surf[:,itau,alt,iphi,tv,ts]
                    

#ecriture des sorties pour chaque bande
#==========================================
print   rho_toa[0,0,0,0,0,:]      
rho_toa.tofile(maison+'/DONNEES/LUTS/refl_'+chaine) #fichier binaire
rho_surf.tofile(maison+'/DONNEES/LUTS/lut_inv_'+chaine)
rho_surf_CS.tofile(maison+'/DONNEES/LUTS/lut_inv_CS_'+chaine) #fichier binaire
albedo.tofile(maison+'/DONNEES/LUTS/'+nom_lut_albedo) #fichier binaire
Tdir.tofile(maison+'/DONNEES/LUTS/'+nom_lut_Tdir) #fichier binaire
Tdif.tofile(maison+'/DONNEES/LUTS/'+nom_lut_Tdif) #fichier binaire

#Ecriture des 5 fichiers texte (pour refl et lut_inv, albedo, Tdir, Tdif)
#=================================================================================
#pour la lut_inverse
f_luttxt=file(maison+'/DONNEES/LUTS/lut_inv_'+chaine+'.txt','w') #fichier .dat

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
#pour la lut_inverse
f_luttxt=file(maison+'/DONNEES/LUTS/lut_inv_CS_'+chaine+'.txt','w') #fichier .dat

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
#pour la lut directe
f_luttxt=file(maison+'/DONNEES/LUTS/refl_'+chaine+'.txt','w') #fichier .dat

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
#pour l'albedo
f_luttxt=file(maison+'/DONNEES/LUTS/albedo_'+chaine+'.txt','w') #fichier .dat

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
#pour Tdir
f_luttxt=file(maison+'/DONNEES/LUTS/Tdir_'+chaine+'.txt','w') #fichier .dat

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
#pour Tdir
f_luttxt=file(maison+'/DONNEES/LUTS/Tdif_'+chaine+'.txt','w') #fichier .dat

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

#graphique fonction de phase :
if graphique==True:

    ftrace=file(fic_trace,'r')
    lignes=ftrace.readlines()
    ftrace.close()
    phase   =na.zeros(80,'Float32')


    for i in na.arange(80):
	lig=lignes[558+i]
	phase[i]   =float(lig.split()[0])
	fonction[num_bd,i]=float(lig.split()[1])

	# graphique fonction de phase :
    semilogy(phase,fonction[0,:],phase,fonction[1,:],phase,fonction[2,:],phase,fonction[3,:])
    ylim([0.01,100])
    title(chaine)
    xlabel('Angle de diffusion')
    ylabel('Fonction de phase')
    
    grid(True)
    legend((str(bandes[0]),str(bandes[1]),str(bandes[2]),str(bandes[3])),'upper right')
    savefig('fonction_de_phase_N_'+chaine+'_bande_'+str(num_bd)+'.png',format='png')

    show()

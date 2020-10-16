#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#$Author$
#$Date$
#$Log$

import os
#####################################################
#routine pour lancer une simu des OS
#####################################################
def lance_simu_OS(fic_res_angles, fic_res_angles_sos,tauRay,tauAer,bande,tauAer_ref,bande_ref,proportion_AOT_c,\
                                                     mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
                                                     mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c,\
                                                     theta_s,phi,rho):

    dphi=0 # mode plan par plan (a changer)
    ficAERgranu                                     =sos_aerosols_bimodal(fic_res_angles,tauAer,bande,tauAer_ref,bande_ref,proportion_AOT_c,\
                                                     mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
                                                     mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c)
    ficPROFIL                                       =sos_profil(tauRay,tauAer)
    (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho,theta_s,phi,dphi,False)
    return(ficOSup,ficAERgranu,Tdes_dir,Tdes_dif)

#Si on utilise les Concentrations Volumiques
def lance_simu_OS_CV(fic_res_angles,fic_res_angles_sos,tauRay,tauAer,bande,tauAer_ref,bande_ref,CVcoarse,CVfine,\
                                                     mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
                                                     mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c,\
                                                     theta_s,phi,rho):

    dphi = 0 #Mode plan par plan (a changer)
    ficAERgranu                                     =sos_aerosols_bimodal_CV(fic_res_angles,tauAer,bande,tauAer_ref,bande_ref,CVcoarse,CVfine,\
                                                     mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
                                                     mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c)
    ficPROFIL                                       =sos_profil(tauRay,tauAer)
    (ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)  =sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho,theta_s,phi,dphi,False)
    return(ficOSup,ficAERgranu,Tdes_dir,Tdes_dif)

#========================================================================
#=========================sos_angles==================================
#========================================================================

def sos_angles(theta_s,nb_gauss,fic_angles):
    SOS_RACINE      =os.getenv('SOS_RACINE')
    SOS_RESULT      =os.getenv('SOS_RESULT')
    SOS_RACINE_MU   =os.getenv('SOS_RACINE_MU')
    
#     print "##############################################"
#     print "######"+fic_angles+ "######"
#     print "##############################################"
#     os.system('cat '+ fic_angles)
    
    fic_res_angles=SOS_RESULT+"/SOS/AER_UsedAngles.txt"
    fic_res_angles_sos=SOS_RESULT+"/SOS/SOS_UsedAngles.txt"
    nom_exe=SOS_RACINE+'/exe/SOS_ANGLES.exe'
    commande= nom_exe+ " -ANG.Rad.Thetas "+ "%9.5f"%(theta_s)+\
                       " -ANG.Rad.NbGauss " + "%d"%(nb_gauss) +\
                       " -ANG.Rad.UserAngFile " + fic_angles+\
                       " -ANG.Rad.ResFile " + fic_res_angles_sos+\
                       " -ANG.Aer.NbGauss " + "%d"%(nb_gauss) +\
                       " -ANG.Aer.UserAngFile " + fic_angles+\
                       " -ANG.Aer.ResFile " + fic_res_angles+\
                       " -ANG.Log " +SOS_RESULT+"/Angles.Log"
                                          
#     print "##################"
#     print commande
#     print "##################"
    os.system(commande)

    return(fic_res_angles,fic_res_angles_sos)                
    
#========================================================================
#=========================sos _aerosols_bimodal==================================
#========================================================================
def sos_aerosols_bimodal(fic_res_angles,tauAer,long_onde,tauAer_ref,long_onde_ref,proportion_AOT_c,\
    mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
    mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c):

#tauAer         2paisseur optique
#longonde       Longueur d'onde en nanomètres.
#mr             partie reelle de l'indice de refraction
#mi             partie imaginaire de l'indice de refraction (valeur negative)
#granuvar1      Si LND : Rayon modal (en microns).
#               Si Loi de Junge : Rayon minimal (en microns).
#granuvar2      Si LND : log10 de la variance.
#               Si Loi de Junge : puissance appliquee au rayon

    print long_onde
    longonde=long_onde/1000.
    longonde_ref=long_onde_ref/1000.

    ##valeur du parametre de taille (alpha) a partir de laquelle 
    ##on arrete le calcul
    ##----------------------------------------------------------
    alphaMax=4000.00     #Format f9.2 (0.01 <= alphaMax < 1.E+05)
                  
    # répertoires et variables d'environnement
    SOS_RACINE      =os.getenv('SOS_RACINE')
    SOS_RESULT      =os.getenv('SOS_RESULT')
    SOS_RACINE_MU   =os.getenv('SOS_RACINE_MU')
    
#     print SOS_RACINE,SOS_RESULT,SOS_RACINE_MU
    repMIE=SOS_RESULT+'/MIE_V51'

    ficTraceMIE='0'
    ficTraceAER=SOS_RESULT+'/TRACE/Trace_AEROSOLS.txt'
    ficAERgranu=SOS_RESULT+'/SOS/ResultGRANU.txt'
    nom_exe= SOS_RACINE+'/exe/SOS_AEROSOLS.exe'  
    
    commande = nom_exe + " -AER.AOT " + "%9.5f"%(tauAer) +\
                         " -AER.AngFile " + fic_res_angles +\
                         " -AER.Wa " + "%9.5f"%(longonde)+\
                         " -AER.Tronca " + "1" +\
                         " -AER.Log " + ficTraceAER+\
                         " -AER.MieLog "+ ficTraceMIE+\
                         " -AER.DirMie "+ repMIE+\
                         " -AER.ResFile "+ ficAERgranu+\
                         " -AER.Model "+ "3" +\
                         " -AER.BMD.VCdef " +"2" +\
                         " -AER.BMD.RAOT " + "%9.5f"%(proportion_AOT_c)+\
                         " -AER.Waref "+ "%9.5f"%(longonde_ref)+\
                         " -AER.AOTref "+ "%9.5f"%(tauAer_ref)+\
                         " -AER.BMD.CM.MRwa "+"%9.5f"%(mr_c)+\
                         " -AER.BMD.CM.MIwa "+"%9.5f"%(mi_c)+\
                         " -AER.BMD.CM.MRwaref "+"%9.5f"%(mr_c_ref)+\
                         " -AER.BMD.CM.MIwaref "+"%9.5f"%(mi_c_ref)+\
                         " -AER.BMD.CM.SDradius "+"%9.5f"%(rmodal_c)+\
                         " -AER.BMD.CM.SDvar "+"%9.5f"%(log10var_c)+\
                         " -AER.BMD.FM.MRwa "+"%9.5f"%(mr_f)+\
                         " -AER.BMD.FM.MIwa "+"%9.5f"%(mi_f)+\
                         " -AER.BMD.FM.MRwaref "+"%9.5f"%(mr_f_ref)+\
                         " -AER.BMD.FM.MIwaref "+"%9.5f"%(mi_f_ref)+\
                         " -AER.BMD.FM.SDradius "+"%9.5f"%(rmodal_f)+\
                         " -AER.BMD.FM.SDvar "+"%9.5f"%(log10var_f)

#                         " -MMD.Mie.AlphaMax " + "%9.5f"%(alphaMax)+\
#     print "##################"
#     print commande
#     print "##################"
    os.system(commande)

    return(ficAERgranu)


#Si on utilise les Concentrations Volumiques
def sos_aerosols_bimodal_CV(fic_res_angles,tauAer,long_onde,tauAer_ref,long_onde_ref,CVcoarse,CVfine,\
    mr_f_ref,mi_f_ref,mr_f,mi_f,rmodal_f,log10var_f,\
    mr_c_ref,mi_c_ref,mr_c,mi_c,rmodal_c,log10var_c):

#tauAer         Epaisseur optique
#longonde       Longueur d'onde en nanometres
#mr             Partie reelle de l'indice de refraction
#mi             Partie imaginaire de l'indice de refraction (valeur negative)
#granuvar1      Si LND : rayon modal (en microns)
#               Si loi de Junge : rayon minimal (en microns)
#granuvar2      Si LND : log10 de la variance
#               Si loi de Junge : puissance appliquee au rayon

    print long_onde
    longonde = long_onde/1000.
    longonde_ref = long_onde_ref/1000.

    #Valeur du parametre de taille (alpha) a partir de laquelle on arrete le calcul
    alphaMax = 4000.00 #Format f9.2 (0.01 <= alphaMax < 1.E+05)
                  
    #Repertoires et variables d'environnement
    SOS_RACINE    = os.getenv('SOS_RACINE')
    SOS_RESULT    = os.getenv('SOS_RESULT')
    SOS_RACINE_MU = os.getenv('SOS_RACINE_MU')
    
    repMIE = SOS_RESULT+'/MIE_V51'

    ficTraceMIE = '0'
    ficTraceAER = SOS_RESULT+'/TRACE/Trace_AEROSOLS.txt'
    ficAERgranu = SOS_RESULT+'/SOS/ResultGRANU.txt'
    nom_exe     = SOS_RACINE+'/exe/SOS_AEROSOLS.exe'  
    
    #Modification de " -AER.BMD.VCdef " +"1" +\
    #Suppression de : " -AER.BMD.RAOT " + "%9.5f"%(proportion_AOT_c)+\
    #Ajout de       : " -AER.BMD.CoarseVC " + "%9.5f"%(CVcoarse)+\
    #et de          : " -AER.BMD.FineVC " + "%9.5f"%(CVfine)+\
    commande = nom_exe + " -AER.AOT " + "%9.5f"%(tauAer) +\
                         " -AER.AngFile " + fic_res_angles +\
                         " -AER.Wa " + "%9.5f"%(longonde)+\
                         " -AER.Tronca " + "1" +\
                         " -AER.Log " + ficTraceAER+\
                         " -AER.MieLog "+ ficTraceMIE+\
                         " -AER.DirMie "+ repMIE+\
                         " -AER.ResFile "+ ficAERgranu+\
                         " -AER.Model "+ "3" +\
                         " -AER.BMD.VCdef " +"1" +\
                         " -AER.BMD.CoarseVC " + "%9.5f"%(CVcoarse)+\
                         " -AER.BMD.FineVC " + "%9.5f"%(CVfine)+\
                         " -AER.Waref "+ "%9.5f"%(longonde_ref)+\
                         " -AER.AOTref "+ "%9.5f"%(tauAer_ref)+\
                         " -AER.BMD.CM.MRwa "+"%9.5f"%(mr_c)+\
                         " -AER.BMD.CM.MIwa "+"%9.5f"%(mi_c)+\
                         " -AER.BMD.CM.MRwaref "+"%9.5f"%(mr_c_ref)+\
                         " -AER.BMD.CM.MIwaref "+"%9.5f"%(mi_c_ref)+\
                         " -AER.BMD.CM.SDradius "+"%9.5f"%(rmodal_c)+\
                         " -AER.BMD.CM.SDvar "+"%9.5f"%(log10var_c)+\
                         " -AER.BMD.FM.MRwa "+"%9.5f"%(mr_f)+\
                         " -AER.BMD.FM.MIwa "+"%9.5f"%(mi_f)+\
                         " -AER.BMD.FM.MRwaref "+"%9.5f"%(mr_f_ref)+\
                         " -AER.BMD.FM.MIwaref "+"%9.5f"%(mi_f_ref)+\
                         " -AER.BMD.FM.SDradius "+"%9.5f"%(rmodal_f)+\
                         " -AER.BMD.FM.SDvar "+"%9.5f"%(log10var_f)
    os.system(commande)

    return(ficAERgranu)

#========================================================================
#=========================sos_profil==================================
#========================================================================
def sos_profil(tauRay,tauAer):  
    

    ######## SI Profil  = 1 ########
    ##Echelle de hauteur du profil moleculaire (en km).
    HR=8.
    ##Echelle de hauteur du profil d'aerosols (en km).
    HA=2.
    
 
    # répertoires et variables d'environnement
    SOS_RACINE      =os.getenv('SOS_RACINE')
    SOS_RESULT      =os.getenv('SOS_RESULT')
    SOS_RACINE_MU   =os.getenv('SOS_RACINE_MU')
      
    ficTracePROFIL  =SOS_RESULT+'/TRACE/Trace_PROFIL.txt'
    ficPROFIL       =SOS_RESULT+'/SOS/ResultPROFIL_%s_%s.txt'%(str(tauRay),str(tauAer))
    nom_exe= SOS_RACINE+'/exe/SOS_PROFIL.exe'  

    commande = nom_exe + " -AP.ResFile " + ficPROFIL  +\
                         " -AP.Log " + ficTracePROFIL +\
                         " -AP.MOT " + "%9.5f"%(tauRay) +\
                         " -AP.HR " + "%9.5f"%(HR) +\
                         " -AP.AOT " + "%9.5f"%(tauAer)+\
                         " -AP.Type " + "1" +\
                         " -AP.AerHS.HA " +"%9.5f"%(HA)
#     print "##################"
#     print commande
#     print "##################"
    os.system(commande)
    return(ficPROFIL)

#========================================================================
#=========================sos_os==================================
#========================================================================
def sos_os(fic_res_angles_sos,ficAERgranu,ficPROFIL,rho,tetas,phi,dphi,trans):  
    #trans=True si on souhaite un calcul des transmissions
    
    ##Facteur de depolarisation (moleculaire).
    ron=0.0279

    ##Indice de type de sortie 
    ##(plan de visee ou diagramme polaire).
    ##-----------------------------------
    if dphi==0:
        optionVisee=1           # 1 : plan de visee.
    else :
        optionVisee=2           # 2 : diagramme polaire (ascii).
        phi=0. #inutile

    # répertoires et variables d'environnement
    SOS_RACINE      =os.getenv('SOS_RACINE')
    SOS_RESULT      =os.getenv('SOS_RESULT')
    SOS_RACINE_MU   =os.getenv('SOS_RACINE_MU')
   
    ficTraceSOS=SOS_RESULT+'/TRACE/Trace_SOS.txt'
    ficOSbin=SOS_RESULT+'/SOS/SOS_BIN'
    
    ##Nom du fichier resultat pour le champ montant.
    ficOSup=SOS_RESULT+'/SOS/ResultUP_angles.txt'
    ficOSupGauss=SOS_RESULT+'/SOS/ResultUP.txt'
    ##Nom du fichier resultat pour le champ descendant
    ficOSdown=SOS_RESULT+'/SOS/ResultDown.txt'
       
    ## Lancement du programme SOS
    nom_exe= SOS_RACINE+'/exe/SOS.exe'
    
    commande=nom_exe +  " -SOS.AngFile " + fic_res_angles_sos +\
                        " -SOS.AerFile " + ficAERgranu +\
                        " -SOS.ProfileFile " + ficPROFIL +\
                        " -SOS.ResBin " + ficOSbin +\
                        " -SOS.ResFileUp.UserAng " +ficOSup +\
                        " -SOS.ResFileUp " +ficOSupGauss +\
                        " -SOS.ResFileDown " + ficOSdown +\
                        " -SOS.Log " + ficTraceSOS +\
                        " -SOS.MDF " + "%9.5f"%(ron) +\
                        " -SURF.Alb " + "%9.5f"%(rho) +\
                        " -SURF.Type " + "0"+\
                        " -SOS.Thetas " + "%9.5f"%(tetas)+\
                        " -SOS.IGmax " +"20"
    if trans==True :
	   #print commande
           commande = commande +" -SOS.Trans " +SOS_RESULT+"/SOS/SOS_transm.txt"
                        
    if dphi==0:
        commande = commande +" -SOS.View " +"1"+\
                             " -SOS.View.Phi " + str(phi)
    else :
        commande = commande +" -SOS.View " +"2"+\
                             " -SOS.View.Dphi " + str(dphi)
                        
    # print "\n##### COMMANDE SOS OS #####"
    # print commande                    
    # print "##################"
    os.system(commande)

    
    if trans==True : 
        # recuperation des transmisssions directes et diffuses
        f_in=file(SOS_RESULT+"/SOS/SOS_transm.txt",'r')
        for ligne in f_in.readlines():
	    #print ligne
            if ligne.find('Direct')>=0 :
    #              print ligne
                Tdes_dir=float(ligne.split(':')[1])
            if ligne.find('td(thetas)')>=0 :     
    #              print ligne
                Tdes_dif=float(ligne.split('=')[2])
    else :
        Tdes_dir=-1
        Tdes_dif=-1

    return(ficOSbin,ficOSup,ficOSdown,Tdes_dir,Tdes_dif)

     
#############################################principal

if __name__=="__main__" :
    ficAERgranu=sos_aerosols_bimodal(0.1,443,1.55,-0.008,0.1,0.4)
    os.system('cat '+ficAERgranu)
    ficPROFIL  =sos_profil  (0.156,0.1)
    os.system('cat '+ficPROFIL)
    (ficOSbin,ficOSup,ficOSdown)=sos_os(ficAERgranu,ficPROFIL,0.2,0.,0.,30)
    os.system('cat '+ficOSup)
    

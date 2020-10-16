#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes              =[485, 566, 660, 819]
    bande_ref   =1 #565
    tauRay         =na.array([0.166053,0.0876010,0.0466880,0.0198165])
    #calcule avec nefertiti:/home/hagolle/PROG/SMAC/Spectres/integration_rayleigh.pro
    liste_theta_v  =na.array([1.71,6.16,12.86,21.80,28.51,35.22,41.93,50.87,57.58])
    
    if site=='Agoufou' :
	# à utiliser avec proportion de 0.2 pour gros aérosols
        mi_f=[-0.003,-0.002,-0.001,-0.000]
        mi_c=[-0.0002,-0.0001,-0.0000,-0.0000]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.55,1.55,1.55,1.55]
        rmodal_f=0.3
        log10var_f=0.26
        rmodal_c=2.
        log10var_c=0.4
    elif site=='Sulfate' :
        mi_f=[-0.0005,-0.0003,-0.0001,-0.0001]
        mr_f=[1.33,1.33,1.33,1.33]
        rmodal_f=0.07
        log10var_f=0.30
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f
    elif site=='BlackCarbon' :
        mi_f=[-0.45,-0.30,-0.1,-0.01]
        mr_f=[1.75,1.75,1.75,1.75]
        rmodal_f=0.0118
        log10var_f=0.3
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f
    elif site=='Organic' :
        mi_f=[-0.005,-0.003,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53]
        rmodal_f=0.0355
        log10var_f=0.26
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f  
    elif site=='SeaSalt' :
        mi_f=[-0.005,-0.003,-0.0001,-0.0001]
        mr_f=[1.33,1.33,1.33,1.33]
        rmodal_f=0.209
        log10var_f=0.3
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=1.75
        log10var_c=log10var_f              
    elif site=='Dust' :
        mi_f=[-0.003,-0.00164,-0.0001,-0.0001]
        mr_f=[1.48,1.48,1.48,1.48]
        rmodal_f=0.39
        log10var_f=0.3
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=1.90
        log10var_c=0.32   
    elif site=='Agoufou_optim' :
        mi_f=[-0.003,-0.002,-0.001,-0.000]
        mi_c=[-0.0002,-0.0001,-0.0000,-0.0000]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.55,1.55,1.55,1.55]
        rmodal_f=0.3
        log10var_f=0.26
        rmodal_c=2.
        log10var_c=0.4
    
    elif site=='Maroc' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002,-0.001,-0.0001]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.55,1.55,1.55,1.55]
        rmodal_f=0.15
        log10var_f=0.26
        rmodal_c=2.
        log10var_c=0.4    
    elif site=='Maroc_papier' :
        tau1=0.3
        tau2=0.6
        theta_s_site=27.
        theta_v_site=21.35
        phi_site    =0
        mi_f=[-0.003,-0.003,-0.003,-0.003]
        mi_c=[-0.003,-0.002,-0.0001,-0.0001]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.55,1.55,1.55,1.55]
        rmodal_f=0.1
        log10var_f=0.4
        rmodal_c=2.
        log10var_c=0.26    
    elif site=='Libye3' :
        tau1=0.2
        tau2=0.4
        theta_s_site=27.
        theta_v_site=43.61
        phi_site    =100
        N_Imag=[-0.001,-0.0015,-0.0025,-0.004]
    elif site=='Sudouest' :
        mi_f=[-0.003,-0.003,-0.003,-0.003]
        mi_c=[-0.003,-0.002,-0.0001,-0.0001]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.1
        log10var_f=0.4
        rmodal_c=1.
        log10var_c=0.26    
    elif site=='Lacrau' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002,-0.0001,-0.0001]
    #     mi_f=[-0.001,-0.001,-0.001,-0.001]
    #     mi_c=[-0.002,-0.002,-0.002,-0.002]
        mr_f=[1.44,1.44,1.44,1.44]
        mr_c=[1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.1
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26    
    elif site=='zerotrois' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002 ,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53]
        mr_c=[1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.3
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26        
    else :
        print('Mauvais site')
        sys.exit(-1)
    
        
    return bandes,bande_ref, tauRay, liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c
 

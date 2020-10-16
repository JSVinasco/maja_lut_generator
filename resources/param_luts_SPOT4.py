#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes =[443 ,510, 565, 665]
    tauRay =[0.233767,0.132423,0.0871672,0.0449294,0.0353388,0.0290548,0.0231687,0.0154892,0.0215036,0.0108469,0.00240469,0.00132053,0.000403033]    
    #calcule avec nefertiti:/home/hagolle/PROG/SMAC/Spectres/integration_rayleigh.pro
    bande_ref=2
    liste_theta_v  =na.array([0.,7.,14.,21.,28.,35.])

    #parametres definissant le modele d'aerosols
    #============================================
    if  site=='Lacrau' :
        mi_f=[-0.0005,-0.0001,-0.0001,-0.0001]
        mr_f=[1.44,1.44,1.44,1.44]
        rmodal_f=0.1
        log10var_f=0.26   
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f
    elif site=='zerotrois' :
        mi_f=[-0.0005,-0.0001,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53]
        rmodal_f=0.3
        log10var_f=0.26
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f
    elif site=='Sulfate' :
        mi_f=[-0.0005,-0.0001,-0.0001,-0.0001]
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
        mi_f=[-0.005,-0.001,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53]
        rmodal_f=0.0355
        log10var_f=0.26
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=rmodal_f
        log10var_c=log10var_f  
    elif site=='SeaSalt' :
        mi_f=[-0.005,-0.001,-0.0001,-0.0001]
        mr_f=[1.33,1.33,1.33,1.33]
        rmodal_f=0.209
        log10var_f=0.3
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=1.75
        log10var_c=log10var_f              
    elif site=='Dust' :
        mi_f=[-0.00164,-0.0005,-0.0001,-0.0001]
        mr_f=[1.48,1.48,1.48;1.48]
        rmodal_f=0.39
        log10var_f=0.3
        mr_c=mr_f
        mi_c=mi_f
        rmodal_c=1.90
        log10var_c=0.32   
    else :
        print('Mauvais site')
        sys.exit(-1)
    
            
    return bandes,bande_ref, tauRay, liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c
 
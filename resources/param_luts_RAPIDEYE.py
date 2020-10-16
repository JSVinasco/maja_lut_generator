#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes              =[477, 555, 658, 709, 802]
    bande_ref   =1 #565
    tauRay         =na.array([0.17721,0.0943932,0.0471007,0.0348636,0.0212539])
    #calcule avec nefertiti:/home/hagolle/PROG/SMAC/Spectres/integration_rayleigh.pro
    liste_theta_v  =na.array([1.71,6.16,12.86,21.80,28.51,35.22,41.93,50.87,57.58])
      
    if site=='zerodeux' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002 ,-0.0001,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53,1.53]
        mr_c=[1.44,1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.2
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26        
    else :
        print('Mauvais modèle')
        sys.exit(-1)
    
        
    return bandes,bande_ref, tauRay, liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c
 

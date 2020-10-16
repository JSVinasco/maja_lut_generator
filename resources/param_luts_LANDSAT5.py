#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes =[485 ,570, 660, 835, 1670, 2208]
    tauRay =[0.16385,0.08539,0.04661,0.01818,0.00112,0.00036]
    #calcule avec nefertiti:/home/hagolle/PROG/SMAC/Spectres/integration_rayleigh.pro
    bande_ref=1
    liste_theta_v  =na.array([0.,7.,13.])

    #parametres definissant le modele d'aerosols
    #============================================
    if site=='Lacrau' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002 ,-0.0001,-0.0001,-0.0001,-0.0001]
        mr_f=[1.44,1.44,1.44,1.44,1.44,1.44]
        mr_c=[1.44,1.44,1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.1
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26    
    elif site=='zerotrois' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002 ,-0.0001,-0.0001,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53,1.53,1.53]
        mr_c=[1.44,1.44,1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.3
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26    
    elif site=='zerodeux' :
        mi_f=[-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.003,-0.002 ,-0.0001,-0.0001,-0.0001,-0.0001]
        mr_f=[1.53,1.53,1.53,1.53,1.53,1.53]
        mr_c=[1.44,1.44,1.44,1.44,1.44,1.44]
        print mr_f
        rmodal_f=0.2
        log10var_f=0.26
        rmodal_c=1.
        log10var_c=0.26
    elif site=='BlackCarbon_CAMS':
        mi_f = [-0.20,-0.20,-0.20,-0.20,-0.20,-0.20]
        mr_f = [1.75,1.75,1.75,1.75,1.75,1.75]
        rmodal_f   = 0.0118
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Dust_CAMS':
        mi_f = [-0.006195,-0.005000,-0.004040,-0.004300,-0.004500,-0.004500]
        mr_f = [1.53,1.53,1.53,1.52,1.36,1.227]
        rmodal_f   = 0.29
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 0.29
        log10var_c = 0.3
    elif site=='SeaSalt_RH30_CAMS' :
        mi_f = [-0.000215,-0.000215,-0.000215,-0.000215,-0.000215,-0.000215]
        mr_f = [1.5156,1.5156,1.5156,1.5156,1.5156,1.5156]
        rmodal_f   = 0.1002
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.002
        log10var_c = 0.3
    elif site=='SeaSalt_RH50_CAMS' :
        mi_f = [-0.000215,-0.000215,-0.000215,-0.000215,-0.000215,-0.000215]
        mr_f = [1.5156,1.5156,1.5156,1.5156,1.5156,1.5156]
        rmodal_f   = 0.1558
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.558
        log10var_c = 0.3
    elif site=='SeaSalt_RH70_CAMS' :
        mi_f = [-0.000775,-0.000775,-0.000775,-0.000775,-0.000775,-0.000775]
        mr_f = [1.4457,1.4457,1.4457,1.4457,1.4457,1.4457]
        rmodal_f   = 0.1803
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.803
        log10var_c = 0.3
    elif site=='SeaSalt_RH80_CAMS' :
        mi_f = [-0.000643,-0.000643,-0.000643,-0.000643,-0.000643,-0.000643]
        mr_f = [1.439,1.439,1.439,1.439,1.439,1.439]
        rmodal_f   = 0.19921
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.992
        log10var_c = 0.3
    elif site=='SeaSalt_RH85_CAMS' :
        mi_f = [-0.000519,-0.000519,-0.000519,-0.000519,-0.000519,-0.000519]
        mr_f = [1.4327,1.4327,1.4327,1.4327,1.4327,1.4327]
        rmodal_f   = 0.2135
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.135
        log10var_c = 0.3
    elif site=='SeaSalt_RH90_CAMS' :
        mi_f = [-0.000390,-0.000390,-0.000390,-0.000390,-0.000390,-0.000390]
        mr_f = [1.4261,1.4261,1.4261,1.4261,1.4261,1.4261]
        rmodal_f   = 0.2366
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.366
        log10var_c = 0.3
    elif site=='SeaSalt_RH95_CAMS' :
        mi_f = [-0.000390,-0.000390,-0.000390,-0.000390,-0.000390,-0.000390]
        mr_f = [1.4261,1.4261,1.4261,1.4261,1.4261,1.4261]
        rmodal_f   = 0.2882
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.882
        log10var_c = 0.3
    elif site=='Sulfate_RH30_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.5241,1.5216,1.5189,1.5136,1.4886,1.4724]
        rmodal_f   = 0.0355
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH50_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4346,1.4322,1.4294,1.4242,1.3991,1.3830]
        rmodal_f   = 0.04331
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH70_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4148,1.4123,1.4096,1.4044,1.3793,1.3631]
        rmodal_f   = 0.04839
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH80_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4014,1.3989,1.3962,1.3909,1.3659,1.3497]
        rmodal_f   = 0.0527
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH85_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3927,1.3902,1.3875,1.3823,1.3572,1.3410]
        rmodal_f   = 0.05613
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH90_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3814,1.3789,1.3762,1.3710,1.3459,1.3297]
        rmodal_f   = 0.06149
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH95_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3645,1.3620,1.3593,1.3540,1.3290,1.3128]
        rmodal_f   = 0.07402
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH30_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.5241,1.5216,1.5189,1.5136,1.4886,1.4724]
        rmodal_f   = 0.0355
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH50_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4346,1.4322,1.4294,1.4242,1.3991,1.3830]
        rmodal_f   = 0.04331
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH70_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4148,1.4123,1.4096,1.4044,1.3793,1.3631]
        rmodal_f   = 0.04839
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH80_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4014,1.3989,1.3962,1.3909,1.3659,1.3497]
        rmodal_f   = 0.0527
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH85_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3927,1.3902,1.3875,1.3823,1.3572,1.3410]
        rmodal_f   = 0.05613
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH90_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3814,1.3789,1.3762,1.3710,1.3459,1.3297]
        rmodal_f   = 0.06149
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH95_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3645,1.3620,1.3593,1.3540,1.3290,1.3128]
        rmodal_f   = 0.07402
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    else :
        print('Mauvais site')
        sys.exit(-1)
    
            
    return bandes,bande_ref, tauRay, liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c

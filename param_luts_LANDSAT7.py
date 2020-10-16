#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes =[487, 560, 661, 831, 1644, 2197]
    tauRay =[0.17466, 0.09122,0.04629,0.01848,0.00118,0.00037]
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
        mi_f = [-0.006129,-0.005100,-0.004029,-0.004300,-0.004500,-0.004500]
        mr_f = [1.53,1.53,1.53,1.52,1.367,1.228]
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
        mr_f = [1.5241,1.5219,1.5189,1.5137,1.4894,1.4727]
        rmodal_f   = 0.0355
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH50_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4346,1.4325,1.4294,1.4243,1.3999,1.3833]
        rmodal_f   = 0.04331
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH70_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4148,1.4126,1.4096,1.4045,1.3801,1.3634]
        rmodal_f   = 0.04839
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH80_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4014,1.3992,1.3962,1.3910,1.3667,1.3500]
        rmodal_f   = 0.0527
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH85_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3927,1.3905,1.3875,1.3824,1.3580,1.3413]
        rmodal_f   = 0.05613
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH90_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3814,1.3792,1.3762,1.3711,1.3467,1.3300]
        rmodal_f   = 0.06149
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH95_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3645,1.3623,1.3593,1.3541,1.3298,1.3131]
        rmodal_f   = 0.07402
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH30_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.5241,1.5219,1.5189,1.5137,1.4894,1.4727]
        rmodal_f   = 0.0355
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH50_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4346,1.4325,1.4294,1.4243,1.3999,1.3833]
        rmodal_f   = 0.04331
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH70_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4148,1.4126,1.4096,1.4045,1.3801,1.3634]
        rmodal_f   = 0.04839
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH80_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.4014,1.3992,1.3962,1.3910,1.3667,1.3500]
        rmodal_f   = 0.0527
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH85_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3927,1.3905,1.3875,1.3824,1.3580,1.3413]
        rmodal_f   = 0.05613
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH90_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3814,1.3792,1.3762,1.3711,1.3467,1.3300]
        rmodal_f   = 0.06149
        log10var_f = 0.30
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH95_CAMS':
        mi_f = [-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00,-0.00]
        mr_f = [1.3645,1.3623,1.3593,1.3541,1.3298,1.3131]
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

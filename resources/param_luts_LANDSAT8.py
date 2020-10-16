#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as na
import sys

def param(site):

    bandes = [443, 482, 561, 654, 865, 1373, 1608, 2195]

    tauRay = [0.234445, 0.168131, 0.090062, 0.047902, 0.015506, 0.002411, 0.001284, 0.000370]
    #Calcules avec nefertiti : /home/hagolle/PROG/SMAC/Spectres/integration_rayleigh.pro

    bande_ref = 2

    liste_theta_v = na.array([0.,7.,13.])

    #Parametres definissant le modele d'aerosols
    #===========================================
    if site=='zeroun' :
        mi_f=[-0.001,-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.0003,-0.0003,-0.0002 ,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
	mr_f=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
 	mr_c=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
        rmodal_f   = 0.1
        log10var_f = 0.26
        rmodal_c   = 1.
        log10var_c = 0.26    
    elif site=='zerotrois' :
        mi_f=[-0.001,-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.0003,-0.0003,-0.0002 ,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
	mr_f=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
 	mr_c=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
        rmodal_f   = 0.3
        log10var_f = 0.26
        rmodal_c   = 1.
        log10var_c = 0.26
    elif site=='zerodeux' :
	mi_f=[-0.001,-0.001,-0.0005,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
        mi_c=[-0.0003,-0.0003,-0.0002 ,-0.0001,-0.0001,-0.0001,-0.0001,-0.0001]
	mr_f=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
	mr_c=[1.53,1.53,1.53,1.53,1.53,1.53,1.53,1.53]
        rmodal_f   = 0.2
        log10var_f = 0.26
        rmodal_c   = 1.
        log10var_c = 0.26
    elif site=='Dust_CAMS':
        mi_f = [-0.007581,-0.006294,-0.005085,-0.004106,-0.004300,-0.004500,-0.004500,-0.004500]
        mr_f = [1.5300,1.5300,1.5300,1.5300,1.5200,1.4338,1.3764,1.2288]
        rmodal_f   = 0.29
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 0.29
        log10var_c = 0.3
    elif site=='BlackCarbon_CAMS':
        #Indices CAMS cycle 46r1
        #mi_f = [-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45,-0.45]
        #Nos indices
        mi_f = [-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20]
        mr_f = [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75]
        rmodal_f   = 0.0118
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='SeaSalt_RH30_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000016,-0.000274,-0.000415,-0.001796]
        mr_f = [1.4258,1.4252,1.4231,1.4174,1.4110,1.3991,1.3924,1.3724]
        rmodal_f   = 0.1002
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.002
        log10var_c = 0.3
    elif site=='SeaSalt_RH50_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000007,-0.000151,-0.000258,-0.001547]
        mr_f = [1.3763,1.3754,1.3725,1.3691,1.3650,1.3553,1.3502,1.3258]
        rmodal_f   = 0.1558
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.558
        log10var_c = 0.3
    elif site=='SeaSalt_RH70_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000005,-0.000122,-0.000221,-0.001488]
        mr_f = [1.3651,1.3637,1.3607,1.3581,1.3544,1.3453,1.3402,1.3144]
        rmodal_f   = 0.1803
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.803
        log10var_c = 0.3
    elif site=='SeaSalt_RH80_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000004,-0.000105,-0.000199,-0.001454]
        mr_f = [1.3581,1.3567,1.3537,1.3511,1.3474,1.3394,1.3346,1.3076]
        rmodal_f   = 0.19921
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 1.992
        log10var_c = 0.3
    elif site=='SeaSalt_RH85_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000003,-0.000094,-0.000185,-0.001432]
        mr_f = [1.3537,1.3522,1.3492,1.3471,1.3434,1.3355,1.3309,1.3039]
        rmodal_f   = 0.2135
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.135
        log10var_c = 0.3
    elif site=='SeaSalt_RH90_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000002,-0.000084,-0.000172,-0.001411]
        mr_f = [1.3493,1.3477,1.3448,1.3431,1.3394,1.3316,1.3271,1.3002]
        rmodal_f   = 0.2366
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.366
        log10var_c = 0.3
    elif site=='SeaSalt_RH95_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000002,-0.000070,-0.000155,-0.001383]
        mr_f = [1.3443,1.3427,1.3398,1.3381,1.3344,1.3270,1.3231,1.2948]
        rmodal_f   = 0.2882
        log10var_f = 0.279
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = 2.882
        log10var_c = 0.3
    elif site=='Sulfate_RH30_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000059,-0.000154,-0.001682]
        mr_f = [1.5375,1.5350,1.5300,1.5252,1.5173,1.4983,1.4894,1.4633]
        rmodal_f   = 0.0212
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH50_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000063,-0.000127,-0.001019]
        mr_f = [1.4363,1.4345,1.4310,1.4276,1.4222,1.4090,1.4023,1.3770]
        rmodal_f   = 0.0259
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH70_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000063,-0.000121,-0.000884]
        mr_f = [1.4156,1.4140,1.4107,1.4077,1.4027,1.3907,1.3845,1.3594]
        rmodal_f   = 0.0289
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH80_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000064,-0.000119,-0.000816]
        mr_f = [1.4053,1.4037,1.4006,1.3977,1.3930,1.3816,1.3756,1.3506]
        rmodal_f   = 0.0315
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH85_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000064,-0.000114,-0.000700]
        mr_f = [1.3875,1.3861,1.3833,1.3806,1.3764,1.3660,1.3603,1.3355]
        rmodal_f   = 0.0335
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH90_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000065,-0.000109,-0.000584]
        mr_f = [1.3698,1.3685,1.3659,1.3635,1.3597,1.3503,1.3450,1.3204]
        rmodal_f   = 0.0367
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Sulfate_RH95_CAMS':
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000066,-0.000104,-0.000468]
        mr_f = [1.3520,1.3509,1.3486,1.3464,1.3430,1.3347,1.3297,1.3053]
        rmodal_f   = 0.0442
        log10var_f = 0.35
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH30_CAMS':
        mi_f = [-0.009793,-0.009740,-0.010271,-0.010920,-0.014406,-0.020941,-0.020874,-0.013975]
        mr_f = [1.4793,1.4788,1.4780,1.4774,1.4699,1.4611,1.4478,1.3885]
        rmodal_f   = 0.024
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH50_CAMS':
        mi_f = [-0.007710,-0.007666,-0.008046,-0.008522,-0.011100,-0.015983,-0.015961,-0.011197]
        mr_f = [1.4426,1.4418,1.4405,1.4395,1.4336,1.4253,1.4143,1.3628]
        rmodal_f   = 0.026
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH70_CAMS':
        mi_f = [-0.006005,-0.005971,-0.006267,-0.006637,-0.008645,-0.012473,-0.012468,-0.009019]
        mr_f = [1.4192,1.4183,1.4167,1.4159,1.4103,1.4027,1.3933,1.3465]
        rmodal_f   = 0.028
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH80_CAMS':
        mi_f = [-0.004860,-0.004832,-0.005071,-0.005371,-0.006996,-0.010114,-0.010120,-0.007556]
        mr_f = [1.4037,1.4028,1.4013,1.3995,1.3949,1.3872,1.3786,1.3356]
        rmodal_f   = 0.030
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH85_CAMS':
        mi_f = [-0.003989,-0.003967,-0.004171,-0.004424,-0.005791,-0.008425,-0.008436,-0.006463]
        mr_f = [1.3933,1.3921,1.3903,1.3886,1.3840,1.3767,1.3688,1.3281]
        rmodal_f   = 0.032
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH90_CAMS':
        mi_f = [-0.003311,-0.003292,-0.003456,-0.003660,-0.004767,-0.006924,-0.006946,-0.005579]
        mr_f = [1.3829,1.3815,1.3796,1.3778,1.3732,1.3664,1.3591,1.3207]
        rmodal_f   = 0.034
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='OrganicMatter_RH95_CAMS':
        mi_f = [-0.002200,-0.002188,-0.002296,-0.002432,-0.003168,-0.004636,-0.004668,-0.004160]
        mr_f = [1.3675,1.3659,1.3640,1.3622,1.3586,1.3513,1.3452,1.3098]
        rmodal_f   = 0.039
        log10var_f = 0.349
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH30_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000]
        mr_f = [1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110]
        rmodal_f   = 0.035
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH50_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000173]
        mr_f = [1.4959,1.4951,1.4939,1.4930,1.4920,1.4887,1.4869,1.4795]
        rmodal_f   = 0.042
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH70_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000578]
        mr_f = [1.4619,1.4611,1.4598,1.4581,1.4570,1.4532,1.4507,1.4407]
        rmodal_f   = 0.0455
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH80_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000595]
        mr_f = [1.4484,1.4476,1.4459,1.4450,1.4434,1.4389,1.4360,1.4257]
        rmodal_f   = 0.04725
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH85_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000644]
        mr_f = [1.4183,1.4171,1.4149,1.4141,1.4124,1.4069,1.4038,1.3910]
        rmodal_f   = 0.0525
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH90_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000677]
        mr_f = [1.3933,1.3917,1.3898,1.3881,1.3860,1.3798,1.3766,1.3623]
        rmodal_f   = 0.0595
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Nitrate_RH95_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000719]
        mr_f = [1.3669,1.3657,1.3628,1.3611,1.3590,1.3523,1.3485,1.3325]
        rmodal_f   = 0.0735
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH30_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000059,-0.000154,-0.002529]
        mr_f = [1.5375,1.5350,1.5300,1.5252,1.5173,1.4983,1.4894,1.4725]
        rmodal_f   = 0.035
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH50_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000063,-0.000127,-0.001803]
        mr_f = [1.4363,1.4345,1.4310,1.4276,1.4222,1.4090,1.4023,1.3834]
        rmodal_f   = 0.043
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH70_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000063,-0.000121,-0.001655]
        mr_f = [1.4156,1.4140,1.4107,1.4077,1.4027,1.3907,1.3845,1.3652]
        rmodal_f   = 0.048
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH80_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000064,-0.000119,-0.001580]
        mr_f = [1.4053,1.4037,1.4006,1.3977,1.3930,1.3816,1.3756,1.3561]
        rmodal_f   = 0.052
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH85_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000064,-0.000114,-0.001453]
        mr_f = [1.3875,1.3861,1.3833,1.3806,1.3764,1.3660,1.3603,1.3405]
        rmodal_f   = 0.055
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH90_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000065,-0.000109,-0.001326]
        mr_f = [1.3698,1.3685,1.3659,1.3635,1.3597,1.3503,1.3450,1.3249]
        rmodal_f   = 0.061
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    elif site=='Ammonium_RH95_CAMS' :
        mi_f = [-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000066,-0.000104,-0.001198]
        mr_f = [1.3520,1.3509,1.3486,1.3464,1.3430,1.3347,1.3297,1.3092]
        rmodal_f   = 0.073
        log10var_f = 0.3
        mr_c       = mr_f
        mi_c       = mi_f
        rmodal_c   = rmodal_f
        log10var_c = log10var_f
    else :
        print('Mauvais site')
        sys.exit(-1)
    
    return bandes,bande_ref, tauRay, liste_theta_v,rmodal_f,log10var_f,rmodal_c,log10var_c,mi_f,mi_c,mr_f,mr_c

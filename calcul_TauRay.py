#! /usr/bin/env python
# -*- coding: utf-8 -*-

from math import *
import numpy as na
import sys
import optparse
import csv
import os

###########################################################################
class OptionParser (optparse.OptionParser):
 
    def check_required (self, opt):
      option = self.get_option(opt)
 
      # Assumes the option's 'default' is set to None!
      if getattr(self.values, option.dest) is None:
          self.error("%s option not supplied" % option)
###########################################################################
#==================
#parse command line
#==================
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print '      '+sys.argv[0]+' [options]'
    print "     Aide : ", prog, " --help"
    print "        ou : ", prog, " -h"
    print "example 1 : python %s -s Sentinel-2N/MSI -i Thuillier_2012.dat -t" %sys.argv[0]
 
    sys.exit(-1)
else :
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
  
    parser.add_option("-s","--satellite", dest="satellite", action="store", type="string", \
            help="path to rep6S file for satellite",default=None)
    parser.add_option("-n","--nbands", dest="nbands", action="store", type="string", \
            help="number of bands",default=None)
    parser.add_option("-i","--irradiance", dest="irradiance", action="store", type="string", \
            help="path to irradiance file",default=None)
    parser.add_option("-t","--tab", dest="tab_delimiter", action="store_true",  \
            help="Use tab delimiter (default space)",default=False)

    (options, args) = parser.parse_args()
    
# ;---------------------------------------------------------------------------
# ;       programme de calcul de la luminance Rayleigh
# ;       integree dans une bande spectrale, et de la luminance equivalente Raylegh
# ;---------------------------------------------------------------------------
nb_bandes=int(options.nbands)
sat=options.satellite
lib_spectra = "/home/colinj/code/luts_init/lib_spectra_v20201016" # TODO: settings

if options.tab_delimiter :
    delim='\t'
else :
    delim=""

# read solar irradiance
nb_points=1000
irradiance  =na.zeros(nb_points,'Float32')
onde_soleil =na.zeros(nb_points,'Float32')
if options.irradiance != None :
    nom_irr= options.irradiance
    reader = csv.reader(open(nom_irr, 'rb'), delimiter=' ', quotechar='|')
    num=0
    for ligne in reader :
        tab=na.zeros(nb_bandes+2,'Float32')
        i=0
        for element in ligne:
            if element!='' :
                tab[i]=float(element)
                i=i+1

        onde_soleil[num]=tab[0]
        irradiance[num]=tab[1]
        num=num+1

    irradiance=irradiance[0:num]

#read  rep6S file


nb_points=1000
if options.irradiance == None :
    soleil   =na.zeros(nb_points,'Float32')
onde     =na.zeros(nb_points,'Float32')
rep_spect=na.zeros((nb_points,nb_bandes),'Float32')

instrument = ''

nom_fic= '%s/%s/rep6S.dat'% (lib_spectra, sat)
print nom_fic
reader = csv.reader(open(nom_fic, 'rb'), delimiter=delim, quotechar='|')
num=0
for ligne in reader :
    if options.irradiance == None :
        tab=na.zeros(nb_bandes+2,'Float32')
    else:
        tab=na.zeros(nb_bandes+1,'Float32')
    i=0
    for element in ligne:
	if element!='' :
	    tab[i]=float(element)
	    i=i+1

    onde[num]=tab[0]
    if options.irradiance == None :
        soleil[num]=tab[1]
        rep_spect[num,:]=tab[2:]
    else :
        rep_spect[num,:]=tab[1:]
    num=num+1

onde=onde[0:num]

rep_spect=rep_spect[0:num,:]

# clip solar irradiance wavelength domain to rep6S domain
if options.irradiance != None :
    first_wl=onde[0]
    last_wl=onde[-1]

    i_first_wl =na.nonzero(onde_soleil==first_wl)[0][0]
    i_last_wl  =na.nonzero(onde_soleil==last_wl)[0][0]
    
    soleil=irradiance[i_first_wl:i_last_wl+1]
    print soleil[0], soleil[-1]
else :
    soleil=soleil[0:num]
    
#   calcul de l'epaisseur optique selon HetT
ep_opt=0.008524/onde/onde/onde/onde*(1+0.0113/onde/onde+0.00013/onde/onde/onde/onde)
ep_opt_aero=1./onde



#   calcul de l'epaisseur optique equivalente
print 'l_equiv \t l_equiv_aero \t l_equiv_ray \t Tau_Ray'
for bande in range(nb_bandes) :
    ep_opt_0  =((ep_opt*rep_spect[:,bande]*soleil).sum())/((rep_spect[:,bande]*soleil).sum())
    onde_equiv=((onde*rep_spect[:,bande]*soleil).sum())/((rep_spect[:,bande]*soleil).sum())
    onde_equiv_aero=((onde*ep_opt_aero*rep_spect[:,bande]*soleil).sum())/((ep_opt_aero*rep_spect[:,bande]*soleil).sum())
    onde_equiv_ray=((onde*ep_opt*rep_spect[:,bande]*soleil).sum())/((ep_opt*rep_spect[:,bande]*soleil).sum())
    print "%7.5f \t %7.5f \t %7.5f \t %7.5f"%(onde_equiv,onde_equiv_aero,onde_equiv_ray,ep_opt_0)

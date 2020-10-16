# MAJA LUT Generator

## Prerequisites

This version is intended to work with :
- Python 2.7
- numpy 1.16+
- SOS 5.1

## Structure
The core components of the code are :
- calcul_TauRay.py : used to compute per band extinction coefficients. Requires a band filter function and solar irradiance.
- luts_V51.py : main program to generate a LUT for a given sensor, aerosol model, aerosol concentration volume and band id.
- trace_luts_V51.py : utility to plot a LUT in terms of TOA reflectance as a function of surface reflectance for a given band.


## Run
WARNING: The location of SOS code must be specified in an environment variable `SOS_RACINE`:

`export SOS_RACINE="/path/to/SOS/"`

### calcul_TauRay.py


`python calcul_TauRay.py -s VENUS/VSSC -n 12 -i resources/Thuillier_2012.dat -t
`
### Single band

### Launch all bands in parallel
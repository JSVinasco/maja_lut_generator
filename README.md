# MAJA LUT Generator

Author: O.Hagolle, CNES/CESBIO

Maintainer : J.Colin, CNRS/CESBIO

## 1. Prerequisites

This version is intended to work with :
- Python 2.7
- numpy 1.16+
- SOS 5.1

WARNING: The location of SOS code must be specified in an environment variable `SOS_RACINE`:

`export SOS_RACINE="/path/to/SOS/"`

## 2. Structure
### 2.1 Compute per band extinction coefficients with `calcul_TauRay.py` 
#### Requires :
- a band filter function : see `resources/lib_spectra/`
- extra-terrestrial solar irradiance : see `resources/Thuillier_2012.dat`

#### Outputs : TODO: check units
- l_equiv : equivalent radiance (W/m²/sr)
- l_equiv_aero : equivalent radiance (W/m²/sr)
- l_equiv_ray : equivalent radiance (W/m²/sr)
- Tau_Ray : optical depth for Rayleigh (-)

### 2.2 Generate the LUTs with `luts_V51.py` 
Main program to generate a LUT for a given sensor, aerosol model, aerosol concentration volume and band id. 

#### Requires :
- the definition of a given `<SENSOR>` in `resources/param_luts_<SENSOR>.py`

#### Outputs :

For a given SENSOR, AEROSOL model in a given proportion PROP for a given band, return
- `/path/to/outputs/SENSOR/albedo_V51_SENSOR_AEROSOL_prop_PROP_band_NM`
- `/path/to/outputs/SENSOR/lut_inv_V51_SENSOR_AEROSOL_prop_PROP_band_NM`
- `/path/to/outputs/SENSOR/refl_V51_SENSOR_AEROSOL_prop_PROP_band_NM`
- `/path/to/outputs/SENSOR/Tdif_V51_SENSOR_AEROSOL_prop_PROP_band_NM`
- `/path/to/outputs/SENSOR/Tdir_V51_SENSOR_AEROSOL_prop_PROP_band_NM`

Each file is provided both as binary and ASCII.

### 2.3 Plot a given LUT with `trace_luts_V51.py` 
Utility to plot a LUT in terms of TOA reflectance as a function of surface reflectance for a given band.

## 3. Launch many jobs in parallel
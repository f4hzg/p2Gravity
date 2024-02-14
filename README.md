# Tools to generate OBs for GRAVITY

## Requires: 
- numpy
- astropy, astroquery
- ruamel.yaml
- whereistheplanet (optional)
- and maybe something else?

## Install:
Make sure you have installed all the required packages, in particular ruamel.yaml

Just clone or download the repository. You should then be able to execute the script create_obs.py
```python
python p2Gravity/create_obs.py --help
```

## How to use?
We suggest to start by making a copy of one of the examples provided as a first draft of your yml. You can use the "generate" option for this:
```python
python p2Gravity/create_obs.py --generate dual_on OB_one.yml
```
"generate" can be one of dual_on, dual_off, dual_off_calib, dual_wide_off, dual_wide_on or single_on, depending on which mode you want to use.

Then edit the YML to fit your observing strategy, and once you are done, run the create_obs.py script to convert it to OBs on P2:
```python
python p2Gravity/create_obs.py OB_one.yml
```

You will be asked to provide your P2 credentials, and a summary plot of each OB will displayed. Just click on one of the upper right buttons to send it to P2 or cancel. 

If you don´t want to be bothered with the plots, use the --nogui option:
```python
python p2Gravity/create_obs.py OB_one.yml --nogui
```
The OBs will be uploaded to P2 without further verification.

For a quick access to the "optimal DIT selection figures" from the template manual, try:
```python
python p2Gravity/create_obs.py --dit
```

If you want to upload a dummy OB on the demo P2 server, just for testing, just generate one, and use the --demo keyword. 
```python
python p2Gravity/create_obs.py --generate dual_on  kenobi.yml
python p2Gravity/create_obs.py kenobi.yml --demo
```

Be aware that the P2 demo server is *PUBLICLY* available here:
[P2 demo server](https://www.eso.org/p2demo/).

## Time constraints

Absolute time constrains can be added to the OBs by providing a list of (from, to) tuple in the yml description of the setup. Here is an example for a setup requesting observations only in September (2020 or 2021):

``` yaml
setup:
  run_id: 60.A-9252(M)         # id of the run to upload the OB in the correct place
  date: 2023-07-14             # Required. But only useful if 'whereistheplanet' is used to predict position of the companion
  folder: P2GRAVITY_examples   # Folder in P2 where the OB will be uploaded. 
  INS.SPEC.RES: "HIGH"         # spectral resolution. LOW, MED, or HIGH
  INS.SPEC.POL: "OUT"          # Polarisation. OUT or IN
  ISS.BASELINE: ["UTs"]        # baselines (small, large, or UTs)
  ISS.VLTITYPE: ["astrometry"] # snapshot, imaging, time-series, or astrometry
  SEQ.MET.MODE: FAINT          # the mode for the metrology laser. Can be FAINT, ON, or OFF  
  concatenation: none          # if not none, a concatenation with this name will be created and all OBs put in here
  constraints:                 # additional constraints
    skyTransparency: "Variable, thin cirrus" 
    airmass: 1.6
    moonDistance: 10
    atm: 85%
  absoluteTimeConstraints:
    - ['2020-09-01T00:00', '2020-09-30T23:59']
    - ['2021-09-01T00:00', '2021-09-30T23:59']
```


## Optional arguments:

--help to print the doc message and exit

--dit to show a plot form the template manual for optimal dit selection

--demo to run in demo mode and upload OBs to P2 demo server

--nogui to skip the plot and confirmation part (OB directly uploaded to P2)

--fov x to increase the fov in the plot

--bg path/to/image to add an image to the background of the plot

--generate xx to quickly generate a first yml

and more! For further details:
```python
create_obs.py --help
```

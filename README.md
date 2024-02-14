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

Absolute time constrains can be added on a OB per OB basis. This is done by adding a list of (from, to) tuple in the OB yml description. For example:

``` yaml
ObservingBlocks:
  OB1_with_ATC:
    description: An OB in with Absolute Time Constraints
    utctime:
      - ['2024-11-25T00:00', '2024-11-28T23:59']
      - ['2024-12-23T00:00', '2024-12-30T23:59']        
    # and the rest follows the usual format
    mode: dual_on
#    etc.
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

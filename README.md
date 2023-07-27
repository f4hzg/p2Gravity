# Tools to generate OBs for GRAVITY

## Requires: 
- numpy
- astropy, astroquery
- ruamel.yaml (optional)
- whereistheplanet (optional)
- and maybe something else?

## How to use?
Simply run the create_obs.py script with your yml file describing the OBs:
```python
create_obs.py file=path/to/yml
```

Examples YML files for different modes and observation types are available in the example directory.

## Optional arguments:
--help to print the doc massage and exit

--dit to show a plot form the template manual for optimal dit selection

--demo to run in demo mode and upload OBs to P2 demo server

--nogui to skip the plot and confirmation part (OB directly uploaded to P2)

fov=x to increase the fov in the plot

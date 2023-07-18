Tools to generate OBs for GRAVITY

Requires: 
- numpy
- astropy, astroquery
- ruamel.yaml (optional)
- whereistheplanet (optional)
- and maybe something else?

How to use?
Simply run the create_obs.py script with your yml file describing the OBs:
create_obs.py file=path/to/yml

Optional arguments are:
--demo to run in demo mode and upload OBs to P2 demo server
--nogui to skip the plot and confirmation part (OB directly uploaded to P2)
fov=x to increase the fov in the plot

Examples YML files for different modes and observation types are available in the example directory.

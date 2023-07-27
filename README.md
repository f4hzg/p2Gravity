# Tools to generate OBs for GRAVITY

## Requires: 
- numpy
- astropy, astroquery
- ruamel.yaml (optional)
- whereistheplanet (optional)
- and maybe something else?

## How to use?
We suggest to start by making a copy of one of the examples provided as a first draft of your yml. You can use the "generate" option for this:
```python
create_obs.py generate=dual_on file=path/to/output/yml
```
"generate" can be one of dual_on, dual_off, dual_off_calib, dual_wide_off, dual_wide_on or single_on.

Then edit the YML to fit your observing strategy, and once you are done, run the create_obs.py script to convert it to OBs on P2:
```python
create_obs.py file=path/to/yml
```

You will be asked to provide your P2 credentials, and a summary plot of each OB will displayed. Just click on one of the upper right buttons to send it to P2 or cancel. 

If you don´t want to be bothered with the plots, use the --nogui option:
```python
create_obs.py file=path/to/yml --nogui
```
The OBs will be uploaded to P2 without further verification.

## Optional arguments:
--help to print the doc massage and exit

--dit to show a plot form the template manual for optimal dit selection

--demo to run in demo mode and upload OBs to P2 demo server

--nogui to skip the plot and confirmation part (OB directly uploaded to P2)

fov=x to increase the fov in the plot

bg=path/to/image to add an image to the background of the plot

generate=xx to quickly generate a first yml

and more! For further details:
```python
create_obs.py --help
```

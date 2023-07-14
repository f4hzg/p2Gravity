#coding: utf8
"""Generate and send GRAVITY OBs to P2

The create_obs script is used to generate GRAVITY OBs and send them to P2
To use this script, you need to call it with a YML file, see example below.

Args:
  file (str): the path the to YAML file describing the OBs.
  fov (int, optional): field-of-view to show in the plots. Default to 10*fiver_fov
  demo (bool, optional): if set, send the OBs to the P2 demo server
  nogui (bool, optional): if set, do not plot a visual summary of the OBs before sending to P2, but send them without warning

Examples:
  python create_obs file=path/to/obs.yml --demo
  python create_obs file=path/to/obs.yml --nogui --demo 

Authors:
  M. Nowak, and the exoGravity team.

Version:
  0.1
"""

# import ESO P2 api and getpass to manage user password
import p2api
from getpass import getpass

# ruamel is used to load the yml
import ruamel.yaml as yaml

# import this package
import p2Gravity as p2g
from p2Gravity.common import *
from p2Gravity.plot import *

# import sys for args
import sys

# load aguments into a dictionnary
dargs = args_to_dict(sys.argv)

if "help" in dargs.keys():
    print(__doc__)
    sys.exit()
    
# arg should be the path to the yml file    
REQUIRED_ARGS = ["file"]
for req in REQUIRED_ARGS:
    if not(req in dargs.keys()):
        printerr("Argument '"+req+"' is not optional for this script. Required args are: "+', '.join(REQUIRED_ARGS))

if "fov" in dargs:
    fov = int(dargs["fov"])
else:
    fov = None
        
if "nogui" in dargs:
    nogui = dargs["nogui"]
else:
    nogui = False

if "demo" in dargs:
    demo = dargs["demo"]
else:
    demo = False

if demo:
    # setup for testing on P2 demo server
    api = p2api.ApiConnection('demo', 52052, "tutorial")
else:
    user = input("ESO P2 username: ")
    password = getpass("ESO P2 password: ")
    api = p2api.ApiConnection('production', user, password)
    
# get filename and load yml
filename = dargs["file"]    
cfg = yaml.load(open(filename, "r"), Loader=yaml.RoundTripLoader)

# Create OB
run_id = cfg["setup"]["run_id"]
folder_name = cfg["setup"]["folder"]
date = cfg["setup"]["date"]

# loop through all OBs
for ob_name in cfg["ObservingBlocks"]:
    ob = cfg["ObservingBlocks"][ob_name]
    mode = ob["mode"]
    if mode == "single_on":
        p2ob = p2g.ob.SingleOnOb(ob, cfg["setup"], label = ob_name)
    if mode == "single_off":
        p2ob = p2g.ob.SingleOffOb(ob, cfg["setup"], label = ob_name)
    if mode == "dual_on":
        p2ob = p2g.ob.DualOnOb(ob, cfg["setup"], label = ob_name)
    if mode == "dual_off":
        p2ob = p2g.ob.DualOffOb(ob, cfg["setup"], label = ob_name)
    p2ob.generate_templates()
    p2ob.simbad_resolve(ob["target"])
    # in nogui mode, we upload straight to p2    
    if nogui:
        p2ob.p2_create(api, run_id, folder_name)
        p2ob.p2_update(api)
    # in gui mode, we lpot the OB and wait for user input
    else:
        def send_p2(event, fig):
            p2ob.p2_create(api, run_id, folder_name)
            p2ob.p2_update(api)
            printinf("OB {} sent to run {}".format(ob_name, run_id))
            plt.close(fig)
            return None
        def cancel(event, fig):
            printwar("OB {} was not sent to P2".format(ob_name))
            plt.close(fig)
            return None
        # plot this OB
        fig, gs = plot_ob(p2ob, title = "run: {}    folder: {}    ob: {}    date: {}".format(run_id, folder_name, ob_name, date), fov=fov)
        # add buttons:
        axConfirm = fig.add_subplot(gs[0, 4])
        axCancel = fig.add_subplot(gs[0, 5])
        bConfirm = Button(axConfirm, 'Send to P2', color="C2")
        bCancel = Button(axCancel, 'Cancel', color="C3")
        bConfirm.on_clicked(lambda event: send_p2(event, fig))
        bCancel.on_clicked(lambda event: cancel(event, fig))
        plt.show() # wait for the user to confirm sending or cancel

printinf("Done")

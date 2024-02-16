#coding: utf8
"""A class inherinting from ObservingBlock to define a dual field off-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock

# import re to properly split swap in sequence
import re

import numpy as np

import math

# to resolve planet position
try:
    import whereistheplanet
    WHEREISTHEPLANET = True    
except:
    common.printwar("Cannot load whereistheplanet module. 'whereistheplanet' will not be available as a coord_syst.")
    WHEREISTHEPLANET = False    


class DualOffOb(ObservingBlock):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        super(DualOffOb, self).__init__(*args, **kwargs)
        self.ob_type = "DualOffOb"
        return None

    def _generate_acquisition(self):
        """
        create the acquisition attribute using the appropriate acquisition type and Automatically populate the fields
        the setup dict attribute will also by used to bypass some default values if required
        """        
        self.acquisition = tpl.DualOffAxisAcq()
        self._fill_magnitudes(self.yml)
        # set target names
        if "ft_target" in self.yml:
            self.acquisition["SEQ.FT.ROBJ.NAME"] = self.yml["ft_target"]
        else:
            if not("target" in self.yml):
                printerr("No 'target' specified in ObservingBlocks")
            self.acquisition["SEQ.FT.ROBJ.NAME"] = self.yml["target"]
        if "sc_target" in self.yml:
            self.acquisition["SEQ.INS.SOBJ.NAME"] = self.yml["sc_target"]
        else:
            if not("target" in self.yml):
                printerr("No 'target' specified in ObservingBlocks")                        
            self.acquisition["SEQ.INS.SOBJ.NAME"] = self.yml["target"]
        # use the mean of templates to set the direction of acquisition
        dx = np.array([tpl["SEQ.RELOFF.X"][0] for tpl in self.templates if tpl.template_name == "GRAVITY_dual_obs_exp"]).mean()
        dy = np.array([tpl["SEQ.RELOFF.Y"][0] for tpl in self.templates if tpl.template_name == "GRAVITY_dual_obs_exp"]).mean()
        self.acquisition["SEQ.INS.SOBJ.X"] = round(dx/np.sqrt(dx**2+dy**2), 2) # 1 mas total sep
        self.acquisition["SEQ.INS.SOBJ.Y"] = round(dy/np.sqrt(dx**2+dy**2), 2)                                           
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        self.acquisition.populate_from_yml(self.yml)
        if "coord_syst" in self.yml:
            if self.yml["coord_syst"] == "radec":
                self.acquisition["SEQ.INS.SOBJ.X"] = round(self.yml["coord"][0], 2)
                self.acquisition["SEQ.INS.SOBJ.Y"] = round(self.yml["coord"][1], 2)
            elif self.yml["coord_syst"] == "pasep":
                pa, sep = self.yml["coord"]
                ra, dec = math.sin(pa/180*math.pi)*sep, math.cos(pa/180.0*math.pi)*sep
                self.acquisition["SEQ.INS.SOBJ.X"] = round(ra, 2)
                self.acquisition["SEQ.INS.SOBJ.Y"] = round(dec, 2)
            elif self.yml["coord_syst"] == "whereistheplanet":
                if WHEREISTHEPLANET:
                    common.printinf("Resolution of {} with whereistheplanet:".format(self.yml["coord"]))
                    ra, dec, sep, pa = whereistheplanet.predict_planet(self.yml["coord"], self.setup["date"])
                    self.acquisition["SEQ.INS.SOBJ.X"] = round(ra[0], 2)
                    self.acquisition["SEQ.INS.SOBJ.Y"] = round(dec[0], 2)                  
                else: 
                    common.printerr("whereistheplanet used as a coord_syst, but whereistheplanet module could not be loaded")
            else:
                common.printerr("Unknown coordinate system {}".format(self.yml["coord_syst"]))
        return None

    def _generate_template(self, obj_yml, exposures, reloff_x = None, reloff_y = None):
        """
        generate the template from the given yml dict and exposure 
        """        
        if exposures == "swap":
            template = tpl.DualObsSwap()            
            template.populate_from_yml(self.yml)
            template.populate_from_yml(obj_yml)            
        else:
            template = tpl.DualObsExp(iscalib = self.iscalib)
            template.populate_from_yml(self.yml)            
            template.populate_from_yml(obj_yml)
            template["SEQ.OBSSEQ"] = exposures            
            if not(reloff_x is None):
                template["SEQ.RELOFF.X"] = reloff_x
            if not(reloff_y is None):                
                template["SEQ.RELOFF.Y"] = reloff_y
        return template

    def generate_templates(self):
        """
        generate the sequence of templates corresponding to the OB. Nothing is send to P2 at this point
        """
        # split sequences on swaps:
        sequences = []
        for seq in self.yml["sequence"]:
            for dummy in re.split("\W(swap)", seq.rstrip().lstrip()):
                sequences.append(dummy)
        for seq in sequences:
            exposures = seq.rstrip().lstrip().split(" ")
            if exposures == ["swap"]: # no test in this case
                self.templates.append(self._generate_template(obj_yml, "swap"))
            else:
                if not("sky" in exposures):
                    common.printwar("No sky in sequence {} in OB '{}'".format(exposures, self.label))
                reloff_x = []
                reloff_y = []
                exposures_ESO = ""                
                for exposure in exposures:
                    if exposure.lower() == "sky":
                        reloff_x.append(0)
                        reloff_y.append(0)
                        exposures_ESO = exposures_ESO + " S"
                    else:
                        if not(exposure  in self.objects):
                            printerr("Object with label {} from sequence not found in yml".format(exposure))
                        obj_yml = self.objects[exposure]
                        if "coord_syst" in obj_yml:
                            if obj_yml["coord_syst"] == "radec":
                                reloff_x.append(round(obj_yml["coord"][0], 2))
                                reloff_y.append(round(obj_yml["coord"][1], 2))                          
                            elif obj_yml["coord_syst"] == "pasep":
                                pa, sep = obj_yml["coord"]
                                ra, dec = math.sin(pa/180*math.pi)*sep, math.cos(pa/180.0*math.pi)*sep
                                reloff_x.append(round(obj_yml["coord"][0], 2))
                                reloff_y.append(round(obj_yml["coord"][1], 2))
                            elif obj_yml["coord_syst"] == "whereistheplanet":
                                if WHEREISTHEPLANET:
                                    common.printinf("Resolution of {} with whereistheplanet:".format(obj_yml["coord"]))
                                    ra, dec, sep, pa = whereistheplanet.predict_planet(obj_yml["coord"], self.setup["date"])
                                    reloff_x.append(round(obj_yml["coord"][0], 2))
                                    reloff_y.append(round(obj_yml["coord"][1], 2))                                                                   
                                else: 
                                    common.printerr("whereistheplanet used as a coord_syst, but whereistheplanet module could not be loaded")
                            else:
                                common.printerr("Unknown coordinate system {}".format(obj_yml["coord_syst"]))
                        else:
                            reloff_x.append(0.)
                            reloff_y.append(0.)                            
                        # add the exposure in the ESO format
                        exposures_ESO = exposures_ESO + " O"
                        # don't forget that these offsets are cumulative, so we need to
                        # remove the previous cumsum from each newly calculated offset
                        reloff_x[-1] = reloff_x[-1] - np.sum(np.array(reloff_x[:-1]))
                        reloff_y[-1] = reloff_y[-1] - np.sum(np.array(reloff_y[:-1]))
                self.templates.append(self._generate_template(obj_yml, exposures_ESO, reloff_x = reloff_x, reloff_y = reloff_y))                
        # now we can generate acquisition                
        self._generate_acquisition()
        return None
            


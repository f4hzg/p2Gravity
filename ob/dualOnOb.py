#coding: utf8
"""A class inherinting from ObservingBlock to define a dual field on-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock
import numpy as np

import math

# to resolve planet position
try:
    import whereistheplanet
    WHEREISTHEPLANET = True    
except:
    common.printwar("Cannot load whereistheplanet module. 'whereistheplanet' will not be available as a coord_syst.")
    WHEREISTHEPLANET = False    


class DualOnOb(ObservingBlock):    
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        super(DualOnOb, self).__init__(*args, **kwargs)
        self.ob_type = "DualOnOb"        
        return None

    def _generate_acquisition(self):
        """
        create the acquisition attribute using the appropriate acquisition type and Automatically populate the fields
        the setup dict attribute will also by used to bypass some default values if required
        """
        self.acquisition = tpl.DualOnAxisAcq()
        # set target names
        if "ft_target" in self.yml:
            self.acquisition["SEQ.FT.ROBJ.NAME"] = self.yml["ft_target"]
        else:
            if not("target" in self.yml):
                common.printerr("No 'target' specified in ObservingBlock")
            self.acquisition["SEQ.FT.ROBJ.NAME"] = self.yml["target"]
        if "sc_target" in self.yml:
            self.acquisition["SEQ.INS.SOBJ.NAME"] = self.yml["sc_target"]
        else:
            if not("target" in self.yml):
                common.printerr("No 'target' specified in ObservingBlock")                        
            self.acquisition["SEQ.INS.SOBJ.NAME"] = self.yml["target"]
        # use the mean of templates to set the direction of acquisition
        dx = np.array([tpl["SEQ.RELOFF.X"][0] for tpl in self.templates]).mean()
        dy = np.array([tpl["SEQ.RELOFF.Y"][0] for tpl in self.templates]).mean()
        self.acquisition["SEQ.INS.SOBJ.X"] = round(dx/np.sqrt(dx**2+dy**2), 2) # 1 mas total sep
        self.acquisition["SEQ.INS.SOBJ.Y"] = round(dy/np.sqrt(dx**2+dy**2), 2)
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        return None

    def _generate_template(self, obj_yml, exposures):
        """
        geneate the template from the given yml dict and exposure 
        """
        template = tpl.DualObsExp()        
        if "coord_syst" in obj_yml:
            if obj_yml["coord_syst"] == "radec":
                template["SEQ.RELOFF.X"] = [round(obj_yml["coord"][0], 2)]
                template["SEQ.RELOFF.Y"] = [round(obj_yml["coord"][1], 2)]
            elif obj_yml["coord_syst"] == "pasep":
                pa, sep = obj_yml["coord"]
                ra, dec = math.sin(pa/190.8*math.pi)*sep, math.cos(pa/190.8*math.pi)*sep
                template["SEQ.RELOFF.X"] = [round(ra, 2)]
                template["SEQ.RELOFF.Y"] = [round(dec, 2)]
            elif obj_yml["coord_syst"] == "whereistheplanet":
                if WHEREISTHEPLANET:
                    common.printinf("Resolution of {} with whereistheplanet:".format(obj_yml["coord"]))
                    ra, dec, sep, pa = whereistheplanet.predict_planet(obj_yml["coord"], self.setup["date"])
                    template["SEQ.RELOFF.X"] = [round(ra[0], 2)]
                    template["SEQ.RELOFF.Y"] = [round(dec[0], 2)]                    
                else: 
                    common.printerr("whereistheplanet used as a coord_syst, but whereistheplanet module could not be loaded")
            else:
                common.printerr("Unknown coordinate system {}".format(obj_yml["coord_syst"]))        
        template.populate_from_yml(obj_yml)
        template["SEQ.OBSSEQ"] = exposures
        return template

    def generate_templates(self):
        """
        generate the sequence of templates corresponding to the OB. Nothing is send to P2 at this point
        """
        for seq in self.yml["sequence"]:
            exposures = seq.split()
            if not("sky" in exposures):
                common.printwar("No sky in sequence {} in OB '{}'".format(exposures, self.label))
            if len(set([dummy for dummy in exposures if dummy != "sky"])) > 1: # number of object different from sky
                common.printerr("Sequence '{}' in OB '{}' contains more than one object".format(exposures, self.label))
            obj_label = [dummy for dummy in exposures if dummy != "sky"][0]
            if not(obj_label in self.objects):
                common.printerr("Exposure '{}' in OB '{}' does not match any of the objects".format(obj_label, self.label))
            obj_yml = self.objects[obj_label]
            dummy_label = "£££"
            exposures = " ".join(exposures).replace("sky", dummy_label).replace(obj_label, "O").replace(dummy_label, "S") # exposure in ESO format
            self.templates.append(self._generate_template(obj_yml, exposures))
        # now we can generate acquisition
        self._generate_acquisition()
        return None
            


#coding: utf8
"""A class inherinting from ObservingBlock to define a dual field on-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock
import numpy as np

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
        self._fill_magnitudes(self.yml)        
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
        # use the mean of first position of templates to set the direction of acquisition
        dx = np.array([tpl["SEQ.RELOFF.X"][0] for tpl in self.templates]).mean()
        dy = np.array([tpl["SEQ.RELOFF.Y"][0] for tpl in self.templates]).mean()
        self.acquisition["SEQ.INS.SOBJ.X"] = round(dx/np.sqrt(dx**2+dy**2), 2) # 1 mas total sep
        self.acquisition["SEQ.INS.SOBJ.Y"] = round(dy/np.sqrt(dx**2+dy**2), 2)
        # now we need to remove the acq position from the first element of each templates
        for template in self.templates:
            template["SEQ.RELOFF.X"][0] = template["SEQ.RELOFF.X"][0] - self.acquisition["SEQ.INS.SOBJ.X"]
            template["SEQ.RELOFF.Y"][0] = template["SEQ.RELOFF.Y"][0] - self.acquisition["SEQ.INS.SOBJ.Y"]            
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        return None

    def _generate_template(self, exposures):
        """
        geneate the template from the given yml dict and exposure 
        """
        template = tpl.DualObsExp(iscalib = self.iscalib)
        template.populate_offsets_from_object_yml(exposures, self.objects, date = self.setup["date"])
        return template

    def generate_templates(self):
        """
        generate the sequence of templates corresponding to the OB. Nothing is send to P2 at this point
        """
        for seq in self.yml["sequence"]:
            exposures = seq.split()
            if not("sky" in exposures):
                common.printwar("No sky in sequence {} in OB '{}'".format(exposures, self.label))
            if len(set([dummy for dummy in exposures if dummy != "sky"])) > 1: # more than one object which is not sky
                if len(set([self.objects[dummy]["DET2.DIT"] for dummy in exposures if dummy != "sky"])) > 1 : # check if all dits are the same
                    common.printerr("Sequence '{}' in OB '{}' contains objects with different DET2.DIT. Please split them on different lines.".format(exposures, self.label))
                if len(set([self.objects[dummy]["DET2.NDIT.SKY"] for dummy in exposures if dummy != "sky"])) > 1 : # check if all dits are the same
                    common.printerr("Sequence '{}' in OB '{}' contains objects with different DET2.NDIT.SKY.. Please split them on different lines.".format(exposures, self.label))
                if len(set([self.objects[dummy]["DET2.NDIT.OBJECT"] for dummy in exposures if dummy != "sky"])) > 1 : # check if all dits are the same
                    common.printerr("Sequence '{}' in OB '{}' contains objects with different DET2.NDIT.OBJECT. Please split them on different lines.".format(exposures, self.label))
            self.templates.append(self._generate_template(exposures))
        # now we can generate acquisition
        self._generate_acquisition()
        return None
            


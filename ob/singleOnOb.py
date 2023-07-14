#coding: utf8
"""A class inherinting from ObservingBlock to define a single field on-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock

class SingleOnOb(ObservingBlock):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """
        super(SingleOnOb, self).__init__(*args, **kwargs)
        self.ob_type = "SingleOnOb"        
        return None

    def _generate_acquisition(self):
        """
        create the acquisition attribute using the appropriate acquisition type and Automatically populate the fields
        the setup dict attribute will also by used to bypass some default values if required
        """
        self.acquisition = tpl.SingleOnAxisAcq()
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
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        return None

    def _generate_template(self, obj_yml, exposures):
        """
        geneate the template from the given yml dict and exposure 
        """
        template = tpl.SingleObsExp()
        template.populate_from_yml(self.objects["star"])            
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
            obj_yml = self.objects["star"]
            exposures = " ".join(exposures).replace("star", "O").replace("sky", "S") # exposure in ESO format
            self.templates.append(self._generate_template(obj_yml, exposures))
        # now we can generate acquisition
        self._generate_acquisition()
        return None

    

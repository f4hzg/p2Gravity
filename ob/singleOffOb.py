#coding: utf8
"""A class inherinting from ObservingBlock to define a single field off-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock

class SingleOffOb(ObservingBlock):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        super(SingleOffOb, self).__init__(*args, **kwargs)
        self.ob_type = "SingleOffOb"                
        return None

    def _generate_acquisition(self):
        """
        create the acquisition attribute using the appropriate acquisition type and Automatically populate the fields
        the setup dict attribute will also by used to bypass some default values if required
        """        
        self.acquisition = tpl.SingleOffAxisAcq()
        self.acquisition["SEQ.FT.ROBJ.NAME"] = self.objects["star"]["name"]
        first_object_label = [object_label for object_label in self.objects if object_label != "star"][0]
        self.acquisition["SEQ.INS.SOBJ.NAME"] = self.objects[first_object_label]["name"]
        # use the first template to set the coodinates
        first_non_star_label = [o for o in self.objects if o != "star"][0]
        first_non_star_index = [o for o in self.objects].index(first_non_star_label)
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        self.acquisition.populate_from_yml(self.objects["star"])                
        return None

    def _generate_template(self, obj_yml, exposures):
        """
        geneate the template from the given yml dict and exposure 
        """        
        template = tpl.SingleObsExp()
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
            exposures = " ".join(exposures).replace(obj_label, "O").replace("sky", "S") # exposure in ESO format
            self.templates.append(self._generate_template(obj_yml, exposures))
        # now we can generate acquisition
        self._generate_acquisition()
        return None
            


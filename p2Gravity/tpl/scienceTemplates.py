#coding: utf8
from .template import Template
from .. import common

import numpy as np

# to resolve planet position
try:
    import whereistheplanet
    WHEREISTHEPLANET = True    
except:
    common.printwar("Cannot load whereistheplanet module. 'whereistheplanet' will not be available as a coord_syst.")
    WHEREISTHEPLANET = False    


class ScienceTemplate(Template): 
    def __init__(self, *args, **kwargs):
        """
        This is the generic class of a science tamplate, with all fields common to all templates
        (except SWAP, which is a weird one)
        """
        super(ScienceTemplate, self).__init__(*args, **kwargs)
        self.template_name = None
        self.template_type = 'science'
        self["DET2.DIT"] = 0.3
        self["DET2.NDIT.OBJECT"] = 16
        self["DET2.NDIT.SKY"] = 16
        self["DET2.NDIT.SKY.X"] = 2000
        self["DET2.NDIT.SKY.Y"] = 2000
        self["SEQ.HWPOFF"] = [0]
        self["SEQ.OBSSEQ"] = "O S"
        return None

class DualObsSwap(Template):
    """
    GRAVITY_dual_obs_swap template (science)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE -- Auto 1 2 7 9 (Auto) -- FringeTracker mode
    """
    def __init__(self, *args, **kwargs):
        super(DualObsSwap, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_dual_obs_swap'
        self.template_type = 'science'
        self["SEQ.FT.MODE"] = "AUTO"
        return None
    
    def populate_from_yml(self, yml):
        if "SEQ.FT.MODE" in yml:
            self["SEQ.FT.MODE"] = yml["SEQ.FT.MODE"]
        return None

class SingleObsExp(ScienceTemplate):
    """
    GRAVITY_single_obs_exp template (science)
    Parameter -- Range (Default) -- Desciption
    DET2.DIT -- 0.3, 1, 3, 5, 10, 30, 60 (0.3) -- SC frame integration time (DIT in s)
    DET2.NDIT.OBJECT -- 10...300 (25) -- Number of science target frames (NDIT)
    DET2.NDIT.SKY -- -10...300 (25) -- Number of sky frames (NDIT)
    SEQ.HWPOFF -- -180...180 (0.0) -- Sequence of HWP offsets (deg)
    SEQ.SKY.X -- -4000...4000 (2000) -- Sky offset in RA (mas).
    SEQ.SKY.Y -- -4000...4000 (2000) -- Sky offset in DEC (mas).
    SEQ.OBSSEQ -- O S (O S) -- Observing sequence of science (O) and sky (S) exposures.
    """
    def __init__(self, iscalib = False, *args, **kwargs):
        super(SingleObsExp, self).__init__(*args, **kwargs)
        if iscalib:
            self.template_name = 'GRAVITY_single_obs_calibrator'
            self.template_type = 'calib'
        else:
            self.template_name = 'GRAVITY_single_obs_exp'
            self.template_type = 'science'          
        return None

    def populate_from_yml(self, yml):
        super(SingleObsExp, self).populate_from_yml(yml)            
        return None    

class DualObsExp(ScienceTemplate):
    """
    GRAVITY_dual_obs_exp template (science)
    Parameter -- Range (Default) -- Desciption
    DET2.DIT -- 0.3, 1, 3, 5, 10, 30, 60 (0.3) -- SC frame integration time (DIT in s)
    DET2.NDIT.OBJECT -- 10...300 (25) -- Number of science target frames (NDIT)
    DET2.NDIT.SKY -- -10...300 (25) -- Number of sky frames (NDIT)
    SEQ.RELOFF.X -- -1000...1000 (0.0) -- Sequence of SC relative RA offsets (mas)
    SEQ.RELOFF.Y -- -1000...1000 (0.0) -- Sequence of SC relative DEC offsets (mas)
    SEQ.HWPOFF -- -180...180 (0.0) -- Sequence of HWP offsets (deg)
    SEQ.SKY.X -- -4000...4000 (2000) -- Sky offset in RA (mas).
    SEQ.SKY.Y -- -4000...4000 (2000) -- Sky offset in DEC (mas).
    SEQ.OBSSEQ -- O S (O S) -- Observing sequence of science (O) and sky (S) exposures.
    """
    def __init__(self, iscalib = False, *args, **kwargs):
        super(DualObsExp, self).__init__(*args, **kwargs)
        if iscalib:
            self.template_name = 'GRAVITY_dual_obs_calibrator'
            self.template_type = 'calib'
        else:
            self.template_name = 'GRAVITY_dual_obs_exp'
            self.template_type = 'science'          
        self["SEQ.RELOFF.X"] = [0]
        self["SEQ.RELOFF.Y"] = [0]
        return None

    def populate_offsets_from_object_yml(self, exposures, objects_yml, date = None):
        """
        Calculate the correct expoure sequence (ESO format) and relative offsets
        from a list like "A B A B" and a dict of object ymls {"A": yml, "B": yml}
        """
        # clear offsets and exposures
        print(exposures)
        self["SEQ.RELOFF.X"] = []
        self["SEQ.RELOFF.Y"] = []
        exposures_ESO = "" 
        # loop through exposures
        for exposure in exposures:
            # if sky, set offset to 0 (skyoffset is used instead)
            if exposure.lower() == "sky":
                self["SEQ.RELOFF.X"].append(0.)
                self["SEQ.RELOFF.Y"].append(0.)                                                
                exposures_ESO = exposures_ESO + " S"
            else:
                if not(exposure in objects_yml):
                    common.printerr("Object with label {} from sequence not found in yml".format(exposure))                
                obj_yml = objects_yml[exposure]
                if "coord_syst" in obj_yml:
                    if obj_yml["coord_syst"] == "radec":
                        self["SEQ.RELOFF.X"].append(round(obj_yml["coord"][0], 2))
                        self["SEQ.RELOFF.Y"].append(round(obj_yml["coord"][1], 2))
                    elif obj_yml["coord_syst"] == "pasep":
                        pa, sep = obj_yml["coord"]
                        ra, dec = np.sin(np.deg2rad(pa))*sep, np.cos(np.deg2rad(pa))*sep
                        self["SEQ.RELOFF.X"].append(round(ra, 2))
                        self["SEQ.RELOFF.Y"].append(round(dec, 2))
                    elif obj_yml["coord_syst"] == "whereistheplanet":
                        if WHEREISTHEPLANET:
                            common.printinf("Resolution of {} with whereistheplanet:".format(obj_yml["coord"]))
                            if date is None:
                                raise Exception("Date not given for Resolution of {} with whereistheplanet:".format(obj_yml["coord"]))                                
                            ra, dec, sep, pa = whereistheplanet.predict_planet(obj_yml["coord"], date)
                            self["SEQ.RELOFF.X"].append(round(ra[0], 2))
                            self["SEQ.RELOFF.Y"].append(round(dec[0], 2))
                        else: 
                            common.printerr("whereistheplanet used as a coord_syst, but whereistheplanet module could not be loaded")
                    else:
                        common.printerr("Unknown coordinate system {}".format(obj_yml["coord_syst"]))
                else:
                    self["SEQ.RELOFF.X"].append(0.)
                    self["SEQ.RELOFF.Y"].append(0.)  
                # add the exposure in the ESO format
                exposures_ESO = exposures_ESO + " O"                            
                # don't forget that these offsets are cumulative, so we need to
                # remove the previous cumsum from each newly calculated offset
                self["SEQ.RELOFF.X"][-1] = self["SEQ.RELOFF.X"][-1] - np.sum(np.array(self["SEQ.RELOFF.X"][:-1]))
                self["SEQ.RELOFF.Y"][-1] = self["SEQ.RELOFF.Y"][-1] - np.sum(np.array(self["SEQ.RELOFF.Y"][:-1]))
                self.populate_from_yml(obj_yml)
        print(self)
        self["SEQ.OBSSEQ"] = exposures_ESO
        return None

    def populate_from_yml(self, yml):
        super(DualObsExp, self).populate_from_yml(yml)            
        return None

    

#coding: utf8
from .template import Template
from .. import common

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

    def populate_from_yml(self, yml):
        super(DualObsExp, self).populate_from_yml(yml)            
        return None

    

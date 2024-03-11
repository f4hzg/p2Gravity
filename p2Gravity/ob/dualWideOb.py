#coding: utf8
"""A class inherinting from DualOffOb to define a Gwide dual field off-axis OB in all its glorious specificity
"""

from .. import tpl
from .. import common
from .observingBlock import ObservingBlock
from .dualOffOb import DualOffOb
from .dualOnOb import DualOnOb

# we need astroquery to get magnitudes, coordinates, etc.
from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord

import math

# to resolve planet position
try:
    import whereistheplanet
    WHEREISTHEPLANET = True    
except:
    common.printwar("Cannot load whereistheplanet module. 'whereistheplanet' will not be available as a coord_syst.")
    WHEREISTHEPLANET = False    


class DualWideOb(ObservingBlock):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        super(DualWideOb, self).__init__(*args, **kwargs)
        self.ob_type = "DualWideOb"
        return None

    def _generate_acquisition(self):
        """
        overwrite the method from dualOffOb to add the FT position resolved from FT name using Simbad. 
        the setup dict attribute will also by used to bypass some default values if required
        """        
        self.acquisition = tpl.DualWideAcq()
        self._fill_magnitudes(self.yml)        
        # set target names. in this mode, both sc_target and ft_target are required
        if "ft_target" in self.yml:
            self.acquisition["SEQ.FT.ROBJ.NAME"] = self.yml["ft_target"]
        else:
            printerr("No 'ft_target' specified in ObservingBlocks")
        if "sc_target" in self.yml:
            self.acquisition["SEQ.INS.SOBJ.NAME"] = self.yml["sc_target"]
        else:
            printerr("No 'sc_target' specified in ObservingBlocks")
        # now we need to resolve the targets
        # last step is to populate with setup, and then star object itself, which can be used to bypass any other setup
        self.acquisition.populate_from_yml(self.setup)
        self.acquisition.populate_from_yml(self.yml)
        return None

    def simbad_resolve(self, ob):
        """ For gwide, we need to overwrite this method, as we have 2 targets to resolve"""
        # get the guide star if given
        gs_table = None
        gs_name = None
        if "guide_star" in ob:
            if not(ob["guide_star"] is None):
                gs_name = ob["guide_star"]
                if not(ob["guide_star"].lower() in ["science", "ft"]):
                    gs_table = self.simbad_get_table(gs_name)
        # RESOLVE SC TARGET
        target_name = ob["sc_target"]
        common.printinf("Resolving target {} on Simbad".format(target_name))
        target_table = Simbad.query_object(target_name)
        if target_table is None:
            raise ValueError('Input not known by Simbad')
        common.printinf("Simbad resolution of {}: \n {}".format(target_name, target_table))
        if len(target_table) > 1:
            printwar("There are multiple results from Simbad. Which one should I use? (1, 2, etc.?)")
            stop()
        # populate the "target" tab using the SC target
        self.target = dict({})
        self.target["name"] = target_name 
        self._populate_from_simbad(target_table = target_table, target_name = target_name)
        # populate SC in the acq template
        self.acquisition._populate_sc_target_from_simbad(target_table = target_table, target_name = target_name, gs_name = gs_name, gs_table = gs_table)

        # now we resolve FT target
        target_name = ob["ft_target"]
        common.printinf("Resolving target {} on Simbad".format(target_name))
        target_table = Simbad.query_object(target_name)
        if target_table is None:
            raise ValueError('Input not known by Simbad')
        common.printinf("Simbad resolution of {}: \n {}".format(target_name, target_table))
        if len(target_table) > 1:
            printwar("There are multiple results from Simbad. Which one should I use? (1, 2, etc.?)")
            stop()
        # populate FT in the acq template
        self.acquisition._populate_ft_target_from_simbad(target_table = target_table, target_name = target_name)
        
        return None

            
class DualWideOffOb(DualOffOb, DualWideOb):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        DualOffOb.__init__(self, *args, **kwargs)
        self.ob_type = "DualWideOffOb"
        return None

    def _generate_acquisition(self):
        return DualWideOb._generate_acquisition(self)        

    def simbad_resolve(self, ob):
        return DualWideOb.simbad_resolve(self, ob)
        
    
class DualWideOnOb(DualOnOb, DualWideOb):
    def __init__(self, *args, **kwargs):
        """
        See ObservingBlock.__init__
        """        
        DualOnOb.__init__(self, *args, **kwargs)
        self.ob_type = "DualWideOnOb"
        return None    

    def _generate_acquisition(self):
        return DualWideOb._generate_acquisition(self)        

    def simbad_resolve(self, ob):
        DualWideOb.simbad_resolve(self, ob)
        # if the user gave specific coordinates for the SC, we need to overwrite them
        if "coord_syst" in ob:
            if ob["coord_syst"] == "radec":
                dra, ddec = ob["coord"][0], ob["coord"][1]
                sep, pa = math.sqrt(dra**2+ddec**2), math.atan2(dra, ddec)/math.pi*180.0
            elif ob["coord_syst"] == "pasep":
                pa, sep = ob["coord"]
                dra, ddec = math.sin(pa/180.0*math.pi)*sep, math.cos(pa/180.0*math.pi)*sep
            elif ob["coord_syst"] == "whereistheplanet":
                if WHEREISTHEPLANET:
                    common.printinf("Resolution of {} with whereistheplanet:".format(ob["coord"]))
                    dra, ddec, sep, pa = whereistheplanet.predict_planet(ob["coord"], self.setup["date"])
                    sep = sep[0]
                    pa = pa[0]
                else: 
                    common.printerr("whereistheplanet used as a coord_syst, but whereistheplanet module could not be loaded")
            else:
                common.printerr("Unknown coordinate system {}".format(obj_yml["coord_syst"]))
            # now we have dra, ddec, we need to recalculate SC position
            # FT coordinates
            coord_ft = SkyCoord(self.acquisition["SEQ.FT.ROBJ.ALPHA"], self.acquisition["SEQ.FT.ROBJ.DELTA"], unit=(u.hourangle, u.deg))
            # SC coordinates
            coord_sc = coord_ft.directional_offset_by(pa*u.deg, sep*u.mas)
            # put them in self.target
            self.target["ra"] = coord_sc.ra.to_string(unit=u.hourangle, sep=":", precision=3, pad=True)
            self.target["dec"] = coord_sc.dec.to_string(sep=":", precision=3, alwayssign=True)            
            return None


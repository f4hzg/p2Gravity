#coding: utf8
from abc import ABC, abstractmethod
import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord

from . import Template
from .. import common

class AcquisitionTemplate(Template):
    """
    GRAVITY generic acquisition template
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(AcquisitionTemplate, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_single_onaxis_acq'
        self.template_type = 'acquisition'        
        self["SEQ.FT.MODE"] = "AUTO"
        self["SEQ.MET.MODE"] = "ON"
        self["SEQ.INS.SOBJ.NAME"] = "Name"
        self["SEQ.INS.SOBJ.MAG"] = 0.0
        self["SEQ.INS.SOBJ.DIAMETER"] = 0.0
        self["SEQ.INS.SOBJ.VIS"] = 1.0
        self["TEL.TARG.PARALLAX"] = 0.0
        self["INS.SPEC.RES"] = "MED"
        self["INS.FT.POL"] = "OUT"
        self["INS.SPEC.POL"] = "OUT"
        self["COU.AG.TYPE"] = "ADAPT_OPT"
        self["COU.AG.GSSOURCE"] = "SCIENCE"
        self["COU.AG.ALPHA"] = "00:00:00.000"
        self["COU.AG.DELTA"] = "00:00:00.000"
        self["COU.AG.PARALLAX"] = 0.0
        self["COU.AG.PMA"] = 0.0
        self["COU.AG.PMD"] = 0.0
        self["COU.AG.EPOCH"] = 2000.0
        self["COU.GS.MAG"] = 0.0
        self["ISS.BASELINE"] = None
        self["ISS.VLTITYPE"] = None
        return None

    def _populate_from_simbad(self, target_table, target_name = ""):
        """ target type can be gs for coude guide star, or ft, or sc """
        coord = SkyCoord(target_table["RA"][0], target_table['DEC'][0], unit=(u.hourangle, u.deg))
        self["COU.AG.GSSOURCE"] = "SETUPFILE"
        self["COU.AG.ALPHA"] = coord.ra.to_string(unit=u.hourangle, sep=":", precision=3, pad=True)
        self["COU.AG.DELTA"] = coord.dec.to_string(sep=":", precision=3, alwayssign=True)
        try:
            self["COU.AG.PMA"] = round((target_table["PMRA"].to(u.arcsec/u.yr))[0].value, 5)
            self["COU.AG.PMD"] = round((target_table["PMDEC"].to(u.arcsec/u.yr))[0].value, 5)
        except:
            common.printwar("Proper motion not found on Simbad for target {}".format(target_name))                   
        try:
            self["TEL.TARG.PARALLAX"] = round((target_table['PLX_VALUE'][0]*u.mas).to(u.arcsec).value, 4)
            self["COU.AG.PARALLAX"] = round((target_table['PLX_VALUE'][0]*u.mas).to(u.arcsec).value, 4)
        except:
            self["TEL.TARG.PARALLAX"] = 0
            common.printwar("Parallax not found on Simbad for target {}".format(target_name))
        try:
            self["SEQ.INS.SOBJ.MAG"] = round(target_table['FLUX_K'][0].item(), 2)
        except:
            common.printwar("K band magnitude not found on Simbad for target {}".format(target_name))
        try:
            self["COU.GS.MAG"] = round(target_table['FLUX_V'][0].item(), 2)     
        except:
            common.printwar("V band magnitude not found on Simbad for target {}".format(target_name))
        return None

    @abstractmethod
    def populate_from_simbad(self, target_table, target_name):
        raise NotImplementedError("Must be overriden")

    
class SingleOnAxisAcq(AcquisitionTemplate):
    """
    GRAVITY_dual_onaxis_acq template (science)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(SingleOnAxisAcq, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_single_onaxis_acq'
        self["SEQ.INS.SOBJ.HMAG"] = 0.0                
        return None

    def populate_from_simbad(self, target_table, target_name):
        super(SingleOnAxisAcq, self)._populate_from_simbad(target_table, target_name)
        try:
            self["SEQ.FT.ROBJ.HMAG"] = round(target_table['FLUX_H'][0].item(), 2)
        except:
            common.printwar("H band magnitude not found on Simbad for target {}".format(target_name))                    
        return None

class SingleOffAxisAcq(AcquisitionTemplate):
    """
    GRAVITY_dual_onaxis_acq template (science)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(SingleOffAxisAcq, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_single_offaxis_acq'
        self["SEQ.MET.MODE"] = "OFF"
        self["SEQ.INS.SOBJ.HMAG"] = 0.0                
        return None

    def populate_from_simbad(self, target_table, target_name):
        super(SingleOffAxisAcq, self)._populate_from_simbad(target_table, target_name)
        try:
            self["SEQ.FT.ROBJ.HMAG"] = round(target_table['FLUX_H'][0].item(), 2)
        except:
            common.printwar("H band magnitude not found on Simbad for target {}".format(target_name))                    
        return None

    
class DualOnAxisAcq(AcquisitionTemplate):
    """
    GRAVITY_dual_onaxis_acq template (science)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.MET.MODE -- ON FAINT OFF (ON) -- Metrology laser mode    
    SEQ.FT.ROBJ.NAME -- (Name) -- FT object name
    SEQ.FT.ROBJ.MAG --  -10...30 (0) -- FT object total magnitude
    SEQ.FT.ROBJ.DIAMETER -- 0...300 (0) -- FT object diameter (mas). Only required for calibrator OBs.
    SEQ.FT.ROBJ.VIS -- -0...1.0 (0) -- FT object expected visibility
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    SEQ.INS.SOBJ.X -- 150...7000 (0) -- RA offset from FT to SC object in mas.
    SEQ.INS.SOBJ.Y -- 150...7000 (0) -- DEC offset from FT to SC object in mas.
    SEQ.FI.HMAG -- -10...25 (0) -- AcqCam guide star magnitude in H
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(DualOnAxisAcq, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_dual_onaxis_acq'
        self["SEQ.FT.MODE"] = "AUTO"
        self["SEQ.MET.MODE"] = "ON"
        self["SEQ.FT.ROBJ.NAME"] = "Name"
        self["SEQ.FT.ROBJ.MAG"] = 0.0
        self["SEQ.FT.ROBJ.HMAG"] = 0.0
        self["SEQ.FT.ROBJ.DIAMETER"] = 0.0
        self["SEQ.FT.ROBJ.VIS"] = 1.0
        self["SEQ.INS.SOBJ.X"] = 0.0
        self["SEQ.INS.SOBJ.Y"] = 0.0
        self["COU.AG.GSSOURCE"] = "FT"
        return None

    def populate_from_simbad(self, target_table, target_name):
        super(DualOnAxisAcq, self)._populate_from_simbad(target_table, target_name)
        try:        
            self["SEQ.FT.ROBJ.MAG"] = round(target_table['FLUX_K'][0].item(), 2)
        except:
            common.printwar("K band magnitude not found on Simbad for target {}".format(target_name))
        try:
            self["SEQ.FT.ROBJ.HMAG"] = round(target_table['FLUX_H'][0].item(), 2)
        except:
            common.printwar("H band magnitude not found on Simbad for target {}".format(target_name))                    
        return None    
    

class DualOffAxisAcq(DualOnAxisAcq):
    """
    GRAVITY_dual_onaxis_acq template (science)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.MET.MODE -- ON FAINT OFF (ON) -- Metrology laser mode    
    SEQ.PICKSC -- T A F (A) -- SC Object Picking strategy (T: operator picking, A: automatic picking, F: Separation tracking)
    SEQ.FT.ROBJ.NAME -- (Name) -- FT object name
    SEQ.FT.ROBJ.MAG --  -10...30 (0) -- FT object total magnitude
    SEQ.FT.ROBJ.DIAMETER -- 0...300 (0) -- FT object diameter (mas). Only required for calibrator OBs.
    SEQ.FT.ROBJ.VIS -- -0...1.0 (0) -- FT object expected visibility
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    SEQ.INS.SOBJ.X -- 150...7000 (0) -- RA offset from FT to SC object in mas.
    SEQ.INS.SOBJ.Y -- 150...7000 (0) -- DEC offset from FT to SC object in mas.
    SEQ.FI.HMAG -- -10...25 (0) -- AcqCam guide star magnitude in H
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(DualOffAxisAcq, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_dual_offaxis_acq'
        self["SEQ.PICKSC"] = "A"
        return None

    def populate_from_yml(self, yml):
        super(DualOffAxisAcq, self).populate_from_yml(yml)            
        return None


class DualWideAcq(AcquisitionTemplate):
    """
    GRAVITY_dual_wide_acq template (acquisition)
    Parameter -- Range (Default) -- Desciption
    SEQ.FT.MODE --  AUTO 1 2 7 9 (AUTO) -- Fringe Tracker mode
    SEQ.MET.MODE -- ON FAINT OFF (ON) -- Metrology laser mode    
    SEQ.FT.ROBJ.ALPHA -- 0...240000 (00:00:00.000) -- FT object RA
    SEQ.FT.ROBJ.DELTA -- -900000...900000 (00:00:00.000) -- FT object DEC
    SEQ.FT.ROBJ.PARALLAX -20...20 (0) -- FT object parallax in arcseconds
    SEQ.FT.ROBJ.PMA -10...10 (0) -- FT object proper motion in RA
    SEQ.FT.ROBJ.PMD -10...10 (0) -- FT object proper motion in DEC
    SEQ.FT.ROBJ.EPOCH -2000...3000 (2000) -- FT object epoch
    SEQ.FT.ROBJ.NAME -- (Name) -- FT object name
    SEQ.FT.ROBJ.MAG --  -10...30 (0) -- FT object total magnitude
    SEQ.FT.ROBJ.DIAMETER -- 0...300 (0) -- FT object diameter (mas). Only required for calibrator OBs.
    SEQ.FT.ROBJ.VIS -- -0...1.0 (0) -- FT object expected visibility
    SEQ.INS.SOBJ.NAME -- (Name) -- SC object name
    SEQ.INS.SOBJ.MAG -- -10...30 (0) -- SC object total magitude
    SEQ.INS.SOBJ.DIAMETER -- 0...300 (0) -- SC object diameter (mas). Only required for calibrator OBs.
    SEQ.INS.SOBJ.VIS -- -0...1.0 (0) -- SC object expected visibility
    SEQ.INS.SOBJ.X -- 150...7000 (0) -- RA offset from FT to SC object in mas.
    SEQ.INS.SOBJ.Y -- 150...7000 (0) -- DEC offset from FT to SC object in mas.
    SEQ.FI.HMAG -- -10...25 (0) -- AcqCam guide star magnitude in H
    TEL.TARG.PARALLAX -- -20...20 (0) -- FT object parallax (arcseconds)
    INS.SPEC.RES -- LOW MED HIGH (MED) -- Science spectrometer resolution LOW, MED or HIGH.
    INS.FT.POL -- IN OUT (IN) -- Fringe-tracker polarisation mode split (IN) or combined (OUT).
    INS.SPEC.POL -- IN OUT (IN) -- Science spectrometer polarisation mode split (IN) or combined (OUT).
    COU.AG.TYPE -- DEFAULT ADAPT_OPT ADAPT_ OPT_TCCD IR_AO_OFFAXIS (DEFAULT) -- Type of Coude guiding.
    COU.AG.GSSOURCE -- SETUPFILE SCIENCE (SCIENCE) -- Coude guide star (GS) input.
    COU.AG.ALPHA -- RA (0.) -- GS RA if SETUPFILE
    COU.AG.DELTA -- DEC (0.) -- GS DEC if SETUPFILE
    COU.GS.MAG -- 0...25 (0.) -- GS magnitude.
    COU.AG.PMA -- -10...10 (0) -- GS proper motion in RA
    COU.AG.PMD -- -10...10 (0) --GS proper motion in DEC
    """
    def __init__(self, *args, **kwargs):
        super(DualWideAcq, self).__init__(*args, **kwargs)
        self.template_name = 'GRAVITY_dual_wide_acq'
        self["SEQ.FT.MODE"] = "AUTO"
        self["SEQ.MET.MODE"] = "ON"
        self["SEQ.FT.ROBJ.NAME"] = "Name"
        self["SEQ.FT.ROBJ.ALPHA"] = "00:00:00.000"
        self["SEQ.FT.ROBJ.DELTA"] = "00:00:00.000"
        self["SEQ.FT.ROBJ.PARALLAX"] = 0
        self["SEQ.FT.ROBJ.PMA"] = 0
        self["SEQ.FT.ROBJ.PMD"] = 0
        self["SEQ.FT.ROBJ.EPOCH"] = 2000.0
        self["SEQ.FT.ROBJ.MAG"] = 0
        self["SEQ.FT.ROBJ.HMAG"] = 0.0
        self["SEQ.FT.ROBJ.DIAMETER"] = 0.0
        self["SEQ.FT.ROBJ.VIS"] = 1.0
        self["SEQ.INS.SOBJ.X"] = 0.0
        self["SEQ.INS.SOBJ.Y"] = 0.0
        self["COU.AG.GSSOURCE"] = "FT"        
        return None

    def populate_from_yml(self, yml):
        super(DualWideAcq, self).populate_from_yml(yml)            
        return None

    def _populate_ft_target_from_simbad(self, target_table, target_name):
        coord = SkyCoord(target_table["RA"][0], target_table['DEC'][0], unit=(u.hourangle, u.deg))        
        self["SEQ.FT.ROBJ.NAME"] = target_name        
        try:        
            self["SEQ.FT.ROBJ.MAG"] = round(target_table['FLUX_K'][0].item(), 2)
        except:
            common.printwar("K band magnitude not found on Simbad for target {}".format(target_name))
        try:
            self["SEQ.FT.ROBJ.HMAG"] = round(target_table['FLUX_H'][0].item(), 2)
        except:
            common.printwar("H band magnitude not found on Simbad for target {}".format(target_name))
        self["SEQ.FT.ROBJ.ALPHA"] = coord.ra.to_string(unit=u.hourangle, sep=":", precision=3, pad=True)        
        self["SEQ.FT.ROBJ.DELTA"] = coord.dec.to_string(sep=":", precision=3, alwayssign=True)
        try:
            self["SEQ.FT.ROBJ.PMA"] = round((target_table["PMRA"].to(u.arcsec/u.yr))[0].value, 5)
            self["SEQ.FT.ROBJ.PMD"] = round((target_table["PMDEC"].to(u.arcsec/u.yr))[0].value, 5)
        except:
            common.printwar("Proper motion not found on Simbad for target {}".format(target_name))                   
        try:
            self["SEQ.FT.ROBJ.PARALLAX"] = round((target_table['PLX_VALUE'][0]*u.mas).to(u.arcsec).value, 4)
        except:
            self["SEQ.FT.ROBJ.PARALLAX"] = 0
            common.printwar("Parallax not found on Simbad for target {}".format(target_name))
        return None

    def _populate_sc_target_from_simbad(self, target_table, target_name):
        coord = SkyCoord(target_table["RA"][0], target_table['DEC'][0], unit=(u.hourangle, u.deg))        
        self["SEQ.INS.SOBJ.NAME"] = target_name        
        try:        
            self["SEQ.INS.SOBJ.MAG"] = round(target_table['FLUX_K'][0].item(), 2)
        except:
            common.printwar("K band magnitude not found on Simbad for target {}".format(target_name))
        try:
            self["SEQ.INS.SOBJ.HMAG"] = round(target_table['FLUX_H'][0].item(), 2)
        except:
            common.printwar("H band magnitude not found on Simbad for target {}".format(target_name))
        try:
            self["TEL.TARG.PARALLAX"] = round((target_table['PLX_VALUE'][0]*u.mas).to(u.arcsec).value, 4)
        except:
            self["TEL.TARG.PARALLAX"] = 0
            common.printwar("Parallax not found on Simbad for target {}".format(target_name))
        return None        
    

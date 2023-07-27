#coding: utf8
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.widgets import Button
import matplotlib.image as mpimg

from astropy import units as u
from astropy.coordinates import SkyCoord

import math
import numpy as np

# to show the DIT JPG
import os
WHEREAMI = os.path.dirname(__file__)
DIT_JPG = WHEREAMI+"/selecting_dit_values.jpg"

# linestyles
FT_LS = (5, (4, 6))
SC_LS = (0, (4, 6))
# colors
FT_C = "C0"
SC_C = "C1"

def show_dit_jpg():
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111)
    img = mpimg.imread(DIT_JPG)
    imgplot = ax.imshow(img)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    plt.tight_layout()
    plt.show()
    return None


def plot_acquisition(ob, ax = None, fiber_fov = 30, ft_c = FT_C, sc_c = SC_C):
    acqTpl = ob.acquisition
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    # GWIDE
    if ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
        # center of field = acq target = ft target
        ax.plot(0, 0, "*k", markersize=20)        
        # plot FT fiber            
        xft, yft = ob.acquisition["SEQ.FT.ROBJ.ALPHA"], ob.acquisition["SEQ.FT.ROBJ.DELTA"]
        xsc, ysc = ob.target["ra"], ob.target["dec"]
        coord_ft = SkyCoord(xft, yft, unit=(u.hourangle, u.deg))
        coord_sc = SkyCoord(xsc, ysc, unit=(u.hourangle, u.deg))
        pa = coord_ft.position_angle(coord_sc).to(u.rad).value
        sep = coord_ft.separation(coord_sc).to(u.arcsec).value
        if ob.acquisition["COU.AG.GSSOURCE"] == "FT":
            xsc, ysc = math.sin(pa)*sep, math.cos(pa)*sep
            xft, yft = 0, 0
        elif ob.acquisition["COU.AG.GSSOURCE"] == "SCIENCE":
            xsc, ysc = 0, 0
            xft, yft = -math.sin(pa)*sep, -math.cos(pa)*sep
        else:
            # not implemented
            xsc, ysc = 0, 0
            xft, yft = 0, 0
        # FT fiber
        fib = plt.plot(xft, yft, color=ft_c, marker="o", ls="")        
        # SC fiber is ACQ target
        fib = plt.plot(xsc, ysc, color=sc_c, marker="o", ls="")
        if not(ob.ob_type in ["DualWideOnOb"]):
            x, y = (xsc - xft), (ysc - yft)
            norm = math.sqrt(x**2+y**2)
            plt.plot([-1000*x/norm, 1000*x/norm], [-1000*y/norm, 1000*y/norm], "-k", alpha=0.2)
        else:
            x = np.mean(np.array([tpl["SEQ.RELOFF.X"] for tpl in ob.templates]))
            y = np.mean(np.array([tpl["SEQ.RELOFF.Y"] for tpl in ob.templates]))           
            norm = math.sqrt(x**2+y**2)
            plt.plot([-1000*x/norm+xsc, 1000*x/norm+xsc], [-1000*y/norm+ysc, 1000*y/norm+ysc], "-k", alpha=0.2)
    # OTHER MODES
    else:
        # plot FT fiber
        ax.plot(0, 0, "*k")
        fib = plt.Circle((0, 0), fiber_fov, edgecolor=ft_c, facecolor="None", ls = FT_LS)
        ax.add_patch(fib)        
        # plot science fiber
        if acqTpl.template_name in ["GRAVITY_single_onaxis_acq", "GRAVITY_single_offaxis_acq"]:
            fib = plt.Circle((0, 0), fiber_fov, edgecolor=sc_c, facecolor="None", ls = SC_LS)
            ax.add_patch(fib)
        if acqTpl.template_name in ["GRAVITY_dual_onaxis_acq", "GRAVITY_dual_offaxis_acq"]:
            x, y = acqTpl["SEQ.INS.SOBJ.X"], acqTpl["SEQ.INS.SOBJ.Y"]
            fib = plt.Circle((x, y), fiber_fov, edgecolor=sc_c, facecolor="None", ls = SC_LS)
            ax.add_patch(fib)
            norm = math.sqrt(x**2+y**2)
            plt.plot([-1000*x/norm, 1000*x/norm], [-1000*y/norm, 1000*y/norm], "-k", alpha=0.2)
    return None        

def plot_dualObsExp(ob, template, ax = None, fiber_fov = 30, ft_c = FT_C, sc_c = SC_C, ft_ls = FT_LS, sc_ls = SC_LS, sobj = (0, 0), swap = 1):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    # FT fiber
    if ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
        # gwide is a pain
        xft, yft = ob.acquisition["SEQ.FT.ROBJ.ALPHA"], ob.acquisition["SEQ.FT.ROBJ.DELTA"]
        xsc, ysc = ob.target["ra"], ob.target["dec"]
        coord_ft = SkyCoord(xft, yft, unit=(u.hourangle, u.deg))
        coord_sc = SkyCoord(xsc, ysc, unit=(u.hourangle, u.deg))
        pa = coord_ft.position_angle(coord_sc).to(u.rad).value
        sep = coord_ft.separation(coord_sc).to(u.arcsec).value
        if ob.acquisition["COU.AG.GSSOURCE"] == "FT":
            xsc, ysc = math.sin(pa)*sep, math.cos(pa)*sep
            xft, yft = 0, 0
        elif ob.acquisition["COU.AG.GSSOURCE"] == "SCIENCE":
            xsc, ysc = 0, 0
            xft, yft = -math.sin(pa)*sep, -math.cos(pa)*sep
        else:
            # not implemented
            xsc, ysc = 0, 0
            xft, yft = 0, 0
        fib = ax.plot(swap*xft, swap*yft, color=FT_C, marker = "o", ls = "")
        if ob.ob_type in ["DualWideOnOb"]:
            for k in range(len(template["SEQ.RELOFF.X"])):
                dx, dy = template["SEQ.RELOFF.X"][k], template["SEQ.RELOFF.Y"][k]
                sep, pa = round(math.sqrt(dx**2+dy**2), 2), round(math.atan2(dx, dy)/math.pi*180, 2)                
                fib = ax.plot(swap*xsc, swap*ysc, color="k", marker = "+", ls = "")
                fib = ax.plot(swap*xsc+dx/1000.0, swap*ysc+dy/1000.0, color=sc_c, marker = "o", ls = "")
                fib = ax.plot([swap*xsc, swap*xsc+dx/1000.0], [swap*ysc, swap*ysc+dy/1000.0], color=sc_c, marker = "", ls = "--") # in WIDE, the unit of plot is as not mas
                txt = "$(\Delta{{}}\mathrm{{RA}}, \Delta{{}}\mathrm{{DEC}}) = ({}\,\mathrm{{mas}}, {}\,\mathrm{{mas}})$\n".format(dx, dy)
                txt = txt + "$(\mathrm{{PA}}, \mathrm{{SEP}}) = ({}\,\mathrm{{deg}}, {}\,\mathrm{{mas}})$ \n".format(pa, sep)                
        else:
            fib = ax.plot(swap*xsc, swap*ysc, color=sc_c, marker = "o", ls = "")
            txt = ""            
    else:
        fib = plt.Circle((0, 0), fiber_fov, edgecolor=ft_c, facecolor="None", ls = ft_ls)
        ax.add_patch(fib)
        # SC fiber
        for k in range(len(template["SEQ.RELOFF.X"])):
            x, y = sobj[0]+template["SEQ.RELOFF.X"][k], sobj[1]+template["SEQ.RELOFF.Y"][k]       
            fib = plt.Circle((x, y), fiber_fov, edgecolor=sc_c, facecolor="None", ls = sc_ls)
            ax.add_patch(fib)
        sep, pa = round(math.sqrt(x**2+y**2), 2), round(math.atan2(x, y)/math.pi*180, 2)
        txt = "$(\Delta{{}}\mathrm{{RA}}, \Delta{{}}\mathrm{{DEC}}) = ({}\,\mathrm{{mas}}, {}\,\mathrm{{mas}})$\n".format(x, y)
        txt = txt + "$(\mathrm{{PA}}, \mathrm{{SEP}}) = ({}\,\mathrm{{deg}}, {}\,\mathrm{{mas}})$ \n".format(pa, sep)
        
    dit, ndit, ndit_sky = template["DET2.DIT"], template["DET2.NDIT.OBJECT"], template["DET2.NDIT.SKY"]
    exptime = 0
    exptime_sky = 0
    for o in template["SEQ.OBSSEQ"]:
        if o == "O":
            exptime = exptime+dit*ndit
        if o == "S":
            exptime_sky = exptime_sky+dit*ndit_sky            
    txt = txt + "$(\mathrm{{DIT}}, \mathrm{{NDIT}}, \mathrm{{NDIT_{{SKY}}}}) = ({}\,\mathrm{{s}}, {}, {})$ \n".format(dit, ndit, ndit_sky)    
    txt = txt+"Sequence: {}\n".format(template["SEQ.OBSSEQ"])
#    txt = txt+"Exposure time (object, sky): $({}\,\mathrm{{s}}, {}\,\mathrm{{s}})$\n".format(exptime, exptime_sky)
    return txt

def plot_singleObsExp(ob, template, ax = None, ft_c = FT_C, sc_c = SC_C, fiber_fov = 30, ft_ls = FT_LS, sc_ls = SC_LS, swap = 1):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.plot(0, 0, "*k")
    # FT fib
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=ft_c, facecolor="None", ls = ft_ls)
    ax.add_patch(fib)
    # SC fib
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=sc_c, facecolor="None", ls = sc_ls)
    ax.add_patch(fib)    
    dit, ndit, ndit_sky = template["DET2.DIT"], template["DET2.NDIT.OBJECT"], template["DET2.NDIT.SKY"]
    exptime = 0
    exptime_sky = 0    
    for o in template["SEQ.OBSSEQ"]:
        if o == "O":
            exptime = exptime+dit*ndit
        if o == "S":
            exptime_sky = exptime_sky+dit*ndit_sky
    txt = "Sequence: {}\n".format(template["SEQ.OBSSEQ"])
    txt = txt + "$(\mathrm{{DIT}}, \mathrm{{NDIT}}, \mathrm{{NDIT_{{SKY}}}}) = ({}\,\mathrm{{s}}, {}, {})$ \n".format(dit, ndit, ndit_sky)    
    txt = txt+"Exposure time (object, sky): $({}\,\mathrm{{s}}, {}\,\mathrm{{s}})$\n".format(exptime, exptime_sky)    
    return txt

def plot_dualObsSwap(ob, template, ax = None, fiber_fov = 30, ft_c = FT_C, sc_c = SC_C, ft_ls = FT_LS, sc_ls = SC_LS, sobj = (0, 0), swap = 1):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    if ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
        # gwide is a pain        
        xft, yft = ob.acquisition["SEQ.FT.ROBJ.ALPHA"], ob.acquisition["SEQ.FT.ROBJ.DELTA"]
        xsc, ysc = ob.target["ra"], ob.target["dec"]
        coord_ft = SkyCoord(xft, yft, unit=(u.hourangle, u.deg))
        coord_sc = SkyCoord(xsc, ysc, unit=(u.hourangle, u.deg))
        pa = coord_ft.position_angle(coord_sc).to(u.rad).value
        sep = coord_ft.separation(coord_sc).to(u.arcsec).value
        if ob.acquisition["COU.AG.GSSOURCE"] == "FT":
            xsc, ysc = math.sin(pa)*sep, math.cos(pa)*sep
            xft, yft = 0, 0
        elif ob.acquisition["COU.AG.GSSOURCE"] == "SCIENCE":
            xsc, ysc = 0, 0
            xft, yft = -math.sin(pa)*sep, -math.cos(pa)*sep
        else:
            # not implemented
            xsc, ysc = 0, 0
            xft, yft = 0, 0
        # plot fibers                        
        fib = ax.plot(xft, yft, color=ft_c, marker = "o", ls="")
        fib = ax.plot(xsc, ysc, color=sc_c, marker = "o", ls="")
        # swap arrow
        arrow = patches.FancyArrowPatch((0, 0), (xft-xsc, yft-ysc), arrowstyle='<->', mutation_scale=10)
        ax.add_patch(arrow)        
    else:
        # FT pos
        fib = plt.Circle((0, 0), fiber_fov, edgecolor=ft_c, facecolor="None", ls = ft_ls)
        ax.add_patch(fib)
        # SC fib
        fib = plt.Circle(sobj, fiber_fov, edgecolor=sc_c, facecolor="None", ls = sc_ls)
        ax.add_patch(fib)
        # plot an arrow
        arrow = patches.FancyArrowPatch((0, 0), sobj, arrowstyle='<->', mutation_scale=10)
        ax.add_patch(arrow)
    txt = "SWAP\n\n\n\n\n\n\n"
    return txt


def plot_template(ob, template, **kwargs):
    if template.template_name in ["GRAVITY_single_obs_exp", "GRAVITY_single_obs_calibrator"]:
        return plot_singleObsExp(ob, template, **kwargs)    
    if template.template_name in ["GRAVITY_dual_obs_exp", "GRAVITY_dual_obs_calibrator"]:
        return plot_dualObsExp(ob, template, **kwargs)
    if template.template_name == "GRAVITY_dual_obs_swap":
        return plot_dualObsSwap(ob, template, **kwargs)
    

def plot_ob(ob, title = None, fov = None, bg=None, bglim=None, ft_c = None, sc_c = None, acq_only = False):
    # default colors
    if ft_c is None:
        ft_c = FT_C
    if sc_c is None:
        sc_c = SC_C            
    # prepare figure and gridspec
    fig = plt.figure(figsize=(12, 7), tight_layout = True)
    ntpl = len(ob.templates)
    ncols = 6
    nrows = 2 + math.ceil(ntpl/6)
    h_ratios = nrows*[5]
    h_ratios[0] = 1
    h_ratios[1] = 30
    gs = gridspec.GridSpec(nrows, ncols, height_ratios = h_ratios)
    # get fiber fov from telescope type
    if "UTs" in ob.acquisition["ISS.BASELINE"]:
        fiber_fov = 30
    else: # ATs
        fiber_fov = 120
    # default fov is 10 fiber_fov
    if fov is None:
        fov = 10*fiber_fov
    # create main axis for OB plot
    ax_ob = fig.add_subplot(gs[1, 0:3])
    # add background if requested
    if not(bg is None):
        img = mpimg.imread(bg)
        imgplot = ax_ob.imshow(img, extent=bglim)
    ax_ob.grid("both")
    ax_ob.set_xlim(fov, -fov)
    ax_ob.set_ylim(-fov, fov)    
#    ax_ob.invert_xaxis()
    ax_ob.set_aspect("equal")
    # now we can plot the acquisition
    plot_acquisition(ob, fiber_fov = fiber_fov, ax = ax_ob, ft_c = ft_c, sc_c = sc_c)
    if ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
        ax_ob.set_xlabel("$\Delta{}\mathrm{RA}$ (mas)")
        ax_ob.set_ylabel("$\Delta{}\mathrm{DEC}$ (mas)")
    else:
        ax_ob.set_xlabel("$\Delta{}\mathrm{RA}$ (as)")
        ax_ob.set_ylabel("$\Delta{}\mathrm{DEC}$ (as)")    

    # and plot the templates one by one
    txt_col1 = "" # we'll have two columns of text to explain templates
    txt_col2 = ""
    swap = 1 # for dualOff we need to keep track of swap status
    for k in range(ntpl):
        # for each template, we add it on top of main plot
        if ob.ob_type in ["DualOffOb", "DualOnOb"]: # take into account acquisition offset
            sobj = (swap*ob.acquisition["SEQ.INS.SOBJ.X"], swap*ob.acquisition["SEQ.INS.SOBJ.Y"])
            plot_template(ob, ob.templates[k], fiber_fov = fiber_fov, ax = ax_ob, sobj = sobj, swap = swap, ft_c = ft_c, sc_c = sc_c)
        elif ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
            plot_template(ob, ob.templates[k], fiber_fov = fiber_fov, ax = ax_ob, swap = swap, ft_c = ft_c, sc_c = sc_c)
        else:
            plot_template(ob, ob.templates[k], fiber_fov = fiber_fov, ax = ax_ob, swap = swap, ft_c = ft_c, sc_c = sc_c)
        # and we plot it as an individual subplot at bottom
        if not(acq_only):
            row, col = k//ncols, k - ncols*(k//ncols)
            ax_tpl = fig.add_subplot(gs[2+row, col])
            ax_tpl.grid("both")
            ax_tpl.set_xlim(fov, -fov)
            ax_tpl.set_ylim(-fov, fov)
            ax_tpl.set_aspect("equal")
            ax_tpl.set_title("TPL {}".format(k+1))
            if ob.ob_type in ["DualOffOb", "DualOnOb"]: # take into account acquisition offset
                sobj = (swap*ob.acquisition["SEQ.INS.SOBJ.X"], swap*ob.acquisition["SEQ.INS.SOBJ.Y"])
                txt_tpl = plot_template(ob, ob.templates[k], ax = ax_tpl, ft_ls = "-", sc_ls = "-", sobj = sobj, ft_c = ft_c, sc_c = sc_c)
            elif ob.ob_type in ["DualWideOnOb", "DualWideOffOb"]:
                txt_tpl = plot_template(ob, ob.templates[k], fiber_fov = fiber_fov, ax = ax_tpl, swap = swap, ft_c = ft_c, sc_c = sc_c)                        
            else:
                txt_tpl = plot_template(ob, ob.templates[k], ax = ax_tpl, ft_ls = "-", sc_ls = "-", ft_c = ft_c, sc_c = sc_c)            
            if k%2==0:
                txt_col1 = txt_col1+"TPL {}:\n{}\n".format(k+1, txt_tpl)
            else:
                txt_col2 = txt_col2+"TPL {}:\n{}\n".format(k+1, txt_tpl)
            # now we can add the text
            ax_txt = fig.add_subplot(gs[1, 3:6])
            ax_txt.axis("off")
            ax_txt.text(0, 1, txt_col1, fontsize=8, va="top", ha="left")
            ax_txt.text(0.5, 1, txt_col2, fontsize=8, va="top", ha="left")
        # if this template was a swap, swap the swap value
        if ob.templates[k].template_name == "GRAVITY_dual_obs_swap":
            swap = -swap

    # and a title if requested
    if not(title is None):
        ax_title = fig.add_subplot(gs[0, 0:4])
        ax_title.axis("off")        
        ax_title.text(0.1, 0, title, fontsize=12, va="center", ha="left")

    ax_ob.legend(["Acq tgt", "FT fiber", "SC fiber", "Acq direction"])        
    return fig, gs
    


    

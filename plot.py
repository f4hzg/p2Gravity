#coding: utf8
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.widgets import Button

import math

# linestyles
FT_LS = (5, (4, 6))
SC_LS = (0, (4, 6))
# colors
FT_C = "C0"
SC_C = "C1"

def plot_acquisition(acqTpl, ax = None, fiber_fov = 30):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    # center of field
    ax.plot(0, 0, "*k")
    # plot FT fiber
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=FT_C, facecolor="None", ls = FT_LS)
    ax.add_patch(fib)
    # plot science fiber
    if acqTpl.template_name in ["GRAVITY_single_onaxis_acq", "GRAVITY_single_offaxis_acq"]:
        fib = plt.Circle((0, 0), fiber_fov, edgecolor=SC_C, facecolor="None", ls = SC_LS)
        ax.add_patch(fib)
    if acqTpl.template_name in ["GRAVITY_dual_onaxis_acq", "GRAVITY_dual_offaxis_acq"]:
        x, y = acqTpl["SEQ.INS.SOBJ.X"], acqTpl["SEQ.INS.SOBJ.Y"]
        fib = plt.Circle((x, y), fiber_fov, edgecolor=SC_C, facecolor="None", ls = SC_LS)
        ax.add_patch(fib)
        norm = math.sqrt(x**2+y**2)
        plt.plot([-1000*x/norm, 1000*x/norm], [-1000*y/norm, 1000*y/norm], "-k", alpha=0.2)
    return None        

def plot_dualObsExp(template, ax = None, fiber_fov = 30, ft_ls = FT_LS, sc_ls = SC_LS, sobj = (0, 0)):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    # FT fiber
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=FT_C, facecolor="None", ls = ft_ls)
    ax.add_patch(fib)
    # SC fiber
    for k in range(len(template["SEQ.RELOFF.X"])):
        x, y = sobj[0]+template["SEQ.RELOFF.X"][k], sobj[1]+template["SEQ.RELOFF.Y"][k]       
        fib = plt.Circle((x, y), fiber_fov, edgecolor=SC_C, facecolor="None", ls = sc_ls)
        ax.add_patch(fib)
    sep, pa = round(math.sqrt(x**2+y**2), 2), round(math.atan2(x, y)/math.pi*180, 2)
    dit, ndit, ndit_sky = template["DET2.DIT"], template["DET2.NDIT.OBJECT"], template["DET2.NDIT.SKY"]
    exptime = 0
    exptime_sky = 0    
    for o in template["SEQ.OBSSEQ"]:
        if o == "O":
            exptime = exptime+dit*ndit
        if o == "S":
            exptime_sky = exptime_sky+dit*ndit_sky            
    txt = "$(\Delta{{}}\mathrm{{RA}}, \Delta{{}}\mathrm{{DEC}}) = ({}\,\mathrm{{mas}}, {}\,\mathrm{{mas}})$\n".format(x, y)
    txt = txt + "$(\mathrm{{PA}}, \mathrm{{SEP}}) = ({}\,\mathrm{{deg}}, {}\,\mathrm{{mas}})$ \n".format(pa, sep)
    txt = txt + "$(\mathrm{{DIT}}, \mathrm{{NDIT}}, \mathrm{{NDIT_{{SKY}}}}) = ({}\,\mathrm{{s}}, {}\,\mathrm{{s}}, {}\,\mathrm{{s}})$ \n".format(dit, ndit, ndit_sky)    
    txt = txt+"Sequence: {}\n".format(template["SEQ.OBSSEQ"])
#    txt = txt+"Exposure time (object, sky): $({}\,\mathrm{{s}}, {}\,\mathrm{{s}})$\n".format(exptime, exptime_sky)
    return txt

def plot_singleObsExp(template, ax = None, fiber_fov = 30, ft_ls = FT_LS, sc_ls = SC_LS):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.plot(0, 0, "*k")
    # FT fib
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=FT_C, facecolor="None", ls = ft_ls)
    ax.add_patch(fib)
    # SC fib
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=SC_C, facecolor="None", ls = sc_ls)
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
    txt = txt + "$(\mathrm{{DIT}}, \mathrm{{NDIT}}, \mathrm{{NDIT_{{SKY}}}}) = ({}\,\mathrm{{s}}, {}\,\mathrm{{s}}, {}\,\mathrm{{s}})$ \n".format(dit, ndit, ndit_sky)    
    txt = txt+"Exposure time (object, sky): $({}\,\mathrm{{s}}, {}\,\mathrm{{s}})$\n".format(exptime, exptime_sky)    
    return txt

def plot_dualObsSwap(template, ax = None, fiber_fov = 30, ft_ls = FT_LS, sc_ls = SC_LS, sobj = (0, 0)):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    # FT pos
    fib = plt.Circle((0, 0), fiber_fov, edgecolor=FT_C, facecolor="None", ls = ft_ls)
    ax.add_patch(fib)
    # SC fib
    fib = plt.Circle(sobj, fiber_fov, edgecolor=SC_C, facecolor="None", ls = sc_ls)
    ax.add_patch(fib)
    # plot an arrow
    arrow = patches.FancyArrowPatch((0, 0), sobj, arrowstyle='<->', mutation_scale=10)
    ax.add_patch(arrow)
    txt = "SWAP\n\n\n\n\n\n\n"
    return txt


def plot_template(template, **kwargs):
    if template.template_name == "GRAVITY_single_obs_exp":
        return plot_singleObsExp(template, **kwargs)    
    if template.template_name == "GRAVITY_dual_obs_exp":
        return plot_dualObsExp(template, **kwargs)
    if template.template_name == "GRAVITY_dual_obs_swap":
        return plot_dualObsSwap(template, **kwargs)        
    
    
def plot_ob(ob, title = None, fov = None):
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
    ax_ob.grid("both")
    ax_ob.set_xlim(fov, -fov)
    ax_ob.set_ylim(-fov, fov)
    ax_ob.set_aspect("equal")
    ax_ob.set_xlabel("$\Delta{}\mathrm{RA}$ (mas)")
    ax_ob.set_ylabel("$\Delta{}\mathrm{DEC}$ (mas)")

    # now we can plot the acquisition
    plot_acquisition(ob.acquisition, fiber_fov = fiber_fov, ax = ax_ob)

    # and plot the templates one by one
    txt_col1 = "" # we'll have two columns of text to explain templates
    txt_col2 = ""
    swap = 1 # for dualOff we need to keep track of swap status
    for k in range(ntpl):
        # for each template, we add it on top of main plot
        if ob.ob_type in ["DualOffOb", "DualOnOb"]: # take into account acquisition offset
            sobj = (swap*ob.acquisition["SEQ.INS.SOBJ.X"], swap*ob.acquisition["SEQ.INS.SOBJ.Y"])
            plot_template(ob.templates[k], fiber_fov = fiber_fov, ax = ax_ob, sobj = sobj)
        else:
            plot_template(ob.templates[k], fiber_fov = fiber_fov, ax = ax_ob)
        # and we plot it as an individual subplot at bottom
        row, col = k//ncols, k - ncols*(k//ncols)
        ax_tpl = fig.add_subplot(gs[2+row, col])
        ax_tpl.grid("both")
        ax_tpl.set_xlim(fov, -fov)
        ax_tpl.set_ylim(-fov, fov)
        ax_tpl.set_aspect("equal")
        ax_tpl.set_title("TPL {}".format(k+1))
        if ob.ob_type in ["DualOffOb", "DualOnOb"]: # take into account acquisition offset
            sobj = (swap*ob.acquisition["SEQ.INS.SOBJ.X"], swap*ob.acquisition["SEQ.INS.SOBJ.Y"])
            txt_tpl = plot_template(ob.templates[k], ax = ax_tpl, ft_ls = "-", sc_ls = "-", sobj = sobj)
        else:
            txt_tpl = plot_template(ob.templates[k], ax = ax_tpl, ft_ls = "-", sc_ls = "-")            
        if k%2==0:
            txt_col1 = txt_col1+"TPL {}:\n{}\n".format(k+1, txt_tpl)
        else:
            txt_col2 = txt_col2+"TPL {}:\n{}\n".format(k+1, txt_tpl)
        # if this template was a swap, swap the swap value
        if ob.templates[k].template_name == "GRAVITY_dual_obs_swap":
            swap = -swap
    # now we can add the text
    ax_txt = fig.add_subplot(gs[1, 3:6])
    ax_txt.axis("off")
    ax_txt.text(0, 1, txt_col1, fontsize=8, va="top", ha="left")
    ax_txt.text(0.5, 1, txt_col2, fontsize=8, va="top", ha="left")

    # and a title if requested
    if not(title is None):
        ax_title = fig.add_subplot(gs[0, 0:4])
        ax_title.axis("off")        
        ax_title.text(0.1, 0, title, fontsize=12, va="center", ha="left")

    ax_ob.legend(["Acq tgt", "FT fiber", "SC fiber", "Acq direction"])
    return fig, gs
    


    

import geometry
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.path import Path
from voronoi import VoronoiPlt
import drawing
from animplayer import Player
import config
import metrics
   
def _reset(patch):
    patch.set_path(Path([(0,0)]))
    

def get_euclid_segments_path(segments):
    if len(segments) == 0:
        return Path([(0,0)])
    v = []
    codes = []
    for s in segments:
        v.append((s[0],s[1]))
        codes.append(Path.MOVETO)
        
        v.append((s[2],s[3]))
        codes.append(Path.LINETO)
        
    return Path(v,codes)

def get_manhattan_segments_path(segments):
    if len(segments) == 0:
        return Path([(0,0)])
    v = []
    codes = []
    
    for s in segments:
        p1 = s[4]
        p2 = s[5]

        (x1,y1,x2,y2)=s[0],s[1],s[2],s[3]
        
        
        (r1_x,r1_y),(x1,y1),(x2,y2),(r2_x,r2_y) = geometry.get_seg(p1,p2,min(x1,x2),max(x1,x2),min(y1,y2),max(y1,y2))
        
        codes.append(Path.MOVETO)
        v.append((r1_x,r1_y))
        codes.append(Path.LINETO)
        v.append((x1,y1))
        codes.append(Path.LINETO)
        v.append((x2,y2))
        codes.append(Path.LINETO)
        v.append((r2_x,r2_y))
        
    return Path(v,codes)
    
def _draw_step(i,ax, segments_done, snapshots, points_plt, segment_finished_patch,segment_inprogress_patch, circle_patch, arcs_patch, d_plot, xlim, ylim,is_manhattan):
    
    [_reset(patch) for patch in [circle_patch,arcs_patch,  segment_finished_patch,segment_inprogress_patch]]
    steps_len = len(snapshots)
    
    if is_manhattan:
        get_circle_path = drawing.get_manhattan_circle_path
        get_parabola_values = drawing.get_manhattan_parabola_values
        intersection_fn = metrics.ManhattanMetric.intersection
        get_segment_path = get_manhattan_segments_path
    else:
        get_circle_path = drawing.get_euclid_circle_path
        get_parabola_values = drawing.get_euclid_parabola_values
        intersection_fn = metrics.EuclideanMetric.intersection
        get_segment_path = get_euclid_segments_path
        
        
    if i == steps_len:
        ax.set_title("Voronoi Output")
        segments_path = get_segment_path(segments_done)
        segment_finished_patch.set(path=segments_path,fill=False,color = 'black')
        # TODO
    else:
        step = snapshots[i]
        
        step_type = step['step_type']
        ax.set_title(f"{step_type} - Step {i} out of {steps_len}")
        
         # points
        points_p = [ s['site'] for s in snapshots[:i+1] if 'site' in s]
        points= np.array([(p.x,p.y) for p in points_p])
        points_plt.set_data(points[:,0], points[:,1])
        
         # directrix
        directrix = step['directrix']
        d_plot.set_data([0,1000],[directrix,directrix])
        
        # segments finished
        segments_o = step['output']
        segments_path = get_segment_path(segments_o)
        segment_finished_patch.set(path=segments_path,fill=False,color = 'black')
        
        # segments inprogres
        
        segments_i = step['in_progress']
        segments_inprogress = get_segment_path(segments_i)
        segment_inprogress_patch.set(path=segments_inprogress, fill=False, color = 'gray')
        
        # Arcs
    
        beachline = drawing.get_beachline_path(step,directrix, intersection_fn,get_parabola_values)
        arcs_patch.set(path=beachline,fill=False, color='red')
        
        
        # Circle Event
        if 'radius' in step:
            r = step['radius']
            center = step['center']
            path = get_circle_path(center,r)
            circle_patch.set(path=path,fill=False, color='orange')
    
    plt.show()
    
    
def init():
    return []


def _setup_animation_deps(points, is_manhattan = True, xlim=None, ylim=None, figsize = None):
    xlim = xlim if xlim else (config.VIEW_X_MIN,config.VIEW_X_MAX)
    ylim = ylim if ylim else (config.VIEW_Y_MIN, config.VIEW_Y_MAX)

    metric = metrics.ManhattanMetric if is_manhattan else metrics.EuclideanMetric
    vplt = VoronoiPlt(points, metric=metric)
    vplt.process()
       
    return vplt, *_prepare_animation(points,is_manhattan,vplt, xlim, ylim,figsize = figsize)
    

def draw_static_animation(points, is_manhattan = True, xlim=None, ylim=None, interval=1000, figsize=(5,5)):
    vplt, fig, anim_fn = _setup_animation_deps(points, is_manhattan , xlim, ylim, figsize)
    return FuncAnimation(fig, anim_fn, frames=len(vplt.steps) + 1, interval=interval)


def draw_interactive_animation(points, is_manhattan = True, xlim=None, ylim=None, interval=1000,figsize=(5,5)):
    vplt, fig, anim_fn = _setup_animation_deps(points, is_manhattan , xlim, ylim)
    return Player(fig, anim_fn, maxi=len(vplt.steps), interval=interval)


def _prepare_animation(points, is_manhattan, vplt,xlim,ylim, figsize = None):
    segments_done = vplt.get_output()    
    snapshots = vplt.steps
    figsize = figsize if figsize else (5,5)
    
    xlim = (config.VIEW_X_MIN,config.VIEW_X_MAX)
    ylim = (config.VIEW_Y_MIN, config.VIEW_Y_MAX)
    fig = plt.figure(figsize = figsize)
    
    ax = plt.axes(xlim=xlim, ylim=ylim)
    (points_plt,) = ax.plot([], [], "o")
    (d_plot,) = ax.plot([], [], linestyle='-',color="yellow")
    
    
    segments_inprogress_patch = ax.add_patch(patches.PathPatch(Path([(0,0)])))
    segments_done_patch = ax.add_patch(patches.PathPatch(Path([(0,0)])))
    circle_patch = ax.add_patch(patches.PathPatch(Path([(0,0)])))
    arcs_patch = ax.add_patch(patches.PathPatch(Path([(0,0)])))
    def _animate(i):
        _draw_step(i,ax, segments_done, snapshots,points_plt, segments_inprogress_patch,segments_done_patch, circle_patch, arcs_patch,d_plot, xlim, ylim, is_manhattan)
        
    return fig, _animate


from matplotlib import rcParams
import numpy as np
import matplotlib.pyplot as plt
from DataType import Point
import geometry
from matplotlib.path import Path
import matplotlib.patches as patches

import config

def draw_seg(ax, seg):
    codes = [Path.MOVETO,Path.LINETO,Path.LINETO, Path.LINETO]
    path = Path(seg, codes)
     
    patch = patches.PathPatch(path,fill=False)
    ax.add_patch(patch)  


def get_manhattan_circle_path(center,radius):
    cx,cy = center.x,center.y
    v = [(cx-radius,cy),(cx,cy-radius),(cx+radius,cy),(cx,cy+radius),(None,None)]
    codes = [Path.MOVETO,Path.LINETO,Path.LINETO, Path.LINETO,Path.CLOSEPOLY]
    return Path(v, codes)
    

def draw_circle_manhattan(ax,center,radius):
    path = get_manhattan_circle_path(center,radius)
    patch = patches.PathPatch(path,fill=False,color='red')
    ax.add_patch(patch)



def get_euclid_parabola_values(focus, directrix, left_bound , right_bound , left_y_bound,right_y_bound ):
    if focus.y == directrix:
        y_max = np.nanmin([left_y_bound, right_y_bound, config.VIEW_Y_MAX])
        return [focus.x,focus.x],[focus.y,y_max]
    else:
        x = _arrange_x(left_bound,right_bound)
        y = np.square(x-focus.x)/(2*focus.y-2*directrix)+ (focus.y+directrix)/2
        return x,y

def get_manhattan_parabola_values(focus, directrix, left_bound, right_bound, left_y_bound, right_y_bound):
    left_bound = left_bound if left_bound else -np.inf
    right_bound = right_bound if right_bound else np.inf
    left_y_bound = left_y_bound if left_y_bound else config.VIEW_Y_MAX
    right_y_bound = right_y_bound if right_y_bound else config.VIEW_Y_MAX
    
    if focus.y == directrix:
        y_max = np.nanmin([left_y_bound, right_y_bound, config.VIEW_Y_MAX])
        return [focus.x,focus.x],[focus.y,y_max]
    else:
        x = _arrange_x(left_bound,right_bound)
        y = (np.abs(focus.x - x) + focus.y + directrix)/2
        y[y>focus.y] = np.inf

        for i,( y1,y2) in  enumerate(zip(y,y[1:])):
            if np.isinf(y1) and not np.isinf(y2):
                y[i]=left_y_bound

            if np.isinf(y2) and not np.isinf(y1):
                y[i+1]=right_y_bound

                break
        return x,y

def draw_euclid_parabola(ax, focus, directrix, left_bound = -np.inf, right_bound = np.inf, left_y_bound = config.VIEW_Y_MAX, right_y_bound = config.VIEW_Y_MAX):
    x,y = get_euclid_parabola_values(focus, directrix, left_bound, right_bound, left_y_bound,right_y_bound)
    ax.plot(x,y,linestyle='-')
    
def draw_manhattan_parabola(ax, focus, directrix, left_bound = None, right_bound = None, left_y_bound =None, right_y_bound = None):
    x,y = get_manhattan_parabola_values(focus, directrix, left_bound, right_bound, left_y_bound, right_y_bound)
    ax.plot(x,y,linestyle='-')

def draw_line(ax,p1,p2,x_min,x_max,y_min,y_max,c=None,label=None):
    (r1_x,r1_y),(x1,y1),(x2,y2),(r2_x,r2_y) = geometry.get_seg(Point(*p1), Point(*p2),x_min,x_max,y_min,y_max)
    xs = [r1_x, x1, x2, r2_x]
    ys = [r1_y, y1, y2, r2_y]
    ax.plot(xs,ys,linestyle = '-', color = c, label=label, linewidth=5)
    ax.plot([p1[0],p2[0]], [p1[1],p2[1]],'x', markersize =15)
    
def _resolve_bounds(left = None,right = None):
    
    if left is None: 
        left = -np.inf
    if right is None:
        right = np.inf
    
    left_bound = left if left > -np.inf else config.VIEW_X_MIN
    right_bound = right if right < np.inf else config.VIEW_X_MAX
    
    return left_bound,right_bound
    
def _arrange_x(left_bound,right_bound):
    left,right  = _resolve_bounds(left_bound,right_bound)
    
    #return np.linspace(left,right,1000)
    return np.arange(right - left) + left
    
def get_euclid_circle_path(center,radius):
    theta = np.linspace(0, 2*np.pi, 100)
    x = radius*np.cos(theta) + center.x
    y = radius*np.sin(theta) + center.y
    v= list(zip(x,y))
    v.append((None,None))
    codes =[ Path.LINETO for _ in x[1:]]
    codes.insert(0, Path.MOVETO)
    codes.append(Path.CLOSEPOLY)

    return Path(v, codes)

def draw_euclid_circle(ax, center,radius):
    path = get_euclid_circle_path(center,radius)
    patch = patches.PathPatch(path,fill=False,color='red')
    ax.add_patch(patch)


def draw_segment_manhattan(plt,s)    :
    p1 = s[4]
    p2 = s[5]
    assert p1 and p2 , "cannot draw segment if point is missing"
    
    (x1,y1,x2,y2)=s[0],s[1],s[2],s[3]
    
    draw_line(plt, (p1.x,p1.y),(p2.x,p2.y),min(x1,x2),max(x1,x2),min(y1,y2),max(y1,y2),label=str(s[6]))


def draw_arcs(ax, arc_snapshot,directrix, intersection_fn,draw_parabola_fn):  
    LEFT_MIN = -100
    RIGHT_MAX = 600
    
    ax.axhline(directrix)
    left_intersection = Point(-np.inf,config.VIEW_Y_MAX)
    right_intersection = Point(np.inf,config.VIEW_Y_MAX)
    
    arc_foci = arc_snapshot['arc_foci']
    intersections = [intersection_fn(f1,f2,directrix) for f1,f2 in zip(arc_foci,arc_foci[1:])]
    intersections.insert(0,left_intersection)
    intersections.append(right_intersection)

    leftI_focus_rightI =  zip(intersections,arc_foci,intersections[1:])
    
    for left,focus,right in leftI_focus_rightI:
        ax.plot(focus.x,focus.y, 'x', color = 'red')
        left_x = (left or None) and left.x -1 
        left_y = (left or None) and left.y 
        right_x = (right or None) and right.x + 1
        right_y = (right or None) and right.y 
        
        draw_parabola_fn(ax,focus,directrix, left_bound = left_x, left_y_bound = left_y, right_bound = right_x, right_y_bound= right_y)
        

def draw_segment_eucl(plt,s):
    (x1,y1,x2,y2)=s[0],s[1],s[2],s[3]
    plt.plot([x1,x2],[y1,y2],linestyle='-')
    

def draw_points(ax, pts):
    for x,y in pts:
        ax.plot(x,y,'x')

def _get_beachline_points(arc_snapshot,directrix, intersection_fn,get_parabola_values):  
    LEFT_MIN = -100
    RIGHT_MAX = 600
    
    left_intersection = Point(-np.inf,config.VIEW_Y_MAX)
    right_intersection = Point(np.inf,config.VIEW_Y_MAX)
    
    arc_foci = arc_snapshot['arc_foci']
    intersections = [intersection_fn(f1,f2,directrix) for f1,f2 in zip(arc_foci,arc_foci[1:])]
    intersections.insert(0,left_intersection)
    intersections.append(right_intersection)

    leftI_focus_rightI =  zip(intersections,arc_foci,intersections[1:])
    
    parabolas =[]
    for left,focus,right in leftI_focus_rightI:
        left_x = (left or None) and left.x -1 
        left_y = (left or None) and left.y 
        right_x = (right or None) and right.x + 1
        right_y = (right or None) and right.y 
        x,y = get_parabola_values(focus,directrix, left_bound = left_x, left_y_bound = left_y, right_bound = right_x, right_y_bound= right_y)
        parabolas.append((x,y))
    return parabolas
        
def get_beachline_path(step,directrix, intersection_fn,get_parabola_values):
    beachline_parabolae = _get_beachline_points(step,directrix, intersection_fn,get_parabola_values)
        
    vs = []
    codess = []
    for x,y in beachline_parabolae:
        assert len(x) == len(y)
        if len(x) == 0:
            continue

        vs.extend(zip(x,y))
        codes =[ Path.LINETO ] * (len(x)-1)

        codes.insert(0, Path.MOVETO)
        codess.append(codes)

    codes = sum(codess,[])
    return Path(vs, codes)


def draw_intersecting_parabolae_notebook(ax,focus_1,focus_2, intersections_fn, draw_fn, title,directrix = 10):
    ax.set_xlim((-100,100))
    ax.set_ylim((0,200))
    ax.set_title(title)
    intersections =  intersections_fn(focus_1,focus_2,directrix)
    draw_fn(ax,focus_1,directrix)
    draw_fn(ax,focus_2,directrix)

    for p in intersections:
        ax.plot([p.x],[p.y],'x',color ='green')
    draw_fn(ax,focus_2, directrix, left_bound=intersections[0].x, left_y_bound =intersections[0].y  ,right_bound=intersections[1].x +1.1, right_y_bound = intersections[1].y)


def draw_circle_notebook(ax, points,draw_fn, circle_fn, title):
    
    ax.set_title(title)
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    ax.axis('equal')
    
    [ax.plot(p.x,p.y,'rx') for p in points]
    is_circle,y,p =circle_fn(*points)
    assert is_circle
    
    ax.plot(p.x,p.y,'gx')
    r = p.y - y
    draw_fn(ax,p,r)

def save_gif(path, points,is_manhattan = True):
    # path to IMAGE MAGIC (use bash `convert --version` to make sure its present)
    rcParams['animation.convert_path'] = r'/usr/bin/convert'
    myAnimation = draw_static_animation(points, is_manhattan = True)
    myAnimation.save(path, writer='imagemagick', fps=2)
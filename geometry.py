import numpy as np

from DataType import Point

import config


def _solve_parabola_for_x(x,focus,directix):
    f_x,f_y = focus.x,focus.y
    f = (f_y - directix)/2
    v_x = f_x
    v_y = f_y - f
    
    if f == 0:
        # if x is np array, it returs array
        # if its number it returns number
        type_hack = (np.abs(x) + 1 )
        return np.inf * type_hack
    return  (1/(4*f))*(np.square(x)) - (v_x/(2*f))*x + v_x**2/(4*f) + v_y

def _get_lines(p,l):
    a = p.y-l
    pts=[(p.x-a,np.inf),(p.x-a, p.y),(p.x,p.y-a/2),(p.x+a,p.y),(p.x+a,np.inf)]
    pts= [ Point(x,y) for x,y in pts]
    return list(zip(pts,pts[1:]))
    


def manhattan_distance(p1,p2):
    return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)

def euclidean_distance(p1,p2):
    return np.sqrt(np.square(p1.x -p2.x) + np.square(p1.y - p2.y))

def _ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def _seg_intersect(A,B,C,D):
    return _ccw(A,C,D) != _ccw(B,C,D) and _ccw(A,B,C) != _ccw(A,B,D)



def _get_intersect(a1,a2, b1,b2) :
    def df(a,b):
        return np.array([a.x-b.x,a.y-b.y])

    da = df(a2,a1)
    db = df(b2,b1)
    dp = df(a1,b1)
    dap = _perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    p= (num / denom.astype(float))*db + np.array([b1.x,b1.y])
    return Point(p[0],p[1])

def get_seg(a,b, x_min,x_max, y_min,y_max):
    """
    For given site points `a` and `b`, returns a bisector in manhattan matric.

    The bisector start and end can be controlled via `x_min`, `x_max`, `y_min`, `y_max`
    :param a: Site A
    :param b: Site B
    :param x_min: Crops bisector so all X are greater than `x_min`
    :param x_max: Same as `x_min` but with max
    :param y_min: Same as `x_min` but with Y
    :param y_max: Same as `x_max` but with Y
    :return: Four points of the bisector
    """
    
    x_d = np.abs(a.x - b.x)
    y_d = np.abs(a.y - b.y)
    
    x_c = (a.x + b.x)/2
    y_c = (a.y + b.y)/2
    
    if x_d > y_d: # "vertical" line
        if a.x > b.x:
            c = a
            a = b
            b = c
        x_1 = x_c + y_d/2
        x_2 = x_c - y_d/2

        y_1 = y_c + y_d/2
        y_2 = y_c - y_d/2
        
        x_dir = 1
        if a.y > b.y:
            
            p1,p2,p3,p4 = (x_2,y_min),(x_2,y_2),(x_1,y_1),(x_1,y_max)
            # with / slant
        else:
            x_dir = -1
            # with \ slant
            p1,p2,p3,p4 = (x_1,y_min),(x_1,y_2),(x_2,y_1),(x_2,y_max)
            
        
        
        if y_2 > y_max:
            # cut bottom vertical segment
            p2 = ( p1[0], y_max)
            p3 = p2
            p4 = p2
        elif y_1 < y_min:
            # cut the top vertical segment
            p3 = (p4[0], y_min)
            p2 = p3
            p1 = p3
        else:
            # cut in the slanted part
            if y_max < y_1:
                # from top
                p3_diff =y_max - y_1
                p3 = (p3[0] + p3_diff*x_dir, y_1+p3_diff)
                p4 = p3

            if y_min > y_2:
                # from bottom
                p2_diff = y_min - y_2
                p1 =(p2[0] + p2_diff*x_dir, y_2 + p2_diff)
                p2 = p1

        return p1,p2,p3,p4
        
    elif np.abs(x_d) < np.abs(y_d): # "horizontal" line
        if a.y > b.y:
            c = a
            a = b
            b = c
        x_1 = x_c + x_d/2
        x_2 = x_c - x_d/2

        y_1 = y_c + x_d/2
        y_2 = y_c - x_d/2
        
        y_dir = 1 
        if a.x < b.x:
            y_dir = -1
            p1,p2,p3,p4 = (x_min,y_1),(x_2,y_1),(x_1,y_2),(x_max,y_2)
        else:
            p1,p2,p3,p4 = (x_min,y_2),(x_2,y_2),(x_1,y_1),(x_max,y_1)
    
        if x_2 > x_max:
            # cut left horizontal segment
            p2 = ( x_max, p1[1])
            p3 = p2
            p4 = p2
        elif x_1 < x_min:
            # cut the right horizontal segment
            p3 = (x_min, p4[1])
            p2 = p3
            p1 = p3
        else:
            if x_max < x_1:
                # from right
                p2_diff =x_max - x_2
                p3 = (x_2 + p2_diff, p2[1]+p2_diff*y_dir)
                p4 = p3
                
            if x_min > x_2:
                # from left
                p2_diff = x_min- x_2
                p1 =(x_2 + p2_diff, p2[1] + p2_diff*y_dir)
                p2 = p1
            
        return p1,p2,p3,p4
        
    else: # diagonal
        
        # ensure that left point is (a)
        if a.x>b.x:
            c = a
            a = b
            b = c
    
        left_offset = x_c - x_min
        bottom_offset = y_c - y_min
        right_offset = x_c - x_max
        top_offset = y_c - y_max
        
        x_dir = 1
        if a.y < b.y: # direction -> \
                        # top left
            if np.abs(left_offset) <= np.abs(top_offset):
                shift_left =  -left_offset
            else:
                shift_left =  top_offset
            
            # bottom right
            if np.abs(right_offset) <= np.abs(bottom_offset):
                shift_right = -right_offset
            else:
                shift_right= bottom_offset
            
            x_dir = -1
            
        else : # direction -> /
            
            if np.abs(left_offset) <= np.abs(bottom_offset):
                shift_left = left_offset
            else:
                shift_left = bottom_offset
                
            if np.abs(right_offset) <= np.abs(top_offset):
                shift_right = right_offset
            else:
                shift_right = top_offset
                
        start_x = x_c - shift_left * x_dir
        end_x = x_c - shift_right * x_dir   
        start_y = y_c - shift_left
        end_y = y_c - shift_right
           
        return (start_x,start_y),(start_x,start_y),(end_x,end_y),(end_x,end_y)

def get_parabolae_intersection_manhattan(p0,p1,l):
    p0_seg_points = _get_lines(p0,l)
    p1_seg_points = _get_lines(p1,l)
    
    intersections = []
    for u1,u2 in p0_seg_points:
        for v1,v2 in p1_seg_points:
            
            #TODO resolve infites values
            # replase inf in Y coordinates by max Y -> should not harm generality
            
            u1,u2,v1,v2 = _resolve_inf([u1,u2,v1,v2])
            
            if _seg_intersect(u1,u2,v1,v2): 
                
                intersectio= _get_intersect(u1,u2,v1,v2)
                intersections.append(intersectio)


    return intersections


def is_right_turn(a,b,c):
    """b point must be in the middle"""
    return ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0

def circle_euclid(c,b,a):
    
    
    if is_right_turn(c,b,a): return False, None, None

    # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
    A = b.x - c.x
    B = b.y - c.y
    C = a.x - c.x
    D = a.y - c.y
    E = A*(c.x + b.x) + B*(c.y + b.y)
    F = C*(c.x + a.x) + D*(c.y + a.y)
    G = 2*(A*(a.y - b.y) - B*(a.x - b.x))

    if (G == 0): return False, None, None # Points are co-linear

    # point o is the center of the circle
    ox = 1.0 * (D*E - B*F) / G
    oy = 1.0 * (A*F - C*E) / G

    # o.y - radius equals min y coord
    y = oy - np.sqrt((c.x-ox)**2 + (c.y-oy)**2)
    o = Point(ox, oy)

    return True, y, o


def _is_coliear(a,b,c):
    den1 = (b.y-a.y)
    if den1==0:
        return True
    slope1=(b.x-a.x)/den1
    
    den2 =(c.y-b.y)
    if den2==0:
        return True
    slope2=(c.x-b.x)/den2
    
    diff = np.abs(slope1 - slope2)
    
    
    threshold = .001
    return diff < threshold

def is_clockwise(a,b,c):
    return ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0
    
def circle_manhattan(a,b,c):
    if _is_coliear(a,b,c):
        return False, None, None
    
    if is_right_turn(a,b,c):
        return False, None, None
    
    points = [a,b,c]

    polylines = [ get_seg(points[i],points[j],config.VIEW_X_MIN,config.VIEW_X_MAX,config.VIEW_Y_MIN,config.VIEW_Y_MAX) for i,j in [ (0,1),(1,2),(2,0)]  ]    
    center = get_circle_center(polylines)
    if center is None:
        return False, None, None
    
    radius = manhattan_distance(center, a)
    
    y = center.y - radius
    
    return True, y, center

def _perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def get_circle_center(polylines):
    p1,p2,p3 = polylines
    
    for a,b in [(p1,p2),(p2,p3),(p1,p3)]:
        intersection = get_polylines_intersection(a,b)
        if intersection is not None:
            return intersection
    
    return None

def get_polylines_intersection(p1,p2):
    p1_segs = list(zip(p1,p1[1:]))
    p2_segs = list(zip(p2,p2[1:]))
    all_segs = [(s1,s2) for s1 in p1_segs for s2 in p2_segs]
    for (s1_1,s1_2),(s2_1,s2_2) in all_segs:
        x1,y1 = s1_1
        p1_1 = Point(x1,y1)
        x2,y2 = s1_2
        p1_2 = Point(x2,y2)
        x3,y3 = s2_1
        p2_1 = Point(x3,y3)
        x4,y4 = s2_2
        p2_2 = Point(x4,y4)
        if _seg_intersect(p1_1,p1_2,p2_1,p2_2):              
            return _get_intersect(p1_1,p1_2,p2_1,p2_2)
    return None


def get_circle_center(polylines):
    p1,p2,p3 = polylines
    
    for a,b in [(p1,p2),(p2,p3),(p1,p3)]:
        intersection = get_polylines_intersection(a,b)
        if intersection is not None:
            return intersection
    
    return None

def get_parabolae_intersection_euclid(focus_1,focus_2,directix):
    
    f_x_1,f_y_1 = focus_1.x, focus_1.y
    f_x_2,f_y_2 = focus_2.x, focus_2.y
    
    # this is the key piece for manhattan as well
    if (f_y_1 == f_y_2):
        i_x = (f_x_1 + f_x_2) / 2.0
        i_y = _solve_parabola_for_x(i_x,focus_2, directix)
        return [Point(i_x,i_y)]
    elif f_y_1 == directix:
        i_x = f_x_1
        i_y = _solve_parabola_for_x(i_x,focus_2, directix)
        return [Point(i_x,i_y)]
    elif f_y_2 == directix:
        i_x = f_x_2
        i_y = _solve_parabola_for_x(i_x,focus_1, directix)
        return [Point(i_x,i_y)]
    
    f_1 = (f_y_1 - directix)/2
    f_2 = (f_y_2 - directix)/2
    
    v_x_1 = f_x_1
    v_y_1 = f_y_1 - f_1
    
    v_x_2 = f_x_2
    v_y_2 = f_y_2 - f_2
    
    # y = a*x^2 + b x*x + c
    
    a = (1/(4*f_1) - 1/(4*f_2))
    b = -(v_x_1/(2*f_1) - v_x_2/(2*f_2))
    c = (v_x_1**2/(4*f_1) - v_x_2**2/(4*f_2)) + (v_y_1 - v_y_2)
    
    bac = b**2 - 4*a*c
    if bac < 0:
        return []
    
    sq_bac = np.sqrt(bac)
    
    x_1 = (-b - sq_bac)/(2*a)
    x_2 = (-b + sq_bac)/(2*a)
    
    x_l,x_r =  min([x_1,x_2]) ,max([x_1,x_2])
    y_1 = _solve_parabola_for_x(x_l,focus_1, directix)
    y_2 = _solve_parabola_for_x(x_r,focus_1, directix)
    return [Point(x_l, y_1 ),Point(x_r,y_2)]


def _resolve_inf(points):
        
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf 
    
    def _min_inf(a,b):
        if np.isinf(a):
            return b
        if np.isinf(b):
            return a
        
        return min(a,b)
    
    def _max_inf(a,b):
        if np.isinf(a):
            return b
        if np.isinf(b):
            return a
        
        return max(a,b)
    
    for p in points:
        x_min = _min_inf(p.x, x_min)
        x_max = _max_inf(p.x, x_max)
        y_min = _min_inf(p.y, y_min)
        y_max = _max_inf(p.y, y_max)
        
    
    
    
    def resolve_p(point):
        
        if point.x>=0:
            x = _min_inf(point.x, x_max)
        else:
            x = _max_inf(point.x, x_min)
            
        if point.y>=0:
            y = _min_inf(point.y, y_max)
        else:
            y = _max_inf(point.y, y_min)
            
        return Point(x,y)
    
    
    return [ resolve_p(p) for p in points]
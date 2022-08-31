import config
from DataType import Arc,Event, Segment, Point
import arc_utils
import geometry
import numpy as np

def voronoi_check_circle_event(arc, events, circle_fn):
    
    if arc is None:
        return
    if (arc.e is not None):
        arc.e.valid = False
    arc.e = None
    if (arc.pprev is None) or (arc.pnext is None): return

    is_circle, y, o = circle_fn(arc.pprev.p, arc.p, arc.pnext.p)
    if is_circle:
        arc.e = Event(y, o, arc)
        events.push(arc.e)


def _check_circle_events_around(arc,events):
    voronoi_check_circle_event(arc, events, geometry.circle_manhattan)
    voronoi_check_circle_event(arc.pprev,  events, geometry.circle_manhattan)
    voronoi_check_circle_event(arc.pnext,  events, geometry.circle_manhattan)

def voronoi_arc_insert_eucl(arc, point,output,events,logger = None):
    if arc is None:
        return Arc(point)
        
    # find the current arcs at p.y
    i = arc_utils._get_top_left_arc(arc)
    while i is not None:
       
        is_intersected, z = EuclideanMetric.intersect(point, i)
            
        if is_intersected:
            # new parabola intersects arc i
            is_intersected, zz = EuclideanMetric.intersect(point, i.pnext)
            
            if (i.pnext is not None) and (not is_intersected):
                i.pnext.pprev = Arc(i.p, i, i.pnext)
                i.pnext = i.pnext.pprev
            else:
                i.pnext = Arc(i.p, i)
            i.pnext.s1 = i.s1

            # add p between i and i.pnext
            i.pnext.pprev = Arc(point, i, i.pnext)
            i.pnext = i.pnext.pprev

            i = i.pnext # now i points to the new arc

            # add new half-edges connected to i's endpoints
            seg = Segment(z,site1 = i.pprev.p,site2=i.p)
            output.append(seg)
            i.pprev.s1 = i.s0 = seg
                        
            seg = Segment(z,site1=i.p, site2=i.pnext.p)
            output.append(seg)
            i.pnext.s0 = i.s1 = seg

            # check for new circle events around the new arc
            voronoi_check_circle_event(i, events, EuclideanMetric.circle)
            voronoi_check_circle_event(i.pprev,  events, EuclideanMetric.circle)
            voronoi_check_circle_event(i.pnext,  events, EuclideanMetric.circle)

            return i

        i = i.pnext

    # if p never intersects an arc, append it to the list
    i = arc
    while i.pnext is not None:
        i = i.pnext
    i.pnext = Arc(point, i)

    # insert new segment between p and i
    x = (i.pnext.p.x + i.p.x) / 2.0;
    start = Point(x, VIEW_Y_MAX)

    seg = Segment(start,site1=i.p,site2=i.pnext.p)
    i.s1 = i.pnext.s0 = seg
    output.append(seg)
    return i

def manhattan_insert_arc(arc, point, output,events,logger = None):
    if arc is None:
        return Arc(point)

    current_arc = arc_utils._get_top_left_arc(arc)
    while current_arc is not None:

        action, intersection = ManhattanMetric.intersect(point, current_arc)
        
        if action == "split_current_arc":
            new_arc, left_seg,right_seg = arc_utils._split_current_arc(current_arc,point,intersection)
            output.append(left_seg)
            output.append(right_seg)
            _check_circle_events_around(new_arc,events)
            
            return new_arc
        elif action == 'add_to_left':
            new_arc, segment = arc_utils._add_to_left(current_arc,point,intersection)
            output.append(segment)

            _check_circle_events_around(new_arc,events)
            return new_arc

        elif action == 'add_to_right':
            new_arc, segment = arc_utils._add_to_right(current_arc,point,intersection)
            output.append(segment)

            _check_circle_events_around(new_arc,events)
            return new_arc
        
        current_arc = current_arc.pnext

    return arc


def _get_parabola_domain_min_max(focus, directrix):        
    latus_rectum = (focus.y - directrix)
    return focus.x - latus_rectum, focus.x + latus_rectum
    
def _resolve_intersection_boundaries(prev_arc,current_arc,next_arc,directrix):
    
    if prev_arc is not None:
        left_boundary_p = ManhattanMetric.intersection(prev_arc.p, current_arc.p, directrix)
        if left_boundary_p is None:
            _,closes_pt = _get_parabola_domain_min_max(prev_arc.p, directrix)
            left_boundary_x = closes_pt
        else:
            left_boundary_x = left_boundary_p.x
    else:
        left_boundary_x = -np.inf

    if next_arc is not None:
        right_boundary_p = ManhattanMetric.intersection(current_arc.p, next_arc.p, directrix)
        if right_boundary_p is None:
            closes_pt,_ = _get_parabola_domain_min_max(next_arc.p, directrix)
            right_boundary_x = closes_pt
        else:
            right_boundary_x = right_boundary_p.x
    else:
        right_boundary_x = np.inf

    return left_boundary_x, right_boundary_x


class ManhattanMetric:
    
    def insert_arc(arc, point, output,events,logger = None):
        return manhattan_insert_arc(arc,point,output,events,logger=logger)
    
    def point_dist(p1,p2):
        return geometry.manhattan_distance(p1,p2)
        
        
    def intersect(p, i):         
        assert i is not None
                
        #_get_parabola_domain_min_max
        directrix = p.y
        left_boundary_x,right_boundary_x = _resolve_intersection_boundaries(i.pprev,i,i.pnext,directrix)
        arc_intersection = ManhattanMetric.intersection(p, i.p, p.y)
        if arc_intersection:
            # px whould be within to be considered new arc
            if left_boundary_x < p.x and p.x < right_boundary_x:
                return "split_current_arc", arc_intersection
            
        elif p.x < i.p.x and p.x > left_boundary_x: 
            # point must be in the  empty space between two arcs
            #this case should not happen as it would have been solved by the 
            # add_right within previous arc
            if i.pprev is None or p.x > i.pprev.p.x:
                # this parabolae is placed on the left side
                fake_intersection = Point(p.x, config.VIEW_Y_MAX)
                return 'add_to_left', fake_intersection
        
        elif p.x > i.p.x and p.x < right_boundary_x: # point added to the right of the current arc
            # point must be in the  empty space between two arcs
            if i.pnext is None or p.x < i.pnext.p.x:
                fake_intersection = Point(p.x, config.VIEW_Y_MAX)
                return 'add_to_right', fake_intersection
        
        return None,None   

        
    def intersection(p0, p1, l):        
        intersections =  geometry.get_parabolae_intersection_manhattan(p0,p1,l)
        if len(intersections) == 2:
            i1,i2 = intersections
            if p0.y > p1.y:
                return i1
            else:
                return i2
        elif len(intersections) == 1:
            return intersections[0]
        else: 
            return None
    
    def circle(a, b, c):
        return geometry.circle_manhattan(a,b,c)   

class EuclideanMetric:
    
    def insert_arc(arc, point, output,events,logger = None):
        return voronoi_arc_insert_eucl(arc,point,output,events,logger=logger)
    
    def point_dist(p1,p2):    
        return euclidean_distance(p1,p2)
        
    def intersect(p, i):         
        # check whether a new parabola at point p intersect with arc i
        if (i is None): return False, None
        if (i.p.y == p.y): return False, None

        prev_intersection_x = 0.0
        next_intersection_x = 0.0

        # this can be improved via get_euclid_intersections
        if i.pprev is not None:
            prev_intersection_x = (EuclideanMetric.intersection(i.pprev.p, i.p, p.y)).x
        if i.pnext is not None:
            next_intersection_x = (EuclideanMetric.intersection(i.p, i.pnext.p, p.y)).x

        if (((i.pprev is None) or (prev_intersection_x <= p.x)) and ((i.pnext is None) or (p.x <= next_intersection_x))):
            
            px = p.x
            
            py = 1.0 * ((i.p.y)**2 + (i.p.x-px)**2 - p.y**2) / (2*i.p.y - 2*p.y)
            res = Point(px, py)
            return True, res
        
        return False, None
    
    def intersection(p0, p1, l):
        
        intersections = geometry.get_parabolae_intersection_euclid(p0,p1,l)
        if len(intersections) == 2:
            i1,i2 = intersections
            if p0.y > p1.y:
                return i1
            else:
                return i2
        elif len(intersections) == 1:
            return intersections[0]
        else: 
            raise Exception("This can't happen in euclid space")
        
    def circle(a, b, c):
        return geometry.circle_euclid(a,b,c)
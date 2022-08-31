from DataType import Arc, Segment, Point

import config

def _get_top_left_arc(arc):
    c_arc = arc
    while c_arc.pprev:
        c_arc = c_arc.pprev
    return c_arc
    
def arc_to_list(arc):
    foci = []
    tl = _get_top_left_arc(arc)
    while tl:
        foci.append(tl.p)
        tl = tl.pnext
    return foci


def create_beachline(points):
    """Creates beachline with arcs in order of the points with fake segments"""
    prev_arc = Arc(Point(*points[0]))
    for x,y in points[1:]:
        point= Point(x,y)
        arc = Arc(point)
        prev_arc.pnext = arc
        arc.pprev = prev_arc
        
        seg = Segment(Point(0,0), site1=prev_arc,site2=arc)
        arc.s0 = seg
        prev_arc.s1 = seg
        prev_arc = arc
        
    return _get_top_left_arc(prev_arc)
        

def iterate_arcs(arc):
    start_arc = _get_top_left_arc(arc)
    
    while start_arc:
        yield start_arc
        start_arc = start_arc.pnext


def _split_current_arc(current_arc, point,intersection):
    
    new_arc_middle = Arc(point)
    
    current_arc_left_part = Arc(current_arc.p, pprev = current_arc.pprev, pnext = new_arc_middle)
    if current_arc.pprev:
        current_arc.pprev.pnext = current_arc_left_part
    current_arc_left_part.s0 = current_arc.s0

    current_arc_right_part = Arc(current_arc.p, pprev = new_arc_middle, pnext = current_arc.pnext)
    if current_arc.pnext:
        current_arc.pnext.pprev = current_arc_right_part
    current_arc_right_part.s1 = current_arc.s1

    new_arc_middle.pprev = current_arc_left_part
    new_arc_middle.pnext = current_arc_right_part
    
    left_seg = Segment(intersection,site1 = new_arc_middle.pprev.p,site2=point)
    current_arc_left_part.s1 = left_seg
    new_arc_middle.s0 = left_seg
    
    right_seg = Segment(intersection,site1=point, site2=new_arc_middle.pnext.p)
    current_arc_right_part.s0 = right_seg
    new_arc_middle.s1 = right_seg
    
    return new_arc_middle, left_seg,right_seg


def _add_to_right(current_arc,point,intersection):
    
    original_right_arc = current_arc.pnext
    old_segment = current_arc.s1
    new_arc = Arc(point)
    
    new_arc.pnext = current_arc.pnext
    current_arc.pnext = new_arc
    new_arc.pprev = current_arc
    
    shared_segment = Segment(intersection, site1 = new_arc.p, site2 = current_arc.p)
    
    
    new_arc.s0 = shared_segment
    current_arc.s1 = shared_segment
    
    if original_right_arc:
        original_right_arc.pprev = new_arc
        
        old_segment.start = Point((original_right_arc.p.x+new_arc.p.x)/2, config.VIEW_Y_MAX)
        new_arc.s1 = old_segment
        old_segment.site2 = original_right_arc.p
        old_segment.site1 = new_arc.p
    
    return new_arc, shared_segment

def _add_to_left(current_arc,point,intersection):
    original_left_arc = current_arc.pprev
    old_segment = current_arc.s0
    
    new_arc = Arc(point)
    
    new_arc.pprev = original_left_arc
    current_arc.pprev = new_arc
    
    new_arc.pnext = current_arc
    
    shared_segment = Segment(intersection, site1 = new_arc.p, site2 = current_arc.p)
    new_arc.s1 = shared_segment
    current_arc.s0 = shared_segment
    
    if original_left_arc:
        original_left_arc.pnext = new_arc
        
        old_segment.start = Point((original_left_arc.p.x+new_arc.p.x)/2, config.VIEW_Y_MAX)
        new_arc.s0 = old_segment
        old_segment.site1 = original_left_arc.p
        old_segment.site2 = new_arc.p
    
    return new_arc, shared_segment
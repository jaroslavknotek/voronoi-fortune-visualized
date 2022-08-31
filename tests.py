
import numpy as np
from DataType import Segment , Arc, Point
from arc_utils import _add_to_left,_add_to_right,_split_current_arc

import config
import metrics
import arc_utils

def test_split_current_arc():

    arc_l  = Arc(Point(-10,1))
    arc_r  = Arc(Point(10,1))
    arc_c   = Arc(Point(0,1), pnext=arc_r, pprev = arc_l)
    
    arc_l.pnext = arc_c
    arc_r.pprev = arc_c
    
    point = Point(2,1)
    intersection = Point(2,2)
    new_arc,left_seg,right_seg = _split_current_arc(arc_c,point,intersection)
    
    assert new_arc.p == point
    
    left_half_arc = new_arc.pprev
    right_half_arc = new_arc.pnext
    
    assert left_half_arc.p == arc_c.p
    assert right_half_arc.p == arc_c.p
    
    
    assert left_half_arc.pprev == arc_l
    assert left_half_arc.pnext == new_arc
    
    assert right_half_arc.pnext == arc_r
    assert right_half_arc.pprev == new_arc
    
    assert left_seg != right_seg
    assert left_seg.start == intersection
    assert right_seg.start == intersection
    
def test_split_current_arc_solo():

    arc_c   = Arc(Point(0,1))
        
    point = Point(2,1)
    intersection = Point(2,2)
    new_arc,left_seg,right_seg = _split_current_arc(arc_c,point,intersection)
    
    assert new_arc.p == point
    
    left_half_arc = new_arc.pprev
    right_half_arc = new_arc.pnext
    
    assert left_half_arc.p == arc_c.p
    assert right_half_arc.p == arc_c.p
        
    assert left_seg != right_seg
    assert left_seg.start == intersection
    assert right_seg.start == intersection

   
def test_add_to_right():
    arc_r = Arc(Point(10,1))
    arc_c = Arc(Point(0,1), pnext = arc_r)
    arc_r.pprev = arc_c
    original_segment =  Segment(Point(5,100),site1=arc_r.p,site2=arc_c.p)
    arc_r.s0 = original_segment
    arc_c.s1 = original_segment
    
    intersection = Point(2,2)
    point = Point(2,1)
    
    arc, seg  = _add_to_right(arc_c,point ,intersection)
    
    assert arc_r.pprev ==arc
    assert arc.pnext == arc_r
    assert arc_c.pnext == arc
    assert arc.pprev == arc_c
    assert seg.start == intersection
        
    assert seg.site1 in [point, arc_c.p]
    assert seg.site2 in [point, arc_c.p]
    
    assert original_segment.site1 in [arc_r.p, point]
    assert original_segment.site2 in [arc_r.p, point]
    assert original_segment.start.x != 5
        
def test_add_to_left_solo():
    arc_c = Arc(Point(0,1))
    intersection = Point(2,2)
    point = Point(2,1)
    arc, seg  = _add_to_left(arc_c,point ,intersection)
    
    
    assert arc.pnext == arc_c
    assert arc_c.pprev == arc
    assert seg.start == intersection
        
    assert seg.site1 in [point, arc_c.p]
    assert seg.site2 in [point, arc_c.p]
    
def test_add_to_right_solo():
    arc_c = Arc(Point(0,1))
    intersection = Point(2,2)
    point = Point(2,1)
    
    arc, seg  = _add_to_right(arc_c,point ,intersection)
    
    assert arc_c.pnext == arc
    assert arc.pprev == arc_c
    assert seg.start == intersection
        
    assert seg.site1 in [point, arc_c.p]
    assert seg.site2 in [point, arc_c.p]



def test_add_to_left():
    arc_l = Arc(Point(10,1))
    arc_c = Arc(Point(0,1), pprev = arc_l)
    arc_l.pnext = arc_c
    
    original_segment =  Segment(Point(5,100),site1=arc_l.p,site2=arc_c.p)
    arc_l.s1 = original_segment
    arc_c.s0 = original_segment
    
    intersection = Point(2,2)
    point = Point(2,1)
    
    new_arc, seg  = _add_to_left(arc_c,point ,intersection)
    
    assert arc_l.pnext == new_arc
    assert new_arc.pprev == arc_l
    assert arc_c.pprev == new_arc
    assert new_arc.pnext == arc_c
    assert seg.start == intersection
        
    assert seg.site1 in [point, arc_c.p]
    assert seg.site2 in [point, arc_c.p]
    
    assert original_segment.site1 in [arc_l.p, point]
    assert original_segment.site2 in [arc_l.p, point]
    assert original_segment.start.x != 5
    assert original_segment.start.y == config.VIEW_Y_MAX


def test_get_parabola_domain_min_max( ):
    
    focus = Point(478.4746681375584 , 68.60466067803821)
    directrix = 16.710713813172294
    l,r = metrics._get_parabola_domain_min_max(focus, directrix)
    
    assert l == focus.x - (focus.y - directrix)
    assert r == focus.x + (focus.y - directrix)
    
def test_resolve_intersectin_boundaries():
    
    pts= [
        [131.65750759256733 , 266.8696966901489],
        [478.4746681375584 , 68.60466067803821]]        

    test_arcs =  arc_utils.create_beachline(pts)
    next_point = Point(450.3574270585061 , 16.710713813172294)
    left,right = metrics._resolve_intersection_boundaries(test_arcs.pprev, test_arcs,test_arcs.pnext, next_point.y)
    assert left < 0 and np.isinf(left)
    assert right > 0 and not np.isinf(right)
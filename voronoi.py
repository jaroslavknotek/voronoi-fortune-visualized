import logging
from DataType import PriorityQueue, Point, Segment
import config
import arc_utils
import metrics

class VoronoiPlt:
    def __init__(self, points, metric = None, remember_steps=True):
        self.logger = logging.getLogger("voronoi")
        self.remember_steps = remember_steps
        self.steps = []
        
        self.output = [] # list of line segment
        self.arc = None  # binary tree for parabola arcs

        self.points = PriorityQueue() # site events
        self.event = PriorityQueue() # circle events
        
        if metric is None:
            self.metric = metrics.EuclideanMetric
        else:
            self.metric = metric
            
        # bounding box
        self.x0 = config.VIEW_X_MIN
        self.x1 = config.VIEW_X_MAX
        self.y0 = config.VIEW_Y_MIN
        self.y1 = config.VIEW_Y_MAX

        # insert points to site event
        for pts in points:
            point = Point(pts[0], pts[1])
            self.points.push(point)
            # keep track of bounding box size
            if point.x < self.x0: self.x0 = point.x
            if point.y < self.y0: self.y0 = point.y
            if point.x > self.x1: self.x1 = point.x
            if point.y > self.y1: self.y1 = point.y

        # add margins to the bounding box
        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy
    
           
        
    
    def _save_step(self,step_type,directrix,arc, circle_event=None,site = None):
        if not self.remember_steps:
            return
        
        o = self.get_output(filter_incomplete=True)
        
        in_progress = []
        
        for a1,a2 in zip(arc_utils.iterate_arcs(arc),list(arc_utils.iterate_arcs(arc))[1:]):
            
            intersection = self.metric.intersection(a1.p,a2.p,directrix)
            if intersection is not None:
                p0 = a1.s1.start
                p1 = intersection
                seg = (p0.x, p0.y, p1.x, p1.y, a1.p,a2.p, id(a1.s1) )
                in_progress.append(seg)
        
        foci = arc_utils.arc_to_list(arc)
        
        snapshot = {
            "step_type": step_type,
            "directrix": directrix,
            "arc_foci":foci,
            "output":o,
            'in_progress':in_progress
        }
        if site:
            snapshot['site'] = site
        
        if circle_event:
            center,r = circle_event
            snapshot['radius'] = r
            snapshot['center'] = center
                
        self.steps.append(snapshot)
        
        
    
    def process(self):
        while not self.points.empty():
            if not self.event.empty() and (self.event.top().y >= self.points.top().y):
                dx = self.event.top().y
                
                valid = self.event.top().valid
                circle_event = self._process_event() # handle circle event
                if valid:
                    self._save_step('Circle Event',dx,self.arc, circle_event = circle_event)
            else:
                point = self.points.top()
                self._process_point() # handle site event
                self._save_step('Site Event',point.y,self.arc, site= point)

        # after all points, process remaining circle events
        while not self.event.empty():
            dx = self.event.top().y
            #self._save_step('before circle',dx,self.arc)
            valid = self.event.top().valid
            circle_event = self._process_event() # handle circle event
            if valid:
                self._save_step('Circle Event',dx,self.arc, circle_event = circle_event)

        self.finish_edges()

    def _process_point(self):
        # get next event from site pq
        p = self.points.pop()
        # add new arc (parabola)
        self.arc_insert(p)
        

    def _process_event(self):
        # get next event from circle pq
        e = self.event.pop()
        
        if e.valid:
            # start new edge
                        
            s = Segment(e.p, site1=e.a.pprev.p, site2=e.a.pnext.p )
            self.output.append(s)

            _, y, center = self.metric.circle(e.a.pprev.p,e.a.p,e.a.pnext.p)
            
            # remove associated arc (parabola)
            a = e.a
            if a.pprev is not None:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext is not None:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s

            # finish the edges before and after a
            if a.s0 is not None: a.s0.finish(e.p)
            if a.s1 is not None: a.s1.finish(e.p)

            # recheck circle events on either side of p
            if a.pprev is not None: self.check_circle_event(a.pprev)
            if a.pnext is not None: self.check_circle_event(a.pnext)
            
            return center, center.y - y
                
            

    def arc_insert(self, p):
        self.arc = self.metric.insert_arc(self.arc, p, self.output,self.event )

    def check_circle_event(self, i):
        metrics.voronoi_check_circle_event(i, self.event, self.metric.circle)

    def finish_edges(self):
        l = -(self.y0 + (self.x1 - self.x0) + (self.y1 - self.y0))
        i = arc_utils._get_top_left_arc(self.arc)        
        while i.pnext is not None:
            if i.s1 is not None:
                p = self.metric.intersection(i.p, i.pnext.p, l*2.0)                
                i.s1.finish(p)
                self.logger.debug("s0",i.s0)
                self.logger.debug("s1", i.s1)
            i = i.pnext

    def get_output(self, filter_incomplete = False):
        res = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            if not p1:
                if not filter_incomplete:
                    p1 = p0
                else: 
                    continue
            res.append((p0.x, p0.y, p1.x, p1.y, o.site1,o.site2, id(o) ))
        return res

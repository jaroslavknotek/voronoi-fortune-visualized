# Credits to jansonh https://github.com/jansonh/Voronoi 

import heapq
import itertools

class Point:
   x = 0.0
   y = 0.0
   
   def __init__(self, x, y):
       self.x = x
       self.y = y
        
   def __str__(self):
       return f"[{self.x} , {self.y}]"

   def __repr__(self):
       return f"Point({self.x},{self.y})"

class Event:
    y = 0.0
    p = None
    a = None
    valid = True
    
    def __init__(self, y, p, a):
        self.y = y
        self.p = p
        self.a = a
        self.valid = True

class Arc:
    p = None
    pprev = None
    pnext = None
    e = None
    s0 = None
    s1 = None
    
    def __init__(self, p, pprev=None, pnext=None):
        self.p = p
        self.pprev = pprev
        self.pnext = pnext
        self.e = None
        self.s0 = None
        self.s1 = None

    def __str__(self):
        return f"A p: {self.p}"

    def __repr__(self):
        return f"Arc({self.p}, {self.pprev}, {self.pnext})"

class Segment:
    start = None
    end = None
    done = False
    
    def __init__(self, p, site1=None,site2=None):
        assert p
        self.start = p
        self.site1 =site1
        self.site2 = site2
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done: return
        self.end = p
        self.done = True 
        
    def __str__(self):

        return f"start:{self.start}, end:{self.end},done:{self.done}. id: {id(self)}"


class PriorityQueue:
    def __init__(self,is_max = True):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()
        self.is_max = is_max

    def push(self, item):
        # check for duplicate
        if item in self.entry_finder: return
        count = next(self.counter)
        # use y-coordinate as a primary key (heapq in python is min-heap)
        if self.is_max:
            entry = [-item.y, count, item]
        else:
            entry = [item.y, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove_entry(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = 'Removed'

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item != 'Removed':
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item != 'Removed':
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def empty(self):
        return not self.pq

            

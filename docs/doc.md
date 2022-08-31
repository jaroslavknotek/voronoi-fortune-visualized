# Structure

This project has three distinct layers
- Visualization
- Algorithmic
- Math

## Visualization

This layer visualizes results of the algorithm using [matplotlib](matplotlib.org). Using this library to visualize data is not common but in this case, it was just enough. It allowed to draw all the results, animate them and even create interactive plots. If you want it nice, fully interactive customizable, choose something else. 

Responsible code
- [drawing.py](../drawing.py) - Draws objects on a given plot
- [animate_voronoi.py](../animate_voronoi.py) - Script running and visualizing Voronoi using matplotlib FuncAnimation and interactive plots
- [animplayer.py](../animplayer.py) - Code running the animations
- [notebook](../notebooks/fortune-visualisation.ipynb) - Notebook where the animation run
- [config.py](../config.py) - file containing settings for the viewport
  
## Algorithmic

This part contains Fortune algorithm that can work with two (possibly more) metrics. It has a common part and then metric specific ones. User pick metric that is desired which then gets plugged to the common part (this way you can add other metrics). 

Notable code
- [voronoi.py](../voronoi.py) - Common part for the Fortune algorithm.
- [metrics.py](../metrics.py) - Code specific to Euclidean and Manhattan metrics. One of them is plugged to the common part.
- [arc_utils.py](../arc_utils.py) - Utils handling beach line and individual arcs that's not specific to metrics. 
- [DataType.py](../DataType.py) - Objects representing main data of the algorithm (segments, points, ...)

## Math

There is only one file [geometry.py](../geometry.py). This file contains all code responsible for calculation of intersection, parabolae, circles. It contains the code that should not be part of the algorithm itself. 


# Lessons Learned

## Achievements

- Having visualized something as strange as Fortune in manhattan metrics helps overcome unintuitive notion of non-euclidean geometry.
- I utilized parts of matplotlib and jupyter I didn't know they existed. The drawing is done mostly by using patches which helps greatly with overcoming issues in animation. You can't just draw or plot something. You need to initialize plots before animation takes place and then plug in different data each frame. You can't dynamically add more than you have previously initialized. Even though it was great to not adding different dependency. However, it may not worth it. Definitely not in production.
- Having the same code working for two different metrics is a challenge. You need to identify the assumptions that are common to both, and integrate the to the base code, as well as the assumptions that differ and create metric-specific code paths. The most interesting thing is how beachline differ. In euclidean space, beach line is a continuous function covering whole domain. In manhattan, it's not. If you want to add next parabola, you need to handle the case when parabola doesn't intersect beachline (which doesn't happen in euclidean space).

## Problems

- This tasks contains numerous software engineering no-nos that stems from multiple bad decision.

  1. Underestimation - This task will be just few days of work. This created false hope and unnecessary hurry.
  2. Overestimation - I remember the algorithm I am supposed well enough. I don't have to read the solution I am about to extend.
  3. Development Environment - Assumption that visual tasks require visual development. Wrong. Instead of developing the whole solution in jupyter notebooks. I should have created normal solution. Write some code and test it right away. It may have cleared many misunderstanding and fix a lot of bugs thus saving many hours.

- Geometry is coupled to viewport. I can't work with rays (only segments) so it needs to have some bounds. Infinite plane won't work. that's pretty bad as you have to pass information about viewport to the geometry class as well.

- There is a similar project [here](https://github.com/Yatoom/foronoi) which looks more professional. Maybe it would have been better to extend it, instead of coming up with my own solution.

- Separate metrics have more in common then its reflected in the code. Writing this stuff again, I will probably manage to merge them more. For example forming beachline is more general in manhattan and more specific in euclidean. I believe it's possible to use the manhattan for euclidean as well. 

- There are mutable classes that could have been immutable given that few choices had been done different.
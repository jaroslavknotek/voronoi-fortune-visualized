# Lessons Learned

## Achievements

- Having visualized something as strange as Fortune in manhattan metrics helps overcome unintuitive notion of non-euclidean geometry.
- I utilized parts of matplotlib and jupyter I didn't know they existed. The drawing is done mostly by using patches which helps greatly with overcoming issues in animation. You can't just draw or plot something. You need to initialize plots before animation takes place and then plug in different data each frame. You can't dynamically add more than you have previously initialized. Even though it was great to not adding different dependency. However, it may not worth it. Definitely not in production.

## Problems

- This tasks contains numerous software engineering no-nos that stems from multiple bad decision.

  1. Underestimation - This task will be just few days of work. This created false hope
  2. Overestimation - I remember the algorithm I am supposed well enough. I don't have to read the solution I am about to extend.
  3. Development Environment - Assumption that visual tasks require visual development. Wrong. Instead of developing the whole solution in jupyter notebooks. I should have created normal solution. Write some code and test it right away. It may have cleared many misunderstanding and fix a lot of bugs thus saving many hours.

- Geometry is coupled to viewport. I can't work with rays (only segments) so it needs to have some bounds. Infinite plane won't work. that's pretty bad as you have to pass information about viewport to the geometry class as well.

- There is a similar project [here](https://github.com/Yatoom/foronoi) which looks more professional. Maybe it would have been better to extend it, instead of coming up with my own solution.
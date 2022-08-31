def test_draw_line():
    
    plt.figure(figsize=(10,10))


    x_min,x_max = 1,201
    y_min,y_max = 3,100

    plt.xlim((x_min,x_max))
    plt.ylim((y_min,y_max))
    plt.axis("scaled")
    
    draw_line = drawing.draw_line
    def draw_vline_cut_in_slanted():
        p1 = (10,80)
        p4 = (150,20)

        draw_line(plt, p4,p1,x_min,x_max,5,15)
        draw_line(plt, p4,p1,x_min,x_max,90,95)

        draw_line(plt, p4,p1,x_min,x_max,17,40)
        draw_line(plt, p4,p1,x_min,x_max,60,85)
        draw_line(plt, p4,p1,x_min,x_max,45,55)


        p1 = (150,80)
        p4 = (10,20)

        draw_line(plt, p4,p1,x_min,x_max,5,15)
        draw_line(plt, p4,p1,x_min,x_max,90,95)

        draw_line(plt, p4,p1,x_min,x_max,17,40)
        draw_line(plt, p4,p1,x_min,x_max,60,85)
        draw_line(plt, p4,p1,x_min,x_max,45,55)



    def draw_hline_cut_in_slanted():
        p1 = (100,95)
        p4 = (150,10)

        draw_line(plt, p4,p1,0,70,y_min,y_max,c='r')
        draw_line(plt, p4,p1,80,110,y_min,y_max,c='r')
        draw_line(plt, p4,p1,115,125,y_min,y_max,c='r')
        draw_line(plt, p4,p1,130,160,y_min,y_max,c='r')
        draw_line(plt, p4,p1,170,x_max,y_min,y_max,c='r')

        p1 = (100,10)
        p4 = (150,95)

        draw_line(plt, p4,p1,0,70,y_min,y_max,c='b')
        draw_line(plt, p4,p1,80,110,y_min,y_max,c='b')
        draw_line(plt, p4,p1,115,125,y_min,y_max,c='b')
        draw_line(plt, p4,p1,130,160,y_min,y_max,c='b')
        draw_line(plt, p4,p1,170,x_max,y_min,y_max,c='b')



    def draw_diagonal_cut():
        p1 = (10,10)
        p4 = (90,90)

        draw_line(plt, p4,p1,10,20,y_min,y_max)
        draw_line(plt, p4,p1,40,60,y_min,y_max)
        draw_line(plt, p4,p1,80,90,y_min,y_max)

        p1 = (10,90)
        p4 = (90,10)

        draw_line(plt, p4,p1,x_min,x_max,10,20)
        draw_line(plt, p4,p1,x_min,x_max,40,60)
        draw_line(plt, p4,p1,x_min,x_max,80,90)



    def test_below():
        p2 = (35,44)
        p4 = (12,20)
        #draw_line(plt, p2,p4,22 ,100, 24, 100)
        #draw_line(plt, p2,p4,0 ,34, 0, 32)
        draw_line(plt, p2,p4,22 ,34, 24, 32)

    test_below()


    draw_hline_cut_in_slanted()
    draw_vline_cut_in_slanted()
    draw_diagonal_cut()

def draw_lines():
    plt.figure(figsize=(4,2))
    x_min,x_max = 1,201
    y_min,y_max = 3,105

    plt.xlim((x_min,x_max))
    plt.ylim((y_min,y_max))
    plt.axis("scaled")


    import random 

    # there are four combination for each direction
    def test_lr():
        drawing.draw_line(plt, (20,80), (90,10),x_min,x_max,y_min,y_max)
        drawing.draw_line(plt, (20,80), (10,90),x_min,x_max,y_min,y_max)
        drawing.draw_line(plt, (5,40), (10,35),x_min,x_max,y_min,y_max)
        drawing.draw_line(plt, (190,15), (195,10),x_min,x_max,y_min,y_max)
        
    def test_rl():
        drawing.draw_line(plt, (80,90), (70,80),x_min,x_max,y_min,y_max)
        drawing.draw_line(plt, (20,20),(10,10),x_min,x_max,y_min,y_max)
        drawing.draw_line(plt, (190,90),(200,100),x_min,x_max,y_min,y_max)
        
    test_lr()    
    test_rl()

    drawing.draw_line(plt, (190,90),(10,100),x_min,x_max,y_min,y_max)
    drawing.draw_line(plt, (90,10),(10,100),x_min,x_max,y_min,y_max)

test_draw_line()


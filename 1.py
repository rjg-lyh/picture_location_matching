from matplotlib import pyplot as plt
# plt.plot([100,100,1500,1500],[100,2000,100,2000],'ro')
# plt.plot([100,100],[100,2000])
# plt.plot()
# plt.show()

def drawPicture(dots: list):
    left_top, right_down = dots[0], dots[1]
    right_top = [right_down[0], left_top[1]]
    left_down = [left_top[0], right_down[1]]
    plt.plot([left_top[0], right_top[0], right_down[0], left_down[0]], 
            [left_top[1], right_top[1], right_down[1], left_down[1]],'ro')
    plt.plot([left_top[0], right_top[0]], [left_top[1], right_top[1]],'r')
    plt.plot([right_top[0], right_down[0]], [right_top[1], right_down[1]],'r')
    plt.plot([right_down[0], left_down[0]], [right_down[1], left_down[1]],'r')
    plt.plot([left_down[0], left_top[0]], [left_down[1], left_top[1]],'r')
    
drawPicture([[300,500], [1500,2000]])
drawPicture([[100,100], [800,600]])
plt.show()
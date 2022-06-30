from scipy.optimize import linear_sum_assignment
from matplotlib import pyplot as plt
import numpy as np
import random
import math

class Solution:
    def generate_dots(self, rows: int, cols: int):  #造出number张图片，[[x1, y1], [x2, y2]]表示
        dots = []
        first_dot_classes = [[[0,0],[1200,1200]],[[50,50],[1160,1280]],[[100,100],[1200,1250]]]
        ratio1_classes = [0.15, 0.2, 0.25, 0.3] #同行间
        ratio2_classes = [0.1, 0.12] #异行间
        ratio3_classes = [0.05, 0.1, 0.15, 0.2] #图片本身缩放率
        # ratio1_classes = [0.4, 0.5, 0.45, 0.6] #同行间
        # ratio2_classes = [0.3, 0.4] #异行间
        # ratio3_classes = [0.15, 0.2, 0.35, 0.4] #图片本身缩放率
        records = []
        for i in range(rows):
            first_dot = random.choice(first_dot_classes)
            if i == 0:
                records.append(first_dot[:])
            else:
                ratio2 = random.choice(ratio2_classes)
                last_dot = records[-1]
                xa, xb, ya, yb = last_dot[0][0], last_dot[1][0], last_dot[0][1], last_dot[1][1]
                w = first_dot[1][0] - first_dot[0][0]
                h = first_dot[1][1] - first_dot[0][1]
                x1 = xa + int((xb - xa)*ratio2)
                y1 = yb + int((yb - ya)*ratio2)
                x2 = x1 + int(w*(1 + random.choice([1, -1])*ratio2))
                y2 = y1 + int(h*(1 + random.choice([1, -1])*ratio2))
                first_dot = [[x1, y1], [x2, y2]]
                records.append(first_dot[:])
            for j in range(cols):
                if j == 0:
                    dots.append(first_dot)
                    continue
                ratio1 = random.choice(ratio1_classes)
                ratio3 = random.choice(ratio3_classes)
                last_dot = dots[-1]
                xa, xb, ya, yb = last_dot[0][0], last_dot[1][0], last_dot[0][1], last_dot[1][1]
                x1 = xb + int((xb - xa)*ratio1)
                y1 = ya + int((yb - ya)*ratio1)
                x2 = x1 + int((xb - xa)*(1 + random.choice([1, -1])*ratio3))
                y2 = y1 + int((yb - ya)*(1 + random.choice([1, -1])*ratio3))
                dots.append([[x1, y1], [x2, y2]])
        return dots

    def Hugmatch(self, dots: list): #匈牙利匹配：从几种W、H拆解情况中，分别计算出最优匹配，最后选择损失最小的匹配方式
        resolutions = self.resolve(len(dots))
        left_top, right_down = self.boundingBox(dots)
        mincost = np.inf
        minidx = -1
        costMatrixs = []
        bestorders = []
        ind_list = []
        result = {}
        for idx, resolution in enumerate(resolutions):            
            cost_matrix, anchor_dots, center_dots = self.make_cost_matrix(dots, resolution, left_top, right_down)
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            cost = cost_matrix[row_ind, col_ind].sum()
            costMatrixs.append(cost_matrix)
            bestorders.append(col_ind)
            print("{}的损失表, 最小损失为{}\n".format(resolution, cost),cost_matrix)
            if cost < mincost:
                mincost = cost
                minidx = idx
        final_costMatrix = costMatrixs[minidx]
        final_col_ind = bestorders[minidx]
        final_resolution = resolutions[minidx]
        w, h = final_resolution[1], final_resolution[0]
        print("最佳匹配形状是{}，其损失表为：\n".format(final_resolution,final_costMatrix))
        for i, ind in enumerate(final_col_ind):
            row, col = self.convertForm(ind, h, w)
            ind_list.append([row, col])
            result['picture{}'.format(i) + str(dots[i])] = [row, col]
        return result, ind_list, anchor_dots, center_dots
    def resolve(self, number: int):    # W、H拆解
        results = []
        nums = list(range(1, number + 1))
        for num in nums:
            if number % num: # 不可被整除或被计算过了
                continue
            results.append([num, number//num])
        return results
    
    def boundingBox(self, dots: list):  # 找出框住所有图片的最小box框
        left_top = [np.Inf, np.Inf] #找左上角
        right_down = [-np.Inf, -np.Inf]
        for dot in dots:
            if dot[0][0] < left_top[0]:
                left_top[0] = dot[0][0]
            if dot[0][1] < left_top[1]:
                left_top[1] = dot[0][1]
            if dot[1][0] > right_down[0]:
                right_down[0] = dot[1][0]
            if dot[1][1] > right_down[1]:
                right_down[1] = dot[1][1]
        return left_top, right_down

    def make_cost_matrix(self, dots: list, resolution: list, left_top: list, right_down: list): #匈牙利损失表计算
        cell_row, cell_col = resolution[0], resolution[1]
        step_row = (right_down[1] - left_top[1])//(cell_row + 1)
        step_col = (right_down[0] - left_top[0])//(cell_col + 1)
        anchor_dots = []
        center_dots = []
        cost_matrix = []
        for i in range(1, cell_row + 1):
            for j in range(1, cell_col + 1):
                anchor_dots.append([left_top[0] + step_col*j, left_top[1] + step_row*i]) #得到锚点
        for dot in dots:
            center_dots.append([dot[0][0] + (dot[1][0] - dot[0][0])//2, dot[0][1] + (dot[1][1] - dot[0][1])//2]) #得到每张图片中心点
        for center_dot in center_dots:
            cost = []
            for anchor_dot in anchor_dots:                                                #计算L2损失
                cost.append(int(math.sqrt((center_dot[0] - anchor_dot[0])**2 + (center_dot[1] - anchor_dot[1])**2)))
            cost_matrix.append(cost)
        return np.array(cost_matrix), anchor_dots, center_dots
    def convertForm(self, index: int, row: int, col: int): #将索引值转化为对应的[row, col]格式
        count = 0
        for i in range(row):
            for j in range(col):
                if count == index:
                    return i, j
                count += 1
    def drawPicture(self, dots: list):
        left_top, right_down = dots[0], dots[1]
        right_top = [right_down[0], left_top[1]]
        left_down = [left_top[0], right_down[1]]
        # plt.scatter([left_top[0], right_top[0], right_down[0], left_down[0]], 
        #         [left_top[1], right_top[1], right_down[1], left_down[1]],s=50)  #'ro'
        # plt.annotate('(%s,%s)'%(left_top[0],left_top[1]),xy=(left_top[0],left_top[1]),xytext=(0,10),textcoords = 'offset points',ha='center')
        # plt.annotate('(%s,%s)'%(left_down[0],left_down[1]),xy=(left_down[0],left_down[1]),xytext=(0,10),textcoords = 'offset points',ha='center')
        # plt.annotate('(%s,%s)'%(right_top[0],right_top[1]),xy=(right_top[0],right_top[1]),xytext=(0,10),textcoords = 'offset points',ha='center')
        # plt.annotate('(%s,%s)'%(right_down[0],right_down[1]),xy=(right_down[0],right_down[1]),xytext=(0,10),textcoords = 'offset points',ha='center')
        plt.plot([left_top[0], right_top[0]], [left_top[1], right_top[1]],'r')
        plt.plot([right_top[0], right_down[0]], [right_top[1], right_down[1]],'r')
        plt.plot([right_down[0], left_down[0]], [right_down[1], left_down[1]],'r')
        plt.plot([left_down[0], left_top[0]], [left_down[1], left_top[1]],'r')
    def drawCenter(self, dots: list, ind_list: list):
        for i in range(len(dots)):
            center_x, center_y = dots[i][0][0] + (dots[i][1][0] - dots[i][0][0])//2, dots[i][0][1] + (dots[i][1][1] - dots[i][0][1])//2
            print(center_x, center_y)
            row, col = ind_list[i][0], ind_list[i][1]
            plt.scatter([center_x],[center_y],marker='s',s=50)
            plt.annotate('(%s,%s)'%(row,col),xy=(center_x,center_y),xytext=(0,10),textcoords = 'offset points',ha='center')

if __name__ == "__main__":
    solution = Solution()
    dots = solution.generate_dots(4, 5) #造点
    print(dots)
    result, ind_list, anchor_dots, center_dots = solution.Hugmatch(dots)
    for dot in dots:
        solution.drawPicture(dot)
    solution.drawCenter(dots, ind_list)
    print(anchor_dots)
    print(center_dots)
    plt.show()



from scipy.optimize import linear_sum_assignment
from matplotlib import pyplot as plt
import numpy as np
import random
import math

class Solution:
    def generate_centers(self, rows: int, cols: int):
        centers = [[[1, 1] for _ in range(cols + 1)] for _ in range(rows + 1)]
        centers_ravel = []
        dist1_classes = [300, 350, 400, 450, 500] #同行间
        dist2_classes = [500, 800, 1200] #异行间
        dist3_classes = [20, 40, 50]
        for j in range(cols + 1):
            if j == 0:
                continue
            dist1 = random.choice(dist1_classes)
            centers[0][j][0] = centers[0][j - 1][0] + dist1
        for i in range(rows + 1):
            if i == 0:
                continue
            dist2 = random.choice(dist2_classes)
            centers[i][0][1] = centers[i - 1][0][1] + dist2
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                dist3 = random.choice(dist3_classes)
                centers[i][j][0] = centers[i - 1][j][0] + random.choice([1, -1])*dist3
                centers[i][j][1] = centers[i][j - 1][1] + random.choice([1, -1])*dist3
        centers.pop(0)
        for i in range(rows):
            centers[i].pop(0)
            centers_ravel += centers[i]
        return centers_ravel
    
    def Hugmatch(self, centers: list):
        resolutions = self.resolve(len(centers))
        mincost = np.inf
        minidx = -1
        costMatrixs = []
        bestorders = []
        ind_list = []
        result = []
        for idx, resolution in enumerate(resolutions):            
            cost_matrix = self.make_cost_matrix(centers, resolution)
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
        print("最佳匹配形状是{}，其损失表为：{}\n".format(final_resolution,final_costMatrix))
        for i, ind in enumerate(final_col_ind):
            row, col = self.convertForm(ind, h, w)
            ind_list.append([row, col])
            plt.annotate('(%s,%s)'%(row + 1, col + 1),xy=(centers[i][0],centers[i][1]),xytext=(0,10),textcoords = 'offset points',ha='center')
            result.append([row + 1, col + 1])

        return result
    def make_cost_matrix(self, centers: list, resolution: list):
        anchor_features = self.grid_features(resolution)
        center_features = self.center_features(centers)
        cost_matrix = []
        for center_feature in center_features:
            cost = []
            for anchor_feature in anchor_features:
                sum1 = 0
                for i in range(len(anchor_feature)):
                    sum1 += abs(center_feature[i] - anchor_feature[i])
                cost.append(sum1)
            cost_matrix.append(cost)
        return np.array(cost_matrix)

    def center_features(self, centers: list):
        center_features = []       
        for i in range(len(centers)):
            x, y = centers[i][0], centers[i][1]
            center_feature = [0, 0, 0, 0]
            for j in range(len(centers)):
                if j == i:
                    continue
                x1, y1 = centers[j][0], centers[j][1]
                if x1 < x:
                    center_feature[0] += 1
                else:
                    center_feature[1] += 1
                if y1 < y:
                    center_feature[2] += 1
                else:
                    center_feature[3] += 1
            center_features.append(center_feature)
        return center_features

    def grid_features(self, resolution: list):
        row, col = resolution[0], resolution[1]
        grid_features = []
        for i in range(row):
            for j in range(col):
                grid_features.append([j*row, (col - j - 1)*row, i*col, (row - i - 1)*col])
        return grid_features


    def resolve(self, number: int):
        results = []
        nums = list(range(1, number + 1))
        for num in nums:
            if number % num: # 不可被整除或被计算过了
                continue
            results.append([num, number//num])
        return results

    def convertForm(self, index: int, row: int, col: int): #将索引值转化为对应的[row, col]格式
        count = 0
        for i in range(row):
            for j in range(col):
                if count == index:
                    return i, j
                count += 1
    
    def drawDots(self, dots: list):
        for dot in dots:
            plt.scatter(dot[0], dot[1], marker='s',s=50)
        
        


if __name__ == "__main__":
    solution = Solution()
    centers = [[100.2, 120.4], [200.1, 210], [210.3, 115.8], [102.5, 200.1]]
    result = solution.Hugmatch(centers)
    print(result)
    solution.drawDots(centers)
    plt.show()

                


        
        
            


        
        
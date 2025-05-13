import numpy as np
import pygad
from deal_matrix import *
import time

# 插值后通量数据读取
read_tif = tif("./out1km.tif")
# 总体足迹矩阵
read_H = read_martix("./footprints/")
i = 0
def fitness_f(ga_instance,solution, solution_idx):
    '''适应度函数'''
    point_list = solution.tolist()
    pt_list = []
    for i in range(0,5): # 提取基因中五个点的坐标(图像中坐标)
        point = Point(point_list[2*i],point_list[2*i+1],read_tif.gt)
        pt_list.append(point)
    # 计算通量
    x_h = read_tif.Get_x(pt_list)
    # 计算足迹矩阵
    H = read_H.Get_H(pt_list)
    # 计算点积
    y_h = H.mutiple(x_h)
    # 计算适应度
    return y_h

# 创建遗传算法实例
box = read_tif.box
ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=10,
    fitness_func=fitness_f,
    sol_per_pop=50,
    num_genes=10,
    gene_type=int,
    gene_space=[# 五个点的坐标，每个坐标由两个基因表示，取值范围为135到边界的整数
        {'low': 135, 'high': box["width"]-135,'step':1},
        {'low': 135, 'high': box["height"]-135,'step':1},
        {'low': 135, 'high': box["width"]-135,'step':1},
        {'low': 135, 'high': box["height"]-135,'step':1},
        {'low': 135, 'high': box["width"]-135,'step':1},
        {'low': 135, 'high': box["height"]-135,'step':1},
        {'low': 135, 'high': box["width"]-135,'step':1},
        {'low': 135, 'high': box["height"]-135,'step':1},
        {'low': 135, 'high': box["width"]-135,'step':1},
        {'low': 135, 'high': box["height"]-135,'step':1} 
        ],
    parent_selection_type="sss",  # 稳态选择
    keep_parents=2,
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=10
)
# 运行算法
ga_instance.run()
# 输出结果
solution, solution_fitness, _ = ga_instance.best_solution()
# 将图像坐标转换成经纬度坐标
solution = solution.tolist()
point_list = []
for i in range(0,5):
    point = Point(solution[2*i],solution[2*i+1],read_tif.gt)
    point_list.append(point)
print("最优解为：")
for pt in point_list:
    print(pt.longitude,pt.latitude)
print(f"适应度: {solution_fitness}")
# 可视化
ga_instance.plot_fitness()

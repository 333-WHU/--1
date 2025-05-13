import numpy as np
import pygad
from deal_tif import Point,tif
from deal_matrix import triple_list,total_triple_list

# 插值后通量数据读取
read_tif = tif("./Global_Fuel_Exploitation_Inventory_v2_2019_Total_Fuel_Exploitation.tif")
def fitness_f(ga_instance,solution, solution_idx):
    '''适应度函数'''
    point_list = solution.tolist()
    pt_list = []
    for i in range(0,5): # 提取基因中五个点的坐标(图像中坐标)
        point = Point(point_list[2*i],point_list[2*i+1],read_tif)
        pt_list.append(point)
    # 计算通量
    x_h = [read_tif.Get_x(pt.x, pt.y) for pt in pt_list]
    # 计算足迹矩阵
    
    
    
if 0:
    # 创建遗传算法实例
    box = read_tif.box
    ga_instance = pygad.GA(
        num_generations=100,
        num_parents_mating=10,
        fitness_func=fitness_f,
        sol_per_pop=50,
        num_genes=2,
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
    print(f"最优解: {solution}, 适应度: {solution_fitness}")
    # 可视化
    ga_instance.plot_fitness()
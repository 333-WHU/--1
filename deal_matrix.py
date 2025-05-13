import pathlib
import os
import json
import numpy as np


class triple:
    """稀疏矩阵三元组表示的矩阵的一行"""
    def __init__(self, row):
        self.row = row
        self.col_and_value = []
        self.max_col = 0
        self.min_col = 0
    
    def add(self, col, value):
        """添加元素"""
        self.col_and_value.append([col, value])
        if self.max_col < col:
            self.max_col = col
        if self.min_col > col:
            self.min_col = col
    def union(self,triple2):
        """矩阵并集"""
        if self.row != triple2.row:
            return 0
        else:
            col_list = [col for col,value in self.col_and_value]
            for col,value in triple2.col_and_value:
                # 如果列号不同添加列号
                if col not in col_list:
                    self.col_and_value.append([col,value])
                    col_list.append(col)
                    continue
                # 如果列号相同取最大值
                for i in range(len(self.col_and_value)):
                    if self.col_and_value[i][0] == col:
                        self.col_and_value[i][1] = max(self.col_and_value[i][1],value)        
    def copy(self):
        """复制一份"""
        t = triple(self.row)
        for col,value in self.col_and_value:
            t.add(col,value)
        return t
    def mutiple(self, triple2)->float:
        """矩阵点积"""
        if self.row != triple2.row:
            return 0
        else:
            result = 0
            for col,value in self.col_and_value:
                for col2,value2 in triple2.col_and_value:
                    if col == col2:
                        result += value * value2
            return result
class triple_list:
    """稀疏矩阵三元组表示的分块矩阵"""
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.triple_list = []
        self.min_row = 0
        self.max_row = 0

    def add(self,triple):
        """添加一行"""
        self.triple_list.append(triple)
        if self.max_row < triple.row:
            self.max_row = triple.row
        if self.min_row > triple.row:
            self.min_row = triple.row
    def union(self,triple_list2):
        """矩阵并集"""
        for triple2 in triple_list2.triple_list:
            if self.triple_list == []:
                self.add(triple2)
            else:
                for triple in self.triple_list:
                    if triple.row == triple2.row:
                        triple.union(triple2)
                    else:
                        self.add(triple2)
    def add_offset(self,offset_x, offset_y):
        """添加偏移量"""
        for triple in self.triple_list:
            triple.row += offset_x
            for col,value in triple.col_and_value:
                col += offset_y

    def copy(self):
        """复制一份"""
        t = triple_list(self.latitude,self.longitude)
        for triple in self.triple_list:
            t.add(triple.copy())
        return t

    def mutiple(self,triple_list2)->float:
        """矩阵点积"""
        result = 0
        for triple in self.triple_list:
            for triple2 in triple_list2.triple_list:
                if triple.row == triple2.row:
                    result += triple.mutiple(triple2)
        return result
    def Get_H(self,pt_list:list,side_length = 10):
        '''根据点集获取足迹矩阵'''
        H = np.zeros(side_length,side_length)
        for pt in pt_list:
            # 根据经纬度在矩阵中找到以它为中心10x10区域
            for t_list in self.triple_list:
                # 如果pt的经纬度不在t_list的经纬度范围内,跳过
                if pt.longitude < t_list.longitude-2.7 or pt.longitude > t_list.longitude+2.7 or pt.latitude < t_list.latitude-2.7 or pt.latitude > t_list.latitude+2.7:
                    continue
                # 如果pt的经纬度在t_list的经纬度范围内,计算H对应值
class total_triple_list:
    """完整的足迹矩阵"""
    def __init__(self):
        self.triple_list = []
    
    def add(self,triple_list):
        """添加一个分块矩阵"""
        self.triple_list.append(triple_list)
    
    def union(self)->triple_list:
        """矩阵并集"""
        logitude_list = [t.longitude for t in self.triple_list]
        latitude_list = [t.latitude for t in self.triple_list]
        # 坐标平均值
        H = triple_list(np.mean(latitude_list),np.mean(logitude_list))
        # 初始化分块矩阵
        for t_list in self.triple_list:
            # 根据与中心坐标的坐标差，对分块矩阵进行偏移
            offset_x = int((t_list.latitude - H.latitude) * 10)
            offset_y = int((t_list.longitude - H.longitude) * 10)
            t_list.add_offset(offset_x,offset_y)
            H.union(t_list)
        return H


def read_martix(file_folder):
    # 对于所有的json文件,合并为一个完整的矩阵
    total_triple = total_triple_list()
    for file in pathlib.Path(file_folder).glob('*.json'):
        with open(file, 'r') as f:
            # 分割filename
            filename = file.stem
            information_list = filename.split('_')
            # 获取中心坐标
            center_latitude = float(information_list[1])            
            center_longitude = float(information_list[2])
            data = json.load(f)
            # 对于每一个json文件,生成一个分块矩阵
            block = triple_list(center_latitude,center_longitude)
            for row_data in data: # 对每一行进行
                # 获取行号
                row = row_data['row']
                # 生成一个triple
                triple_row = triple(row)
                # 获取列号和通量值
                for col,value in row_data['col_and_value']:
                    triple_row.add(col,value)
                block.add(triple_row)
            total_triple.add(block)
    t = total_triple.union()
    return t
            

if __name__ == '__main__':
    from time import time
    start = time()
    total_triple = read_martix('./footprints/')
    end = time()
    print(end-start)

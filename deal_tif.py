from osgeo import gdal




class Point:
    def __init__(self, x:int, y:int,gt):
        self.x = x
        self.y = y
        self.longitude = gt[0] + x * gt[1] + y * gt[2]
        self.latitude = gt[3] + x * gt[4] + y * gt[5]


class tif:
    def __init__(self,file_path):
        self.file_path = file_path
        self.dataset = gdal.Open(file_path)
        self.gt = self.dataset.GetGeoTransform()
        self.band = self.dataset.GetRasterBand(1)
        self.array = self.band.ReadAsArray()
        self.width = self.dataset.RasterXSize  # 列数
        self.height = self.dataset.RasterYSize  # 行数
        self.box = {'left': self.gt[0],
                'top': self.gt[3], 
                'right': self.gt[0] + self.gt[1] * self.width,
                'bottom': self.gt[3] + self.gt[5] * self.height,
                'width': self.width,
                'height': self.height
                }
    def Get_x(self,center_x, center_y,side_length = 10):
        '''根据图像中坐标获取通量值,x,y为中心行列号，返回长度为10的方阵'''
        # 计算矩形范围
        half = side_length // 2
        if center_x < half or center_y < half:
            return None
        if center_x > self.width - half or center_y > self.height - half:
            return None
        x_left = center_x - half
        y_top = center_y - half
        # 读取数据
        region = self.array(x_left, y_top, side_length, side_length)
        return region        


'''
@desc:元数据类
@author: Martin Huang
@time: created on 2019/6/2 17:57
@修改记录:2019/6/3 => 完成基础骨架
'''

class MetaData:
    def __init__(self,fileSize,fileName,MD5,blockNum):
        self.fileSezie = fileSize
        self.fileName = fileName
        self.MD5 = MD5
        self.blockNum = blockNum

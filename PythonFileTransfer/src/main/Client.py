'''
@desc:客户端类
@author: Martin Huang
@time: created on 2019/6/2 21:31
@修改记录:2019/6/3 => 完成基础骨架
'''
import os
from threading import Thread
from tqdm import tqdm
from threading import Thread
from MetaData import *
from Utils.ConversionUtils import ConversionUtils
from Utils.IOUtils import IOUtils
from Utils.NetUtils import NetUtils
#以下包pycharm使用
# from src.main.Utils.IOUtils import *
# from src.main.Utils.ConversionUtils import *
# from src.main.Utils.NetUtils import *
# from src.main.MetaData import *


class Client:
    def __init__(self,path,ip,bufferSize=1,threadNumTop=2):
        self.path = path
        self.serverIP = ip
        self.bufferSize = bufferSize
        self.fileList = []
        self.threadNum = 0
        self.threadNumTop = threadNumTop

    def getMetaData(self):
        metaDataPath = self.path + os.sep + 'METADATA'
        self.fileList.append(metaDataPath)
        NetUtils.receiveSigFile(metaDataPath, self.serverIP)
        print('元数据接收完毕')
        self.metadata = IOUtils.deserializeObjFromPkl(metaDataPath)

    def receiveFileSubProcess(self,partPath,port):
        NetUtils.receiveSigFile(partPath,self.serverIP,port,self.bufferSize,verbose=False)
        self.threadNum -= 1
        #print('接收了1个文件')


    def receiveFileProcess(self):
        print('SETP1---接收元数据')
        self.getMetaData()
        blockNum = self.metadata.blockNum
        print('SETP2---开始传输数据')
        if blockNum == 0:
            print('单文件直接传输，目标文件小于100M 传输中...')
            NetUtils.receiveSigFile(self.path + os.sep + self.metadata.fileName,self.serverIP,bufferSize=self.bufferSize,verbose=False)
        else:
            tPool = []
            for i in tqdm(range(blockNum),ascii=True):
                while self.threadNum >= self.threadNumTop:
                    pass
                partPath = self.path + os.sep + 'PART' + str(i)
                t = Thread(target=self.receiveFileSubProcess,args=(partPath,9000+i))
                self.fileList.append(partPath)
                t.setDaemon(True)
                t.start()
                tPool.append(t)
                self.threadNum += 1
            for t in tPool:
                while True:
                    if not t.isAlive():
                        break
            print('SETP3---开始合并文件')
            IOUtils.combineFile(self.path,self.path+os.sep+self.metadata.fileName,self.metadata.blockNum)
        IOUtils.deleteFiles(self.fileList)
        md5 = IOUtils.getMD5(self.path+os.sep+self.metadata.fileName)
        print('SETP4---验证文件中...')
        print(md5)
        if md5 == self.metadata.MD5:
            print('完成！')
        else:
            print('失败')


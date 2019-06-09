'''
@desc:服务器类
@author: Martin Huang
@time: created on 2019/6/2 17:38
@修改记录:2019/6/3 => 完成基础骨架
          2019/6/6 => 增加异常处理
          2019/6/7 => 输出优化+参数优化+端口连通性检测
          2019/6/9 => 服务器端启动时显示其IP
'''
from tqdm import tqdm
import os
import sys
from MetaData import *
from threading import Thread
from Utils.ConversionUtils import ConversionUtils
from Utils.IOUtils import IOUtils
from Utils.NetUtils import NetUtils
#以下包pycharm使用
# from src.main.Utils.IOUtils import *
# from src.main.Utils.NetUtils import *
# from src.main.Utils.ConversionUtils import *
class Server:
    def __init__(self,path,port=9000,bufferSize=1,blockSize=100):
        self.fileList = []
        self.path = path
        self.port = port
        self.bufferSie=bufferSize
        self.blockSize = blockSize
        if os.path.isdir(path):
            print('该路径是目录，将该目录中的所有文件(包含子文件夹)打包为dirpack.zip')
            self.path = IOUtils.packageDir(path)
            self.fileList.append(self.path)


    def initMetaData(self):
        print('计算MD5...')
        MD5 = IOUtils.getMD5(self.path)
        print(MD5)
        fileSize = os.path.getsize(self.path)
        fileName = os.path.basename(self.path)
        #文件大小小于100M 不分块
        if fileSize < ConversionUtils.megabytes2Bytes(100):
            self.blockNum = 0
        else:
            self.blockNum = IOUtils.getPartionBlockNum(self.path,self.blockSize)
        metadata = MetaData(fileSize,fileName,MD5,self.blockNum)
        self.metadataPath = os.path.dirname(self.path) + os.sep + 'METADATA'
        IOUtils.serializeObj2Pkl(metadata,self.metadataPath)
        self.fileList.append(self.metadataPath)
        print('元数据初始化完毕')

    def scanPort(self):
        if self.blockNum == 0:
            ret = NetUtils.isPortOccupied(self.port)
            if ret:
                print(str(self.port)+'被占用！请释放或更换端口')
                sys.exit(-1)
        else:
            for i in tqdm(range(self.blockNum),ascii=True):
                ret = NetUtils.isPortOccupied(self.port+i)
                if ret:
                    print(str(self.port+i) + '被占用！请释放或更换端口')
                    sys.exit(-1)

    def serverTransferFileProcess(self):
        print('服务器IP为：')
        sip = NetUtils.getLocalIPAddr()
        print(sip)
        print('SETP1---初始化元数据')
        self.initMetaData()
        print('STEP2---测试端口连通性')
        self.scanPort()
        print('STEP3---发送元数据')
        NetUtils.transferSigFile(self.metadataPath)
        print('元数据已发送')
        print('STEP4---开始传输数据')
        if self.blockNum == 0:
            print('单文件<100M 传输中...请稍等...')
            NetUtils.transferSigFile(self.path,bufferSize=self.bufferSie,verbose=True,port=self.port)
        else:
            print('文件共分为'+str(self.blockNum)+'块，开始分割文件')
            blockBytes = ConversionUtils.megabytes2Bytes(self.blockSize)
            toPath = os.path.dirname(self.path) + os.sep + 'MEtemp'
            self.fileList.append(toPath)
            if IOUtils.isDir(toPath):
                print('MEtemp目录已存在，删除之')
                IOUtils.deleteFile(toPath)
            try:
                os.mkdir(toPath)
            except FileNotFoundError as reason:
                print('错误！无法创建目录！')
                sys.exit(-1)
            #线程池
            tpool = []
            #printByNoneAutoNewLine = sys.stdout
            with open(self.path, 'rb') as orgFile:
                for i in tqdm(range(self.blockNum),ascii=True):
                    #printByNoneAutoNewLine.write('正在分割第' + str(i + 1) + '块\r\n')
                    totalBufferSize = 0
                    with open(toPath + os.sep+'PART' + str(i), 'wb') as toFile:
                        while totalBufferSize < blockBytes:
                            # 缓冲区
                            data = orgFile.read(ConversionUtils.megabytes2Bytes(self.bufferSie))
                            if not data:
                                break
                            toFile.write(data)
                            totalBufferSize += ConversionUtils.megabytes2Bytes(self.bufferSie)
                    self.fileList.append(toPath + os.sep+'PART' + str(i))
                    #printByNoneAutoNewLine.write(toPath + os.sep+'PART' + str(i)+'\r\n')
                    #printByNoneAutoNewLine.write('分割完成'+'\r\n')
                    t = Thread(target=NetUtils.transferSigFile, args=(toPath + os.sep+'PART' + str(i), self.port+i,self.bufferSie,False))
                    t.setDaemon(True)
                    t.start()
                    tpool.append(t)

            for eachThread in tqdm(tpool,ascii=True):
                while True:
                    if not eachThread.isAlive():
                        break
        print('清理临时文件...')
        IOUtils.deleteFiles(self.fileList)
        print('完成!')
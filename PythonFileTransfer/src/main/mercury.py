'''
@desc:主程序类
@author: Martin Huang
@time: created on 2019/6/3 18:50
@修改记录:2019/6/3 => 完成基础骨架
          2019/6/7 => 参数优化+输出优化
          2019/6/8 => BUG修复
'''
import sys,getopt,platform,os
from Server import Server
from Client import Client

def printHelpInfo():
    print(
        '''
        使用方法：
        mercury -t client -p path -i serverIP [-P port -T threadnum -b buffer -n blocksize]
        or
        mercury -t server -p path [-P port -T threadnum -b buffer -n blocksize]
        -t or --type 表示类型(必须) 值：server/client
        -p or --path 表示文件路径(必须) 值：server端为文件路径 client端为目录
        -i or --ip   表示服务器地址(客户端时必须) 值：默认本机127.0.0.1
        -P or --port 表示程序要使用的端口号(可选) 值：默认9000
        -T or --threadnum 表示客户端同时接收的线程数(可选) 值：默认为2
        -b or --buffer 表示网络传输时的缓冲区大小(可选) 值：默认1M
        -n or --blocksize 表示文件的分块大小(可选) 值：默认100M
        '''
    )

def main(argv):
    type = ''
    path = ''
    port = 9000
    bufferSize = 1
    blockSize = 100
    ip = '127.0.0.1'
    threadNum = 2
    try:
        '''
        -t or --type 表示类型(必须) 值：server/client
        -p or --path 表示文件路径(必须) 值：server端为文件路径 client端为目录
        -i or --ip   表示服务器地址(客户端时必须) 值：默认本机127.0.0.1
        -P or --port 表示程序要使用的端口号(可选) 值：默认9000
        -T or --threadnum 表示客户端同时接收的线程数(可选) 值：默认为2
        -b or --buffer 表示网络传输时的缓冲区大小(可选) 值：默认1M
        -n or --blocksize 表示文件的分块大小(可选) 值：默认100M
        '''
        opts, args = getopt.getopt(argv, 't:p:P:i:T:b:n:',['type=','path=','port=','ip=','threadnum=','buffer=','blocksize='])
    except:
        printHelpInfo()
        sys.exit(-1)
    try:
        for opt,arg in opts:
            if opt in ('-t','--type'):
                type = arg
            elif opt in ('-p','--path'):
                path = arg
                if platform.system() == 'Windows':
                    path = path.replace('\\',os.sep)
                else:
                    path = path.replace('/',os.sep)
                if path == '':
                    printHelpInfo()
                    exit(-1)
            elif opt in ('-P','--port'):
                port = int(arg)
            elif opt in ('-i','--ip'):
                if type == 'client':
                    ip = arg
            elif opt in ('-T','--threadnum'):
                threadNum = int(arg)
            elif opt in('-b','--buffer'):
                bufferSize = int(arg)
            elif opt in ('-n','--blocksize'):
                blockSize = int(arg)
    except:
        printHelpInfo()
        exit(-1)
    if type == 'server':
        s  = Server(path,port,bufferSize,blockSize)
        s.serverTransferFileProcess()
    elif type == 'client':
        c = Client(path,ip,bufferSize,threadNum)
        c.receiveFileProcess()
    else:
       printHelpInfo()


if __name__ == '__main__':
    main(sys.argv[1:])
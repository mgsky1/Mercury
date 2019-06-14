# Mercury
![](https://img.shields.io/badge/Python-3.6+-brightgreen.svg)
![](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20x64-blue.svg)
# Summary
一个简单跨平台的局域网P2P文件传输工具，目前支持Windows/Linux
# Usage
```shell
    当本机作为客户端时：
    mercury -t client -p path -i serverIP [-P port -T threadnum -b buffer -n blocksize]
    当本机作服务器为时：
    mercury -t server -p path [-P port -T threadnum -b buffer -n blocksize]
    参数含义：
    -t or --type 表示类型(必须) 值：server/client
    -p or --path 表示文件路径(必须) 值：server端为文件路径 client端为目录
    -i or --ip   表示服务器地址(客户端时必须) 值：默认本机127.0.0.1
    -P or --port 表示程序要使用的端口号(可选) 值：默认9000
    -T or --threadnum 表示客户端同时接收的线程数(可选) 值：默认为2
    -b or --buffer 表示网络传输时的缓冲区大小(可选) 值：默认1M
    -n or --blocksize 表示文件的分块大小(可选) 值：默认100M
```
# Download
[二进制文件下载](https://github.com/mgsky1/Mercury/releases)
# Features
> * 当本机作为服务器时，若传入的路径是目录，则会将其以及子目录中的所有文件打包成zip文件后传输
> * 支持多线程传输/下载数据
> * 支持大文件分块传输以提高效率
> * 传输进度使用了`tqdm`库，进度直观
> * 命令行提供多种参数，例如线程数、文件分块大小等可供用户设置，方便在不同的网络环境和具体场景中达到较理想的传输效果
> * 服务器端启动时直接显示其IP地址，免除查询烦恼

# Application Scenario
> * 当前许多笔记本电脑，例如苹果的Macbook系列，正逐渐取消USB-A接口，而目前U盘等设备
还是以该接口为主流，带一根USB-A的转接线一定是以简很麻烦的事。这个小工具就可以解决这个问题。
> * 有时候想在同一局域网中的两台电脑上传输文件，这两台电脑的距离比较进，例如在同一办公室
    或者家里，有时并不想使用U盘传输文件，这个小工具可以解决这个问题。
> * 两台电脑传输文件的时候，会经常用到一些传输助手，如果两台计算机在同一局域网环境，这么
    做不是很合算，毕竟利用到外网的带宽，这个小工具是利用局域网带宽进行的，速度会好一些。
> * 现在有的笔记本电脑提供较少的USB-A接口，平时可能会出现接口不够用，没地插U盘的情况，这个小工具可以缓解该问题。
# Performance
测试环境，局域网中的两台计算机，两台计算机均装有Windows 10 Pro。一台无线接入，一台有线接入
传输一个4.2GB大小的文件，客户端开启4线程同时下载，整个过程(包括前期准备、分割文件、传输、验证)
大约需要15分钟。若两台计算机均有线接入，相同条件下，时间会缩短到10分钟左右。

# Attention
> * 请不要将该工具作为局域网分发文件的工具。
> * 因为是基于P2P设计的，所以开启一个服务器后，不要多开客户端，否则可能会造成文件块丢失。
> * 若涉及文件分块传输，需要更大一些的磁盘空间来存放文件块。不过
    不用担心，这些临时文件会在传输成功后或在分块开始前(工具会检测是否存在临时文件)移除。
> * 若涉及文件分块，在该文件所在的目录中不要有`MEtemp`目录，因为这个是块文件暂存目录，
    若有同名目录的话，在分块前会进行移除，若有同名目录，请及时更名，否则会造成数据丢失。
> * 目录打包的文件名为`dirpack.zip`，在目录中有重名文件，可能会造成覆盖。

# Note
> * 基于Python 3
> * 依赖与`tqdm`、`zipfile`库
> * 单元测试基于`unittest`
> * 软件的开发工具为`PyCharm`，在每个`.py`文件头，均有`Pycharm使用`
    的注释，进行开发时，将其打开即可，当然，前面对应的引入要注释掉
> * `PyCharm`导入的时候项目名为`PythonFileTransfer`

# About Project Name
*图片来自 BaiduImage*
<br>
![](https://blog.acmsmu.cn/wp-content/uploads/2019/06/1394781409282.jpg)
<br>
`Mercury`又名水星，是太阳系最内侧，最靠近太阳，也是最小的一颗行星。
<br>
这也是我GitHub上第一个比较"像样"一点的项目。
<br>
主要是这半年来比较迷刘慈欣的三体，然后三体人针对的是太阳系，就琢磨着是否可以用太阳系的行星来命名自己的项目。
<br>
就好比`Hadoop`名称的由来，本身并没有非常大的意义，也不是什么缩写，就是偶然~


# Screen Shots
![](https://blog.acmsmu.cn/wp-content/uploads/2019/06/20190609093238.png)

# ChangeLog
> * 2019/06/03 完成项目基本骨架
> * 2019/06/08 项目调试以及Bug修复

# Contribution
我不敢说这个项目会不会得到大家的认可，至少它可以方便我自己。
TCP文件传输也算是一个比较简单的项目，但要做的细与好，还真不是一件容易的事情！
如果它也能帮助到你，我表示感谢。也欢迎Star 或 Fork，有Bug也
可以题，或者提交Pull Request，让这个项目变得更好~

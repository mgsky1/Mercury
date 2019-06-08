'''
@desc:测试类
@author: Martin Huang
@time: created on 2019/5/15 21:29
@修改记录:
'''
import unittest
from src.main.Utils.NetUtils import *

class TestFunctions(unittest.TestCase):
    def test_net(self):
        NetUtils.receiveSigFile('E:\\ray.rar','127.0.0.1')

if __name__ == '__main__':
    unittest.main()
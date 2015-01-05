# 解决epub文件无法正常显示中文的问题
# （其根本原因是，内容网页中没有指明是语言类型，因此阅读器无法识别）
#
#
# 使用方法：
# 1. 将epub解压
# 2. 将这个程序，放到包含epub内容的文件夹（有许多html，htm，xhtml的地方）内
# 3. 运行
# 4. 回到根目录全选打包成zip，重命名为epub

import glob

cn = '''<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">'''

files = glob.glob(".\\*.html")

for f in files:
    fh = open(f,"r")
    fc = fh.readlines()
    for i in xrange(0,len(fc)):
        cwords = fc[i].split(" ")
        if "<html" == cwords[0]:
            fc[i] = cn+"\n"
    fh.close()
    fh = open(f,"w")
    for i in xrange(0,len(fc)):
        fh.write(fc[i])
    fh.close()
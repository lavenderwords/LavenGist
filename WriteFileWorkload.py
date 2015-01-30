import sys
import time
import subprocess
num_of_blk = 16384
num_of_MB  = 16
time_blk = 1
duration_per_round = 60
num_of_round = 10
blk_content = "0000000011111111222222223333333344444444555555556666666677777777"
# def gen_blk(blk_size,blk_content):
#     blk = ""
#     for x in xrange(1,blk_size):
#         blk.append(blk_content)
#     return blk
def gen_file(num_of_blk):
    '''
    生成1MB的内容
    '''
    file_contents = ""
    for x in xrange(1,num_of_blk):
        file_contents += blk_content
    return file_contents
# file = open("testfile.txt","a")
# for x in xrange(0,num_of_MB):
#    file.write(gen_file(num_of_blk))
# file.close()

# 每秒钟生成一个文件
for r in xrange(0,num_of_round):
    print r
    for c in xrange(0,duration_per_round):
        print c
        f = open("suyi"+str(c),"w")
        f.write(gen_file(num_of_blk))
        f.close()
        time.sleep(time_blk)
    subprocess.Popen(["rm","-f","/mnt/suyi*"],stdout=subprocess.PIPE)
    print "clear"
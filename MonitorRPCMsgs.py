# 监控RPC中以N开头的消息（过滤出NFS相关的消息）
# 统计30s内不同类型的RPC消息的数量
import subprocess
import time
stime = time.time()
result = {}
count = 0
proc = subprocess.Popen(["tshark","-i","eth1","-V"],stdout=subprocess.PIPE)
for line in iter(proc.stdout.readline,''):
    if line[0] == "N":
        opline = line.split("\n")[0].split(":")[1]
        ops = opline.split(" ")[1:]
        count += len(ops)
        for o in ops:
            if o in result:
                result[o] = result[o] + 1
            else:
                result[o] = 1
    if time.time()-stime >= 30:
        stime = time.time()
        print result
        print count
        result = {}
        count = 0
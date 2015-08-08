import random
from multiprocessing import Pool
# import sys
# filename = sys.argv[1]


def transTrace(filename):
    timeBase = 0
    timeRange = 60 * 60 * 100
    timeSlot = [[] for i in xrange(timeRange)]

    with open(filename, 'r') as dumps:
        for l in dumps:
            ll = l.split(' ')
            count = int(ll[2])
            if ll[3][-1] == "\n":
                bs = long(ll[3][:-1])
            else:
                bs = long(ll[3])
            size = bs / count
            newl = "%s %s %d\n" % (ll[0], ll[1], size)
            # print newl
            for c in xrange(count):
                ts = random.randint(0, timeRange - 1)
                timeSlot[ts].append("%d %s" % (timeBase + ts, newl))

    f = open("./lavenSeq/LavenSeq" + filename, "w")
    ts = 0
    while True:
        try:
            requests = timeSlot.pop(0)
            # reqs = []
            # for rq in requests:
            #     reqs.append(str(timeBase + ts) + " " + rq + "\n")
            if requests != []:
                # print ts
                # print requests
                f.writelines(requests)
            ts += 1
        except:
            break
    f.close()


if __name__ == '__main__':
    jobs = []
    for i in xrange(24):
        if i == 15:
            continue
        si = str(i)
        if len(si) < 2:
            si = "0" + si
        fn = "pagecounts-20150801-%s0000" % (si)
        print fn
        jobs.append(fn)
    p = Pool(3)
    p.map(transTrace, jobs)
    # transTrace(fn)

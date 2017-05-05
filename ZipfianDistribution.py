#!/usr/bin/env python
import random

class zipfian(object):
    # The algorithm used here is from "Quickly Generating Billion-Record Synthetic Databases", Jim Gray et al, SIGMOD 1994.
    def __init__(self, item_min, item_max, zipfianconstant=0.99):
        self.lastVal = None
        self.items = item_max - item_min + 1
        self.base = item_min
        self.zipfianconstant = zipfianconstant
        self.theta = self.zipfianconstant
        self.alpha = 1.0 / (1.0 - self.theta)
        self.zetan = self.zetastatic(self.items, self.zipfianconstant)
        self.zeta2theta = self.zeta(2, self.theta)
        self.countforzeta = self.items
        self.eta = (1 - (2.0/self.items)**(1-self.theta)) / (1 - (self.zeta2theta/self.zetan))
        self.allowitemcountdecrease = False
        self.__next__()

    def zeta(self, n, thetaVal, st=0, initialsum=0):
        self.countforzeta = n
        return self.zetastatic(n, thetaVal, st=st, initialsum=initialsum)

    def zetastatic(self, n, theta, st=0, initialsum=0):
        s = initialsum
        for i in range(st, n):
            s += 1.0 / ((i+1)**theta)
        return s

    def __next__(self):
        u = random.random()
        uz = u * self.zetan
        if uz < 1.0:
            return self.base
        if uz < 1.0 + 0.5**self.theta:
            return self.base+1
        ret = self.base + long(self.items * (self.eta * u - self.eta + 1)**self.alpha)
        self.setLastValue(ret)
        return ret

    def next(self):
        return self.__next__()

    def setLastValue(self, last):
        self.lastVal = last


if __name__ == "__main__":
    zipf = zipfian(0, 1000000)
    item_counts = {}
    for i in range(1000000):
        item = zipf.next()
        item_counts[item] = item_counts.get(item, 0) + 1
    sorted_ic = sorted(item_counts.items(), key=lambda x:x[1])
    for i in range(1, 10):
        print sorted_ic[i], sorted_ic[-i]

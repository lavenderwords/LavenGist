#!/usr/bin/env python
# _*_ coding:UTF-8
# http://blog.lifeeth.in/2011/03/reading-raw-disks-with-python.html
possible_drives = [
        r"\\.\PhysicalDrive1", # Windows
        r"\\.\PhysicalDrive2",
        r"\\.\PhysicalDrive3",
        "/dev/mmcblk0", # Linux - MMC
        "/dev/mmcblk1",
        "/dev/mmcblk2",
        "/dev/sdb", # Linux - Disk
        "/dev/sdc",
        "/dev/sdd",
        "/dev/disk1", #MacOSX 
        "/dev/disk2",
        "/dev/disk3",
        ]

import random
import time
import sys
import os
import mmap
import ctypes
import ctypes.util
libc = ctypes.CDLL(ctypes.util.find_library('c'))

one_KB = 1024
one_MB = 1024*one_KB
one_GB = 1024*one_MB
one_TB = 1024*one_GB
sector_size = 512
block_size = 4*one_KB


def ctypes_alloc_aligned(size, alignment):
    buf_size = size + (alignment - 1)
    raw_memory = bytearray(buf_size)
    ctypes_raw_type = (ctypes.c_char * buf_size)
    ctypes_raw_memory = ctypes_raw_type.from_buffer(raw_memory)
    raw_address = ctypes.addressof(ctypes_raw_memory)
    offset = raw_address % alignment
    offset_to_aligned = (alignment - offset) % alignment
    ctypes_aligned_type = (ctypes.c_char * (buf_size - offset_to_aligned))
    ctypes_aligned_memory = ctypes_aligned_type.from_buffer(raw_memory, offset_to_aligned)
    return ctypes_aligned_memory


def get_max_address(dev_name):
    disk = file(dev_name, 'rb')
    max_addr = one_TB
    while max_addr > 0:
        try:
            disk.seek(max_addr)
            break
        except:
            max_addr -= 5 * one_GB
    return max_addr


class rand_address(object):

    def __init__(self, count, dev_name, sector_size=512):
        self.max_addr = get_max_address(dev_name)
        self.max_sector = self.max_addr / sector_size
        self.count = count
        # self.sectors = [random.randint(0, self.max_sector) for i in range(count)]
        self.sectors = set()
        while len(self.sectors) < count:
            self.sectors.add(random.randint(0, self.max_sector))
        self.addrs = [s*sector_size for s in self.sectors]

    def get_addr(self):
        return random.choice(self.addrs)

    def get_n_addr(self, n):
        for i in range(n):
            yield self.get_addr()


if __name__ == "__main__":
    addr_count = long(sys.argv[1])
    dev_name = sys.argv[2]
    req_count = long(sys.argv[3])

    duration = 0.0

    #disk = open(dev_name, "rb")
    disk = os.open(dev_name, os.O_RDONLY | os.O_DIRECT)
    ra = rand_address(addr_count, dev_name)
    start_time = time.time()
    for addr in ra.get_n_addr(req_count):
        st = time.time()
        #disk.seek(addr)
        os.lseek(disk, addr, os.SEEK_SET)
        #content = disk.read(block_size)
        #buff = mmap.mmap(-1, block_size)
        buff =ctypes_alloc_aligned(block_size, sector_size)
        err_code = libc.read(ctypes.c_int(disk), buff, ctypes.c_int(block_size))
        #print err_code
        duration += time.time() - st

    print dev_name, addr_count, req_count
    print "Running Time", time.time() - start_time
    print "Duration: ", duration
    print "Avg. Latency: ", duration / req_count
    bw = req_count * block_size / duration
    print "Bandwidth: ", "%.2f MB/s" % (bw/one_MB), bw

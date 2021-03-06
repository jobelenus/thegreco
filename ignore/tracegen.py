#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import collections
#import matplotlib.pyplot as plt

factor = 1/4

class TraceGenerator():
  
      
    def __init__(self):
        fname='/Users/jobelenus/work/thegreco/cpu.entries'
        self.fname = fname
        with open(self.fname) as f:
            self.lines = f.readlines()
            self.cpu = map(int, self.lines)
      
    def gen_cpu_trace(self):
        return self.cpu

    def gen_mem_trace(self):
        self.mem = collections.deque(self.cpu)
        self.mem.rotate(len(self.cpu)/4)
        return self.mem

    def gen_disk_trace(self):
        self.disk = collections.deque(self.cpu)
        self.disk.rotate(2*len(self.cpu)/4)
        return self.disk

    def gen_net_trace(self):
        self.net = collections.deque(self.cpu)
        self.net.rotate(3*len(self.cpu)/4)
        return self.net
      
    def gen_trace(self):
        self.gen_cpu_trace()
        self.gen_mem_trace()
        self.gen_disk_trace()
        self.gen_net_trace()
        self.trace = zip(self.cpu, self.mem, self.disk, self.net)
        return self.trace

#tg = TraceGenerator()
#cpu = tg.gen_cpu_trace()
#mem = tg.gen_mem_trace()
#disk = tg.gen_disk_trace()
#net = tg.gen_net_trace()
#trace = zip(cpu, mem, disk, net)

#print trace
#plt.bar(range(0,len(cpu)), cpu)
#plt.show()

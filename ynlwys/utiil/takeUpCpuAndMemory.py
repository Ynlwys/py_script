# -*- coding: utf-8 -*

"""
    author：Ynlwys

    1.用于从检测结果上增加CPU以及内存的利用率。
    2.在增加利用率的同时不会影响到系统业务的正常运转。
        1).业务利用率增加则该程序降低
        2).业务利用率降低则该程序增加
"""

import psutil


# function of Get CPU State
def getCPUstate(interval=1):
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")


def judgmentCPUstate(v):
    vNum = str(v).split(" ");
    cpuUsed = float(vNum[2].split("%")[0]);

    if cpuUsed > 70:
        print "CPU 使用过高"
        offTakeUpCPU();

    if cpuUsed < 20:
        print "CPU 使用过低"

        onTakeUpCPU();

    print vNum[2];


def offTakeUpCPU():
    print "pkill -9 dd"


def onTakeUpCPU():
    print """for i in `seq 1 $(cat /proc/cpuinfo |grep "physical id" |wc -l)`; do dd if=/dev/zero of=/dev/null & done"""


if __name__ == '__main__':
    judgmentCPUstate(getCPUstate());

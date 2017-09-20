#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    author：Ynlwys


功能介绍：
    完成单台tomcat服务器应用文件的替换


具体步骤如下：
    1.解压文件
    2.检索文件 拼接出目录中每个文件的绝对路径
    3.对原始文件进行备份
    4.将新文件进行覆盖

方法声明：
    1.unzipAndanalysis
        : 对ROOT.zip 进行解压 并且判断当中的内容是替换还是新增
    2.backupAndDeploy
        : 根据替换目录对原文件进行备份并且对新文件进行部署
"""
import os
import time
import shutil
import zipfile
import sys

############################################################################
#
#
# 定义常用变量

# 用于接收命令行输入参数
gpus = sys.argv[1];

# 定义项目名称
ROOT = "ROOT";

# 定义项目替换文件的路径
path = "/data/script/" + ROOT + "/";

# 定义当前年月日时分秒
curDateTime = time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time()));

"""
    该类的帮助说明方法 通过调用该方法可以打印该类的其他方法
"""


def help():
    print """
    1.unzipAndanalysis(cmd: python tomcatAppFileDeploy.py bad)
        : 对ROOT.zip 进行解压 并且判断当中的内容是替换还是新增
    2.backupAndDeploy(cmd: python tomcatAppFileDeploy.py bad)
        : 根据替换目录对原文件进行备份并且对新文件进行部署
    """


"""
    对需要进行部署替换的压缩包文件进行解压和分析
"""


def unzipAndanalysis():
    ############################################################################
    #
    #
    # 清空替换文件列表
    jfiles = open('/data/script/fileList', 'r+w');
    jfiles.truncate();

    # 进行压缩文件的解压
    if os.path.exists("/data/script/" + ROOT + ".zip"):
        zf = zipfile.ZipFile("/data/script/" + ROOT + ".zip", 'r');
        for file in zf.namelist():
            print(file);
            zf.extract(file, "/data/script/");
    else:
        print "请确认/data/script/" + ROOT + ".zip是否存在";
        exit(-1);

    ############################################################################
    #
    #
    # 对目录进行遍历 找寻存在文件的路径全地址 并将其存放至替换列表文件中
    for i in os.walk(path):
        subString = i[0] + "/";
        for j in i[2]:
            print >> jfiles, subString[12:] + j;

    jfiles.close();

    ############################################################################
    #
    #
    # 判断文件是进行添加还是替换 并将信息进行输出 由使用者判断是否需要进行添加或者替换
    jfiles = open('/data/script/fileList', 'r');
    for jfile in jfiles:
        # print "/opt/tomcat/webapps" + jfile;
        if os.path.exists(("/opt/tomcat/webapps" + jfile).replace("\n", "")):
            print ("/opt/tomcat/webapps" + jfile).replace("\n",
                                                          "") + "--" + "文件已存在，可进行替换（命令：python tomcatAppFileDeploy.py bad）,如文件不匹配请停止接下来的操作"
        else:
            print ("/opt/tomcat/webapps" + jfile).replace("\n",
                                                          "") + "--" + "文件不存在，可进行添加（命令：python tomcatAppFileDeploy.py bad）,如文件不匹配请停止接下来的操作"

    jfiles.close();


"""
    对原有文件进行备份(根据时间创建文件夹、cp原由文件、对更新文件路径进行保存 cp fileList文件)并对新文件进行部署
"""


def backupAndDeploy():
    ############################################################################
    #
    #
    # 分别对新旧文件判断是否存在 并进行备份与替换

    # 判断新文件是否存在
    if os.path.exists("/data/script/" + ROOT + "/") == False:
        print "请确认/data/script/" + ROOT + "/是否存在";
        exit(-1);

    jfiles = open('/data/script/fileList', 'r');
    os.mkdir("/data/script/" + ROOT + "_bak/" + curDateTime);

    shutil.copyfile("/data/script/fileList", "/data/script/" + ROOT + "_bak/" + curDateTime + "/fileList");

    # 判断旧文件是否存在 并且对其进行备份
    for jfile in jfiles:
        if os.path.exists(("/opt/tomcat/webapps" + jfile).replace("\n", "")):
            shutil.move(("/opt/tomcat/webapps" + jfile).replace("\n", ""),
                        ("/data/script/" + ROOT + "_bak/" + curDateTime).replace("\n", ""));

        # 对新文件进行部署 并且对操作结果进行输出
        shutil.copyfile(("/data/script" + jfile).replace("\n", ""), ("/opt/tomcat/webapps" + jfile).replace("\n", ""));
        print ("/opt/tomcat/webapps" + jfile).replace("\n", "") + "-文件部署成功";

    jfiles.close();


"""
    判断替换文件列表中是否包含了需要进行重启的文件 比如 .class or .xml
"""


def isRestart():
    ############################################################################
    #
    #
    # 如果有需要重启的文件 该方法会重启tomcat 但是只会重启一次

    jfiles = open('/data/script/fileList', 'r');

    for jfile in jfiles:
        if ".class" in str(jfile) or ".xml" in str(jfile):
            os.system('service tomcat restart');
            exit(-1);

    jfiles.close();


"""
    主方法 在调用该类的时候需要跟上参数 help or uaa or bad
"""
if (__name__ == '__main__'):
    print "参数 = " + gpus;

    if gpus == "help" or gpus == "":
        help();
    else:
        if gpus == "uaa":
            unzipAndanalysis();
        else:
            if gpus == "bad":
                backupAndDeploy();
                isRestart();




# 将运行中的tomcatAPP添加压缩包至对应目录

# rootFile = zipfile.ZipFile("/data/script/"+ROOT+"_bak/"+curDateTime,'w',zipfile.ZIP_DEFLATED);
# rootFile.write("/opt/tomcat/webapps/");
# rootFile.close();



###---- 暂时无用 ----###

############################################################################
#
# 停止正在运行中的tomcat服务


############################################################################
#
# 对已经备份好的tomcatAPP进行删除


############################################################################
#
# 启动tomcat服务

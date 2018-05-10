# -*- coding: utf-8 -*
# 处理Excel的包

"""
    author：Ynlwys



"""


import xlrd;
import xlwt;
import datetime;
import  time;
import sys
import random
import re


reload(sys);
sys.setdefaultencoding("utf-8");



"""
    1.已经可以针对人员进行分析。
    2.需要对时间进行分析（添加）。

    定义刷卡记录类。
    
    包含字段如下：
        
        人员姓名 - userName
        刷卡时间 - useTime


"""


class Record:
    def __init__(self,userName,useTime):

        self.userName = userName
        self.useTime = useTime





"""
    0.打开Excel。
    1.获取第一个table。
    2.获取行数。
    3.获取列数。
    4.双层循环遍历对取出每个单元格数据。
    5.将Excel中时间戳数据进行还原成日期格式。
    6.创建Map对象，将重复数据进行过滤，取出每个人最早和最晚的数据。
        0.首先对数据进行排序，按照时间顺序(正序+倒叙)。
        1.将排序的数据依次放入map当中，key重复则进行替换。
        2.最后替换过重复的数据便是最终的数据。
    7.将取出后的数据重新写入到excel当中。
"""


## 定义每个数据列
userName = "";
useTime = "";
flag = 1;


## 进行读取的文件路径。
workbook = xlrd.open_workbook('E:\\1.xls');
## 设定需要读取的sheets。
table = workbook.sheets()[0];

# 获取行数和列数。
nrows = table.nrows;
ncols = table.ncols;


#判断名字是否重复map。
nameRe = dict();
# 最大值数组，当中包含考勤时间的最大值。
maxAttendanceDate = dict();
# 最小值数组，当中包含考勤时间的最小值。
minAttendanceDate = dict();
#汇总数据，当中包含了 每个人的最大最小值。
#countAttendanceDate = dict();
##存放记录信息的map
recordList = [];

##存放记录信息的map
flagmap = dict();

row = 1;

# 取出
for i in range(nrows):
    # 跳过表头
    if i==0:
        continue;

    #统计出每个用户的最大值。
    minAttendanceDate.setdefault(table.cell(i, 0).value.encode("utf-8")+(str(datetime.datetime.fromtimestamp(((table.cell(i, 1).value)-70*365-19)*86400-8*3600))).split(" ")[0],datetime.datetime.fromtimestamp(((table.cell(i, 1).value)-70*365-19)*86400-8*3600));

    #将记录信息保存到字段中。
    userName = table.cell(i, 0).value.encode("utf-8");
    useTime = table.cell(i, 1).value;

    #将记录字段封装到对象里。
    info = Record(userName,useTime);

    #将对象封装到List中。
    recordList.append(info);


j = nrows - 1;

#保存每个用户的最小值。
while (j > 0):
    maxAttendanceDate.setdefault(table.cell(j, 0).value.encode("utf-8")+(str(datetime.datetime.fromtimestamp(((table.cell(j, 1).value)-70*365-19)*86400-8*3600))).split(" ")[0],datetime.datetime.fromtimestamp(((table.cell(j, 1).value)-70*365-19)*86400-8*3600));

    j = j -1;

"""
    设置Excel格式。

"""
newWorkbook = xlwt.Workbook();
newTable = newWorkbook.add_sheet('Attendance'.decode(),cell_overwrite_ok=True);

# 表头字体样式以及大小。
headStyle = xlwt.XFStyle();
headFont = xlwt.Font();
headFont.bold = True;
headFont.height = 360;

headFont.name = u'微软雅黑';
headStyle.font = headFont;

# 表格内容样式以及大小。
style = xlwt.XFStyle();
font = xlwt.Font();
font.height = 300;
style.font = font;

# 表格内时间数据格式。
style = xlwt.XFStyle();
style.num_format_str = 'yyyy/m/d h:mm AM/PM'


# 设置列宽。
firstWidth_col = newTable.col(0);
secendWidth_col = newTable.col(1);

firstWidth_col.width = 256 * 20;
secendWidth_col.width = 256 * 20;


# 设置列的单元格格式。

#设置表头。
#newTable.write(0, 0, "CtrlEventNo",headStyle);
newTable.write(0, 0, "UserName",headStyle);
newTable.write(0, 1, "UseTime",headStyle);


#对list进行遍历，正常数据写入到Excel 中。
for i, val in enumerate(recordList):
    #print ("序号：%s   值：%s" % (i + 1, val.cardNum));
    #newTable.write(row, 0,val.recordNum, style);
    newTable.write(row, 0,val.userName.decode('utf-8'), style);
    newTable.write(row, 1,val.useTime, style);

    row = row + 1;

"""
    对最大值最小值进行分析，判断合理值。

    
"""
#print "汇总时间："
for (k,v) in  minAttendanceDate.items():
    maxTime = str(maxAttendanceDate.get(k));
    minTime = str(v);

    #去重操作，如果该条记录补充过一次，即不再进行补充。
    if nameRe.get(k) == 1:
        continue;


    #print maxTime;
    #print minTime;

    #最终需要补充的时间。
    finalTime = "";
    #最大时间值。
    mxd = datetime.datetime.strptime(maxTime, '%Y-%m-%d %H:%M:%S');
    #最小时间值。
    mnd = datetime.datetime.strptime(minTime, '%Y-%m-%d %H:%M:%S');
    #最大最小中间值。
    mcd = str(mxd.date()) + " 12:00:00";
    #根据字符串获取时间对象。
    mcd = datetime.datetime.strptime(mcd, '%Y-%m-%d %H:%M:%S');


    #最大阈值
    mxyd = str(mxd.date()) + " 21:00:00";
    mxyd = datetime.datetime.strptime(mxyd, '%Y-%m-%d %H:%M:%S');
    #最小阈值
    mnyd = str(mxd.date()) + " 08:00:00";
    mnyd = datetime.datetime.strptime(mnyd, '%Y-%m-%d %H:%M:%S');
    # 最小阈值
    mnydBase = str(mxd.date()) + " 09:00:00";
    mnydBase = datetime.datetime.strptime(mnydBase, '%Y-%m-%d %H:%M:%S');


    #测试
    # t1 = datetime.datetime.strptime('2017-07-07 11:00:00', '%Y-%m-%d %H:%M:%S');
    # tz = datetime.datetime.strptime('2017-07-07 12:00:00', '%Y-%m-%d %H:%M:%S');
    # t2 = datetime.datetime.strptime('2017-07-07 13:00:00', '%Y-%m-%d %H:%M:%S');
    #
    # print t1 > tz;
    # print t2 > tz;


    #判断最大最小时间值的时间差。
    delta = mxd - mnd;

    delta = delta.seconds / 60 / 60;

    print "delta", delta;
    print "mxd", mxd;
    print "mnd", mnd;
    print "mcd", mcd;

    #随机时间9小时+-30分钟。
    randomNum = random.uniform(1000, 2000) + 32400;

    finalTime = "";


    #如果上班时间不足8小时
    if delta < 8:
        #如果时间值是下午，则进行。
        if mxd > mcd :
            #print (mxd - mcd).seconds;
            finalTime = mxd - datetime.timedelta(seconds=randomNum);

            if mnd < mcd:
                finalTime = mnd + datetime.timedelta(seconds=randomNum);

        elif mxd < mcd :
            #print (mxd - mcd).seconds;
            finalTime = mxd + datetime.timedelta(seconds=randomNum);
            print "finalTime = ", finalTime;


        #过滤出没有正确信息的人员
        name = re.sub("-|[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", k);

        for i, val in enumerate(recordList):


            if val.userName == name:
                print name + " - 未正确打卡";
                userName = val.userName;
                useTime = finalTime;


                if useTime > mxyd:
                    useTime = mxyd - datetime.timedelta(seconds=random.uniform(1000, 2000));

                if useTime < mnyd:
                    useTime = mxyd + datetime.timedelta(seconds=random.uniform(1000, 1500));


                if userName == "李四":
                    flagmap.setdefault(k,1);
                    newTable.write(row, 0, userName.decode('utf-8'), style);
                    newTable.write(row, 1, useTime, style);
                    nameRe.setdefault(k, 1);
                    row = row + 1;
                    flag = 0;

                recordList.remove(val);

                break;

    if mnd > mnydBase:
        newTable.write(row, 0, userName.decode('utf-8'), style);
        newTable.write(row, 1, mnyd + datetime.timedelta(seconds=random.uniform(2500, 3500)), style);
        nameRe.setdefault(k, 1);
        row = row + 1;
        flag = 1;
"""
   将过滤完成的数据，重新写入到excel当中。
"""
newWorkbook.save('F:\\2017.12.xls');

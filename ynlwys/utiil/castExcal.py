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
    定义刷卡记录类。
    
    包含字段如下：
        
        记录序号 - recordNum
        卡片序号 - cardNum
        卡片类型 - cardType
        人员姓名 - userName
        人员编号 - userNum
        部门名称 - userDep
        通行原由 - useDes
        房门编号 - doorNum
        刷卡时间 - useTime
        公司名称 - orzName        

"""


class Record:
    def __init__(self, recordNum, cardNum, cardType,userName,userNum,userDep,useDes,doorNum,useTime,orzName):
        self.recordNum = recordNum
        self.cardNum = cardNum
        self.cardType = cardType
        self.userName = userName
        self.userNum = userNum
        self.userDep = userDep
        self.useDes = useDes
        self.doorNum = doorNum
        self.useTime = useTime
        self.orzName = orzName




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
recordNum = "";
cardNum = "";
cardType = "";
userName = "";
userNum = "";
userDep = "";
useDes = "";
doorNum = "";
useTime = "";
orzName = "";

## 进行读取的文件路径。
workbook = xlrd.open_workbook('E:\\2017.5-6.xls');
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
row = 1;

# 取出
for i in range(nrows):
    # 跳过表头
    if i==0:
        continue;

    #统计出每个用户的最大值。
    minAttendanceDate.setdefault(table.cell(i, 3).value.encode("utf-8")+(str(datetime.datetime.fromtimestamp(((table.cell(i, 8).value)-70*365-19)*86400-8*3600))).split(" ")[0],datetime.datetime.fromtimestamp(((table.cell(i, 8).value)-70*365-19)*86400-8*3600));

    #将记录信息保存到字段中。
    recordNum = table.cell(i, 0).value;
    cardNum = table.cell(i, 1).value.encode("utf-8");
    cardType = table.cell(i, 2).value.encode("utf-8");
    userName = table.cell(i, 3).value.encode("utf-8");
    userNum = table.cell(i, 4).value;
    userDep = table.cell(i, 5).value.encode("utf-8");
    useDes = table.cell(i, 6).value.encode("utf-8");
    doorNum = table.cell(i, 7).value;
    useTime = table.cell(i, 8).value;
    orzName = table.cell(i, 9).value.encode("utf-8");

    #将记录字段封装到对象里。
    info = Record(recordNum,cardNum,cardType,userName,userNum,userDep,useDes,doorNum,useTime,orzName);

    #将对象封装到List中。
    recordList.append(info);


j = nrows - 1;

#保存每个用户的最小值。
while (j > 0):
    maxAttendanceDate.setdefault(table.cell(j, 3).value.encode("utf-8")+(str(datetime.datetime.fromtimestamp(((table.cell(j, 8).value)-70*365-19)*86400-8*3600))).split(" ")[0],datetime.datetime.fromtimestamp(((table.cell(j, 8).value)-70*365-19)*86400-8*3600));

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
newTable.write(0, 0, "CardNum",headStyle);
newTable.write(0, 1, "CardType",headStyle);
newTable.write(0, 2, "UserName",headStyle);
newTable.write(0, 3, "UserNum",headStyle);
newTable.write(0, 4, "UserDepName",headStyle);
newTable.write(0, 5, "UseDes",headStyle);
newTable.write(0, 6, "DoorNum",headStyle);
newTable.write(0, 7, "UseTime",headStyle);
newTable.write(0, 8, "OrzName",headStyle);


#对list进行遍历，正常数据写入到Excel 中。
for i, val in enumerate(recordList):
    #print ("序号：%s   值：%s" % (i + 1, val.cardNum));
    #newTable.write(row, 0,val.recordNum, style);
    newTable.write(row, 0,val.cardNum.decode('utf-8'), style);
    newTable.write(row, 1,val.cardType.decode('utf-8'), style);
    newTable.write(row, 2,val.userName.decode('utf-8'), style);
    newTable.write(row, 3,val.userNum, style);
    newTable.write(row, 4,val.userDep.decode('utf-8'), style);
    newTable.write(row, 5,val.useDes.decode('utf-8'), style);
    newTable.write(row, 6,val.doorNum, style);
    newTable.write(row, 7,val.useTime, style);
    newTable.write(row, 8,val.orzName.decode('utf-8'), style);

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
                cardNum = val.cardNum;
                cardType = val.cardType;
                userName = val.userName;
                userNum = val.userNum;
                userDep = val.userDep;
                useDes = val.useDes;
                doorNum = val.doorNum;
                useTime = finalTime;
                orzName = val.orzName;


                if useTime > mxyd:
                    useTime = mxyd - datetime.timedelta(seconds=random.uniform(1000, 2000));

                if useTime < mnyd:
                    useTime = mxyd + datetime.timedelta(seconds=random.uniform(1000, 2000));

                newTable.write(row, 0, cardNum.decode('utf-8'), style);
                newTable.write(row, 1, cardType.decode('utf-8'), style);
                newTable.write(row, 2, userName.decode('utf-8'), style);
                newTable.write(row, 3, userNum, style);
                newTable.write(row, 4, userDep.decode('utf-8'), style);
                newTable.write(row, 5, useDes.decode('utf-8'), style);
                newTable.write(row, 6, doorNum, style);
                newTable.write(row, 7, useTime, style);
                newTable.write(row, 8, orzName.decode('utf-8'), style);

                recordList.remove(val);

                nameRe.setdefault(k,1);

                row = row + 1;

                break;

"""
   将过滤完成的数据，重新写入到excel当中。
"""
newWorkbook.save('F:\\2017.5-6.xls');

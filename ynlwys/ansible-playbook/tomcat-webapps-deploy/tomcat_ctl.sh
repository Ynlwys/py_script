#!/bin/bash
DATE=`date +%Y%m%d-%H%M%S`
TPID1=`ps aux|grep tomcat|grep Xms|grep tomcat_end|awk  '{print $2}'`
TPID2=`ps -aux|grep tomcat |grep Xms|grep opt/tomcat/bin|awk  '{print $2}'`
TSTART1="/opt/tomcat_end/bin/startup.sh"
TSTART2="/opt/tomcat/bin/startup.sh"

JAVA_HOME=/opt/jdk
JRE_HOME=$JAVA_HOME/jre
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
export JAVA_HOME JRE_HOME CLASSPATH PATH

if [ $1 == stop ]
then
kill -9 $TPID1  && echo "tomcat_end shutdown OK"
kill -9 $TPID2  && echo "tomcat_web shutdown OK"
fi

if [ $1 == start ]
then
su - somp -c "sh $TSTART1"
su - somp -c "sh $TSTART2"
fi

if [ $1 == bakup ]
then

mkdir -p /data/script/tomcat/$DATE && cp -r /opt/tomcat/webapps/* /data/script/tomcat/$DATE
mkdir -p /data/script/tomcat_end/$DATE && cp -r /opt/tomcat_end/webapps/* /data/script/tomcat_end/$DATE

fi

if [ $1 == restart ]
then
kill -9 $TPID1  && echo "tomcat_end shutdown OK"
kill -9 $TPID2  && echo "tomcat_web shutdown OK"
sleep 2
su - somp -c "sh $TSTART1 && echo 'tomcat_end start OK'"
su - somp -c "sh $TSTART2 && echo 'tomcat_web start OK'"
fi
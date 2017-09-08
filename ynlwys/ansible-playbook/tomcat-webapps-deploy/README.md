功能描述
=======

> 通过ansible-playbook对多台tomcat进行应用部署
> 
> 该文件的使用基于ansible已经配置完成的情况


使用方式如下
===========

#### 1.客户端安装

```
mkdir -p /data/script

cp tomcat_ctl.sh /data/script/tomcat_ctl.sh

chmod 755 /data/script/tomcat_ctl.sh

ln -s /data/script/tomcat_ctl.sh /usr/sbin/tomcat_ctl


# 测试
tomcat_ctl restart 

```


#### 2.tomcat服务安装(是指启动脚本而并非应用)

```
cp tomcat /etc/init.d/tomcat

chmod 755 /etc/init.d/tomcat

# 测试
service tomcat restart
```


#### 3.yml文档编写

```
cp tomcat-webapps-deploy.yml /data/script/

```
   
#### 4.ansible执行

```
cd /data/script/

ansible-playbook tomcat-webapps-deploy.yml

```
   
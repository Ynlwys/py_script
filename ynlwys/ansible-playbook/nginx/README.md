使用方式如下
===========

>   --extra-vars "server_hostname=192.168.122.11" 属于变量定义部分。
> 
>   

   * `ansible-playbook site.yml --extra-vars "server_hostname=192.168.122.11"`
   
   
   
各个配置文件说明
=================

## site.ymml
   程序入口


## role/nginx/handler/main.yml

   用于控制nginx,对nginx进行重启操作 
   
   
## role/nginx/tasks/main.yml
   用于进行nginx安装
   
   
## role/nginx/templates/default.conf
   nginx配置文件
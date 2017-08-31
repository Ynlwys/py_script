Ansible基本使用
==============

> Ansible 是用于批量管理服务器的工具
>
> Ansible相对与Cfengine、Puppet、SaltStack 来说更加的轻量级，更加的便捷
>
> Ansible本身可以不需要使用客户端而直接通过ssh的方式进行连接管理服务器


---



#### Ansible的安装

1.首先安装 epel

- `yum -y install epel-release`

2.然后安装Ansible

- `yum -y install ansible`

3.安装完成之后简单配置ansible默认的hosts文件
```shell
vim /etc/ansible/hosts

[serverName]
192.168.122.11
```
#### Absible的第一条命令
- `ansible -i elk elk -u root -m command -a 'uptime' -k`


#### 关于Ansible的第一条命令的解释
- `ansible : 工具的主程序、主命令`
- `-i : 指定hosts文件的参数 如果不是使用则使用默认文件`
- `elk[1] : 配置文件路径 如 /etc/ansible/hosts` 
- `elk[2] : hosts配置文件中的主机组 如serverName`
- `-u root : 指定远程执行用户为root`
- `-m command : 指定模块为command`
- `-a 'uptime' : 指定远程执行的命令`
- `-k : 指定为输入密码 如果已做无密验证 可忽略此选项`
- `-h : -h or --help 查看更多选项`

#### Ansible的Hosts文件
最简配置 ：
```shell
[serverName1]
www.ynlwyscloud.com
db-[a:f].example.com
localhost   ansible_connection=local
www.ynlwyscloud.com ansible_connection=ssh ansible_ssh_user=ynlwys
jumper ansible_ssh_port=22 ansible_ssh_host=192.168.122.11

[serverName2]
192.168.122.[1-9] http_port=80 maxRequestsPerChild=8080
192.168.122.150:22
192.168.122.45
192.168.122.11

[serverName2:vars]
server_hosts=192.168.1.1

[serverName:children]
serverName1
serverName2

```

其他方式 ：

- 可以配置ip地址 如：192.168.122.11
- 可以配置域名 如：www.ynlwyscloud.com
- 可以配置一个或者多个组 如：[serverName1]、[serverName2]
- 可以更换默认端口 如：192.168.122.150:22
- 可以添加别名根据端口和ip 如：jumper ansible_ssh_port=22 ansible_ssh_host=192.168.122.11
- 可以批量添加域名或者ip 如：db-[a:f].example.com、192.168.122.[1-9]
- 可以添加本地连接 如：localhost   ansible_connection=local
- 可以设定某域名或ip的连接方式和连接用户 如：www.ynlwyscloud.com ansible_connection=ssh ansible_ssh_user=ynlwys
- 可以设定变量给主机 如：192.168.122.[1-9] http_port=80 maxRequestsPerChild=8080
- 可以设定变量给主机组 如：[serverName2:vars] \ server_hosts=192.168.1.1
- 可以进行主机组嵌套 如：[serverName:children] \ serverName1 \ serverName2
- ~~可以分文件定义Host和Group变量 会在ansible-playbook中进行说明~~


---
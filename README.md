
# 短信发送通道系统 | 后台

## 上传格式

xlsx
每行一个手机号


### 环境

Centos7

Mysql 5.7+ 需要开启group by  (Google = TRADITIONAL)
 ~ SET sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

### 部署环境

1. Redis
yum install redis -y &&
systemctl enable redis &&
systemctl start redis

2. pythone3.6+
yum update
yum install python36 -y &&
yum install python36-devel -y &&
yum install python36-setuptools -y &&
ln -s /usr/bin/python3.6 /usr/bin/python3 &&
mkdir /usr/local/lib/python3.6/site-packages &&
easy_install-3.6 pip && ln -s /usr/local/bin/pip3 /usr/bin/pip3 &&
ln -s /usr/local/bin/pip3 /usr/bin/pip3

3. python3 插件
~ pip3 install flask xlwt pymysql DBUtils redis requests openpyxl flask-login flask-cors nexmo plivo clickatell gunicorn


### 启动

1. 打开列队
python3 queue_api.py

2. 打开发送者
python3 sender.py

3. (如果使用Axflix SMS网关发短信，可选) 本地开一个9999端口提供TCP服务，用来调用Axflix SMS Gateway短信网关接口，因为网关是长连接的，所以就写了axflix_server.py这个文件。
python3 axflix_server.py

5. 开启余额处理
python3 balance_server.py

5. 打开web
python3 web.py  <- 生产环境推荐使用gunicorn  (start.sh就是使用的gunicorn)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
PS: 找不到gunicorn命令的解决办法：
find / -name gunicorn   # 找到了 /usr/local/python3/bin/gunicorn
ln -s /usr/local/bin/gunicorn /usr/bin/gunicorn
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


### 前端 ->  front-end

解压后直接部署到nginx下即可

### DB ->  sms.sql

设计请看design.md

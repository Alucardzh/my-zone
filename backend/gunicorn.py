# -*- encoding: utf-8 -*-
'''
@File    :   gunicorn.py
@Time    :   2025/02/17 15:56:16
@Author  :   Alucard Zheng
@Version :   1.0
@Contact :   zheng.hanbin@sihanfu.cn
@Desc    :   None
'''

# here put the import lib
# 并行工作进程数
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
# 指定每个工作者的线程数
threads = 2
# 监听内网端口5000
bind = 'unix:/tmp/gunicorn.sock'
# bind = 'unix:/tmp/my-comfyui-client.sock'
# 设置守护进程,将进程交给supervisor管理
# daemon = 'true'
# 设置进程文件目录
pidfile = './pid.pid'
# 设置访问日志和错误信息日志路径
accesslog = '-'
errorlog = '-'
# 设置日志记录水平
loglevel = 'debug'

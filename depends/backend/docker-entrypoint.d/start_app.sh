#!/bin/bash

# set -e  # 遇到错误立即退出
set -x

echo "Starting application..."

rm /etc/nginx/sites-enabled/default || true
echo "激活虚拟环境..."
source /root/.venv/bin/activate


echo "Starting FastAPI application..."
cd /app


nginx
# 启动主应用
echo "Starting main application..."
exec gunicorn -c gunicorn.py app.main:app -k uvicorn.workers.UvicornWorker 

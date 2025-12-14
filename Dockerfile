FROM python:3.13-slim


# 配置 Debian 清华源
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    (echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
     echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
     echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
     echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list)

# 设置Pypi源，注释采用官方默认，一般很慢，需要自行修改Pypi的源
ARG PYPI=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

RUN apt update && apt install curl procps nginx dos2unix -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY .env /root/.env
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="/root/.local/bin:$PATH" && \
    uv venv /root/.venv
ENV PATH="/root/.local/bin:$PATH"

# 设置工作目录
WORKDIR /app

# uv安装依赖,若注释了$PYPI设置，RUN最后的$PYPI也需要注释掉
COPY backend/pyproject.toml /app/pyproject.toml
RUN uv venv --clear /root/.venv && \
    export UV_INDEX_URL=$PYPI && \
    export UV_PROJECT_ENVIRONMENT=/root/.venv && \
    export PATH="/root/.venv/bin:$PATH" && \
    . /root/.venv/bin/activate && \
    cd /app && uv lock && \
    uv sync --active

# 设置环境变量
ENV PYTHONPATH=/root/.venv/bin
ENV PYTHONUNBUFFERED=1

# 使用uv安装依赖
# RUN pip install -r requirements.txt
COPY ./depends/backend/start.sh /docker-entrypoint.sh
RUN mkdir -p /docker-entrypoint.d
COPY ./depends/backend/docker-entrypoint.d/start_app.sh /docker-entrypoint.d/start_app.sh

RUN dos2unix /docker-entrypoint.sh /docker-entrypoint.d/*.sh 2>/dev/null || true && \
    chmod +x /docker-entrypoint.sh /docker-entrypoint.d/*.sh
EXPOSE 80

# 若注释了代理设置，此行需要注释
RUN sed -i 's/^user www-data;/user root;/' /etc/nginx/nginx.conf

# 启动命令
ENTRYPOINT [ "/docker-entrypoint.sh" ]
#!/bin/bash

dos2unix /docker-entrypoint.d/*.sh 2>/dev/null || true
chmod +x /docker-entrypoint.d/*.sh
/docker-entrypoint.d/start_app.sh

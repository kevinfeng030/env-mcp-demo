#!/bin/bash

set -e

start() {
    uv --directory hello_world run python src/main.py > stdout.log 2>&1 &
    SERVER_PID=$!
    echo "Server started with PID: $SERVER_PID"
}

check() {
    local max_wait=120
    local elapsed=0
    local health_url="http://localhost:8081/health"

    echo "Waiting for server to be ready..."

    while [ $elapsed -lt $max_wait ]; do
        if curl -s -o /dev/null -w "%{http_code}" "$health_url" | grep -q "200"; then
            echo "Server is ready!"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done

    echo "Timeout: Server did not become ready within ${max_wait} seconds"
    return 1
}

start
check

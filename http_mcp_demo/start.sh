#!/bin/bash

set -e

cd "hello_world_server"

uv run python src/main.py


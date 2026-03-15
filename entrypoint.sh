#!/bin/bash
echo "Starting container"
alembic upgrade head
python init_admin.py
python main.py
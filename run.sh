#!/bin/bash
cd /home/game_server
uvicorn main:app --host 0.0.0.0 --port 8000

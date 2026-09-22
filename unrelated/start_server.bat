@echo off
title Antigravity Chrome Bridge Pro 3.0
echo ====================================================
echo Starting Antigravity Chrome Bridge & Web Studio 3.0
echo WebSocket Server: ws://localhost:9999
echo Web Studio UI:    http://localhost:9998
echo ====================================================
python "%~dp0bridge_server.py"
pause

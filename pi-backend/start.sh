#!/bin/bash
# PHANTOM CONTROLLER — Pi Backend Start Script
# Usage: ./start.sh

cd "$(dirname "$0")"

# Kill any existing server
pkill -f "uvicorn server:app" 2>/dev/null
sleep 1

# Start server in background (no venv source needed — use full path)
nohup /home/noktirnal/phantom/bin/python -m uvicorn server:app \
  --host 0.0.0.0 \
  --port 8080 \
  --ws-ping-interval 10 \
  --ws-ping-timeout 30 \
  > /home/noktirnal/phantom/server.log 2>&1 &
UVICORN_PID=$!

echo "Phantom Controller backend started on port 8080"
echo "PID: $UVICORN_PID"
echo "Log: /home/noktirnal/phantom/server.log"

# Wait a moment and verify
sleep 2
if kill -0 $UVICORN_PID 2>/dev/null; then
  echo "Server is running"
else
  echo "ERROR: Server failed to start. Log:"
  cat /home/noktirnal/phantom/server.log
fi

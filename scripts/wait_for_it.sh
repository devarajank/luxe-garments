#!/bin/sh
# Wait for a service to be ready
HOST="$1"
PORT="$2"
shift 2
echo "Waiting for $HOST:$PORT..."
while ! nc -z "$HOST" "$PORT" 2>/dev/null; do
  sleep 1
done
echo "$HOST:$PORT is ready."
exec "$@"

#!/bin/sh
set -e
for host in regional_mx regional_us film_action film_romance film_scifi soundtrack_classical soundtrack_jazz soundtrack_pop analytics admin_secure; do
  echo "Waiting for $host..."
  until pg_isready -h "$host" -p 5432 -U postgres >/dev/null 2>&1; do
    sleep 1
  done
done

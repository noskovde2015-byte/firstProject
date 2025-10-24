#!/usr/bin/env bash

set -e

echo "Start Migration..."

alembic upgrade head

echo "Migration applied"

exec "$@"
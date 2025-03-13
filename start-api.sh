#!/bin/bash

uv run --env-file .env -- fastapi dev api.py --root-path /api/platform --port 8090
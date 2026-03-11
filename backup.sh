#!/bin/sh
cd /home/fengxueda/.openclaw/workspace
git add .
git commit -m "workspace backup $(date +%Y-%m-%d)" || true
git push origin main

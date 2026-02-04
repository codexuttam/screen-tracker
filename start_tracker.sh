#!/bin/bash

cd /home/codebloodedsash/my-screen-tracker || exit 1
source venv/bin/activate
exec python tracker_phase3_sqlite.py

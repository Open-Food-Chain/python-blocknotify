#!/bin/bash
cd /opt/komodo/blocknotify-python
source .venv/bin/activate
python3 test.py $1
deactivate

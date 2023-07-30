#!/usr/bin/env bash
source env/Scripts/Activate
py scripts/build.py
sh scripts/stubgen.sh
py -m build
py scripts/upload.py $1 $2

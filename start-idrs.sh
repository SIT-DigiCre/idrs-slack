#!/bin/bash

SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR

./lockchecker.py &

#!/bin/bash

cd `dirname $0`

dockerfiledata=`cat ./Dockerfile`
if [ "`git pull`" != "Already up-to-date." ]; then
	[ "`cat ./Dockerfile`" != $dockerfiledata ] && docker build -t idrs-python:0.1 ./
fi

#!/bin/bash

cd `dirname $0`

dockerfiledata=`cat ./Dockerfile`
pipfiledata=`cat ./Pipfile`
if [ "`git pull`" != "Already up-to-date." ]; then
	if [ "`cat ./Dockerfile`" != "$dockerfiledata" ] || [ "`cat ./Pipfile`" != "$pipfiledata" ]; then
		docker build -t idrs-python:0.1 ./
	fi
fi

exit 0

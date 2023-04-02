#!/bin/bash

MCDIR=$1

tmux new-session -s MCserver -d
sleep 1
tmux send-keys -t MCserver "cd ${MCDIR}/running" Enter
sleep 1
tmux send-keys -t MCserver 'LD_LIBRARY_PATH=. ./bedrock_server' Enter

echo "server turned on"

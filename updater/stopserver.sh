#!/bin/bash

checkserver=$(tmux ls | grep 'MCserver')
if [ -z "$checkserver" ]; then
	echo "Server is already off"
	exit
fi

tmux send-keys -t MCserver Enter
tmux send-keys -t MCserver Enter

# Notice users that server will shutdown
#tmux send-keys -t MCserver 'tellraw @a {"rawtext":[{"text":"server will shutdown"}]}' Enter
#tmux send-keys -t MCserver Enter
#tmux send-keys -t MCserver Enter

tmux send-keys -t MCserver 'stop' Enter
sleep 60
tmux send-keys -t MCserver 'exit' Enter
sleep 1
echo "server successfully turned off"

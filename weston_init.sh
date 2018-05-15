#!/bin/sh

function installmod {
	MOD_NAME=$1
	MOD_LIVE=`grep "$MOD_NAME" /proc/modules | awk '{ print $5 }'`
	if [ "Live" == "$MOD_LIVE" ]; 
	then
		echo "$MOD_NAME already installed!!"
	else
		MOD_PATH="/lib/modules/*/$MOD_NAME.ko"
		insmod $MOD_PATH
	fi
}

installmod iopc_inputs

mkdir -p /tmp/wayland
chmod 0700 /tmp/wayland
export XDG_RUNTIME_DIR=/tmp/wayland

/bin/weston-launch

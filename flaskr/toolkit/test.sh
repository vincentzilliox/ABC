#!/bin/bash
echo "hi from shell script"
echo "hello from shell script"

SECONDS=0; while sleep 1; do echo "$SECONDS"; [ $SECONDS == "10" ] && break ; done;

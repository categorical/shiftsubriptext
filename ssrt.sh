#!/bin/bash
 

declare s=${BASH_SOURCE[0]}
while [ -L "$s" ];do
    s=$(readlink "$s")
done
DIR=$(cd -P `dirname "$s"` && pwd)
PYTHON2="$DIR/env/bin/python2"

PYTHON2 "$DIR/shift.py" "$@"




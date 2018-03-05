#!/bin/bash

# Usage example: sh count-files-in-subdirs.sh /nfs/HelloFresh/Databases/fact_tables 50

PATH=$1
LIMIT=$2

/usr/bin/find $PATH -type d | while read x; do
   num=$(/usr/bin/ls $x | /usr/bin/wc -l)
   # echo $LIMIT
   if (( $num>=$LIMIT )); then
    echo $x
    echo 'Too many files: '$num
   fi
done

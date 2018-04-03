#!/bin/sh

clean() {
  for file in $1/*
  do
    if [ -d $file ]
    then
      clean $file
    else
      echo $file
      temp=$(tail -300 $file)
      echo "$temp" > $file
    fi
  done
}

dir=/service/logs
clean $dir

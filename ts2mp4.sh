#!/bin/sh

for filename in $@
do
    name=$(echo "$filename" | cut -f 1 -d '.')
    ffmpeg -i $filename -c copy ${name}.mp4
done

#!/bin/bash
if [ $# -lt 3 ] 
    then
    echo "Invalid number of arguments"
    echo "Usage: ./run.sh <team_name> <algorithm_name> <version>"
    exit 1
fi
imagename=$1"/"$2":"$3
filename=$1"_"$2"_"$3".tgz"
echo $imagename 
echo $filename

echo "Building image" $imagename &&
docker build --network=host -t $imagename . && 
echo "Saving image" $imagename "to" $filename && 
docker save $imagename | gzip > $filename &&
echo "Removing image" $imagename
docker image rm $imagename
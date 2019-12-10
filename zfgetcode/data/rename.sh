#! /bin/bash
cd model
for file in `ls | grep .gif`
do
    newfile=`echo $file | sed 's/-/-a/'`
    mv $file $newfile
done

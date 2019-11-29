#!/usr/bin/env bash

echo "cleanup not well-formated directory names with maxdepth=10"
for i in {1..10}
do
    find . -depth -maxdepth $i -type d |
    while read name
    do
        name=${name#*/}
        na=$(echo $name | tr "@'&, " "_" | tr -s '_')
        if [ "$name" != "$na" ]
        then
            mv "$name" "$na"
        fi
    done
done

echo "cleanup not well-formated filenames"
find . -type f |
while read name
do
    name=${name#*/}
    na=$(echo $name | tr "'&@, " "_" | tr -s '_')
    if [ "$name" != "$na" ]
    then
        mv "$name" "$na"
    fi
done

echo "cleanup no-use files or directories"
find . -type f -name '.DS_store' -delete
find . -type f -name 'Thumbs.db' -delete
find . -type d -name '@eaDir' | xargs rm -rf
find . -type d -name 'CVS' | xargs rm -rf
find . -type d -name '.svn' | xargs rm -rf

echo "cleanup empty directories and files"
find . -type f -empty -delete
find . -type d -empty | xargs rm -rf

echo "log old file list and count"
find . -type f | sort > ./old_file_list.txt
find . -type f | sed 's/^.*\.//' | sort | uniq -c | sort -n > ./old_file_ext_statistic.txt

echo "create new directories for classification"
mkdir ../Pictures_without_exif
mkdir ../Photos
mkdir ../Videos

echo "move all picture format files"
find . -type f | grep -i "\.jpg\|\.png\|\.gif\|\.jpeg\|\.nef\|\.psd" |
while read name
do
    na="../Pictures_without_exif/"$(echo $name | sed "s/\/[^\/]*\..*$//")
    echo "$name" "$na"
    mkdir -p "$na"
    mv "$name" "$na"
done

echo "move all video format files"
find . -type f | grep -i "\.mov\|\.mp4\|\.mpg\|\.avi\|\.3pg\|\.m4v" |
while read name
do
    na="../Videos/"$(echo $name | sed "s/\/[^\/]*\..*$//")
    echo "$name" "$na"
    mkdir -p "$na"
    mv "$name" "$na"
done

echo "move all photos with exif(date and maker)"
python copy_photos.py -s ../Pictures_without_exif -d ../Photos 1>stdout.log 2>stderr.log
cat todo_list.txt |
while read old new
do
    new_dir=$(echo $new|sed "s/\/[^\/]*\..*$//")
    mkdir -p "$new_dir"
    mv "$old" "$new"
done

echo "log new  file list and count"
find ../Pictures_without_exif/ ../Photos/ ../Videos/ -type f | sort > ./new_file_list.txt
find ../Pictures_without_exif/ ../Photos/ ../Videos/ -type f | sed 's/^.*\.//' | sort | uniq -c | sort -n > ./new_file_ext_statistic.txt

echo "cleanup empty directories and files"
find . -type f -empty -delete
find . -type d -empty | xargs rm -rf

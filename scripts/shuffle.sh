#!/bin/sh
#DATASET="the-nature-conservancy-fisheries-monitoring"; #dogscats
DATASET="$1"; #dogscats
SAMPLE="$2";

dirpath="${DATASET}/train/*";

if [ "$SAMPLE" = "sample" ]; then
    for dir in ${dirpath}; do 
        dname="${dir##*/}" 
        mkdir -p ${DATASET}_smpl/valid/${dname}
        mkdir -p ${DATASET}_smpl/train/${dname} 
        gshuf -n 200 -e ${DATASET}/train/${dname}/* | xargs -I {} cp {} ${DATASET}_smpl/train/${dname}
        gshuf -n 100 -e ${DATASET}/valid/${dname}/* | xargs -I {} cp {} ${DATASET}_smpl/valid/${dname} 
    done;
else
    for dir in ${dirpath}; do 
        dname="${dir##*/}" 
        mkdir -p ${DATASET}/valid/${dname}
        gshuf -n "$2" -e ${DATASET}/train/${dname}/* | xargs -I {} mv {} ${DATASET}/valid/${dname}
    done;
fi

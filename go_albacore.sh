#!/bin/bash 
tag=$1

#for var in "$@"
#do
#   python copyunprocessedfiles.py data/"$var" basecalls/"$tag" staging/"$tag"
#done

python moveprocessedfiles.py staging/"$tag" basecalls/"$tag"/workspace processed/"$tag"_processed
time read_fast5_basecaller.py --input staging/"$tag" --worker_threads 32 -c r94_450bps_linear.cfg -s basecalls/"$tag" -r -o fast5

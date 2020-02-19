#!/bin/bash

OUTPUT="/workspace/output"

usage(){
  echo "Take the input audio and decoding into text, the output is put to /output folder. ";
  echo "If the input path is not provided or there is no audio, the system will be idle. ";
  echo "Usage: $0 -i input_dir -o output_dir [--metadata path_to_the_metadata_file]";
}

while getopts "h?m:p:y:" opt; do
    case "$opt" in
    h|\?)
        usage
        exit 0
        ;;
    i)  INPUT=$OPTARG
        ;;
    o)  OUTPUT=$OPTARG
        ;;
    metadata)  METAFILE=$OPTARG
        ;;
    esac
done

#input path must be specified
#if [ "$INPUT" == "" ] ; then
#  usage;
#  exit 1;
#fi;

# call the decoding_schedule with the input path to audio file, and output folder
# $OUTPUT $METAFILE
# python /workspace/sgdecoding/src/decoding_schedule.py $INPUT $METAFILE
python /workspace/scripts/scoring_schedule.py /workspace/input ''


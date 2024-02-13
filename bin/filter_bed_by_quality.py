#!/usr/bin/python3

"""
This script filters a BED file using the 
quality score given within the BED.

To use:

filter_bed_by_quality.py sample_id bed_path quality_score_to_filter_by

E.g.

filter_bed_by_quality.py Sample1 data/Sample1.bed 30
"""

import sys
import warnings
# We use the stdout in this script
# to be used by the Nextflow pipeline
# therefore we want to supress all
# warnings that may result in 
# Nextflow input errors.
warnings.filterwarnings("ignore")


def filter_bed(bed_path, quality_filter):
    "A generator to yield only records greater than a user-defined quality score"
    with open(bed_path, "r", encoding="utf-8") as bed_file:
        # Count the total reads in the BED
        total_read_count = 0

        for line in bed_file:
            # Count READs
            total_read_count += 1
            # extract quality score
            bam_record_q_score = int(line.split("\t")[4])

            if bam_record_q_score >= quality_filter:
                # BED record is greater than the cut-off
                yield line, total_read_count


# --- Define incoming paramters
SAMPLE_ID = sys.argv[1]
SAMPLE_BED_PATH = sys.argv[2]
QUALITY_SCORE = int(sys.argv[3])

# set output filename
OUTPUT_FILENAME = f"{SAMPLE_ID}.Q{QUALITY_SCORE}.bed"

# Count the total number of unfiltered reads
TOTAL_READ_COUNT = 0


with open(OUTPUT_FILENAME,"w", encoding="utf-8") as outputf:
    for bed_record, read_count in filter_bed(SAMPLE_BED_PATH, QUALITY_SCORE):
        outputf.write(bed_record)
        TOTAL_READ_COUNT = read_count

# Set the total read count for the sample
# bed to an envirnoment variable called
# total count. This will be picked up
# by Nextflow using env(total_count)
print(f"{TOTAL_READ_COUNT}", file=sys.stdout)

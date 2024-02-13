#!/usr/bin/python3

"""
This script accepts a sample BED containing posistions for a Double strand break (DSB)
and the number of raw count before the BED file was filtered.

Two output files are generated:
 1) A sample based summary statistics file.
 2) A regions (genomic) based summary statistics file.

"""

import sys
from collections import defaultdict

# -- Define the paramters for the script

SAMPLE_ID = sys.argv[1]
FILTERED_BED_PATH = sys.argv[2]
UNFILTERED_BED_TOTAL_READ_VAL = int(sys.argv[3]) / 1000 # divided by 1000 to improve readability

# Create a default dict to count
# the DSBs by region.
COUNT_DSB_DICT = defaultdict(int)

# -- Count the frequency for each DSB (by region)

with open(FILTERED_BED_PATH, 'r', encoding="UTF-8") as filtered_bed:
    for line in filtered_bed:
        # split BED line by tab spacing
        # extract first 3 columns i.e.
        # chromosome, start and end
        SPLIT_BED = line.split('\t')[0:3]
        
        # Use the chomosome_start_end as a
        # key. Count the number of times
        # the key occurs in the BED.
        COUNT_DSB_DICT['_'.join(SPLIT_BED)] += 1

# -------------------------- Create a summary statistics for the sample

# Count the total number of DSBs in the sample
COUNT_DSB_SUM= sum([value for (_, value) in COUNT_DSB_DICT.items()])
# Calculate the normalised count of DSBs per sample
NORMALISED_COUNT_DSB_SUM = round(COUNT_DSB_SUM / UNFILTERED_BED_TOTAL_READ_VAL, 2)
# Count the number of DSB regions
COUNT_DSB_REGIONS = len(COUNT_DSB_DICT)

# -- Write out the results
with open(f"{SAMPLE_ID}.normalised_reads.csv", 'w', encoding='UTF-8') as outf:
    # Create column names
    outf.write('#sample_id,normalised_DSB_counts,number_of_DSB_regions,total_read_counts\n')
    # Write out results
    outf.write(f"{SAMPLE_ID},{NORMALISED_COUNT_DSB_SUM},{COUNT_DSB_REGIONS},{UNFILTERED_BED_TOTAL_READ_VAL}\n")


# --------------------------- Create a summary statistics for each region

# Calculate the normalised reads for each DSB region
NORMALISED_COUNT_DSB_DICT= {key: (value / UNFILTERED_BED_TOTAL_READ_VAL) for (key, value) in COUNT_DSB_DICT.items()}


# -- Write out the results
with open(f"{SAMPLE_ID}.normalised_reads.per_region.csv", 'w', encoding='UTF-8') as outf:

    outf.write('#sample_id,position_id,normalised_count,raw_count,total_read_count_div_by_1000\n')

    if not NORMALISED_COUNT_DSB_DICT:
        # The dictionary is empty as there
        # are no BED records. Record the sample
        # ID and the total_read values.
        outf.write(f"{SAMPLE_ID}, None, 0, 0, {UNFILTERED_BED_TOTAL_READ_VAL}\n")
    
    else:
        # Dict is not empty - proceed
        for key in NORMALISED_COUNT_DSB_DICT.keys():    
            # Write out the results from the raw and normalised
            # dictionaries.
            outf.write(f"{SAMPLE_ID}, {key}, {NORMALISED_COUNT_DSB_DICT[key]}, {COUNT_DSB_DICT[key]}, {UNFILTERED_BED_TOTAL_READ_VAL}\n")

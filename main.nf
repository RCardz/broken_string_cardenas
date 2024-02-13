#!/usr/bin/env nextflow

/* 
 * Broken string coding challenge: Ryan Cardenas
*/

nextflow.enable.dsl=2
include { quality_filter; intersect_AsiSI_regions; 
        count_and_normalise; collate_count_files} from './modules/processes.nf'

workflow {

    Channel.fromPath("${params.test_bed_path}/*.bed")                           // create a channel for the sample bed files
        .map { [it.baseName.toString().replaceAll(/.breakends/, ""), it] }      // extract the sample name
        .set { ch_sample_bed }

    // Filter the BED by quality
    quality_filter(ch_sample_bed)

    // Intersect Sample BEDs with the Query AsiSI BED
    asisi_bed = file("${params.AsiSI_bed}")
    intersect_AsiSI_regions(quality_filter.out.quality_filtered_bed, asisi_bed)

    // Count and normalise
    count_and_normalise(intersect_AsiSI_regions.out.asiSI_filtered_bed)

    // Collate all the results into a single file
    normalised_count_files_per_sample = count_and_normalise.out.normalised_counts_per_sample
                                .collect()          // collects all variables from the channel
    normalised_count_files_per_region = count_and_normalise.out.normalised_counts_per_region
                                .collect()          // collects all variables from the channel
            
    collate_count_files(normalised_count_files_per_sample,
                        normalised_count_files_per_region)

}
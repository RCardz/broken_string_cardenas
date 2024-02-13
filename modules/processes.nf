#!/usr/bin/env nextflow

process quality_filter {
    // Here we filter reads that have a quality score greater
    // than the predefined value
    publishDir "${params.outdir}/quality_filtered_beds"
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(sample_bed)

    output:
    tuple val(sample_id), path("${sample_id}.Q${params.quality_score}.bed"), stdout, emit: quality_filtered_bed

    script:
    """
    # Python script will stdout the total number of regions
    # in the sample BED file. This is captured as an output 
    # by Nextflow.


    filter_bed_by_quality.py ${sample_id} ${sample_bed} ${params.quality_score}
    
    """

}

process intersect_AsiSI_regions {

    // Here we intersect with AsiSI regions
    // with our filtered sample bed fileds.

    publishDir "${params.outdir}/AsiSI_filtered_beds"
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(quality_filtered_bed), val(total_read_count)
    path(asisi_bed)

    output:
    tuple val(sample_id), path("${sample_id}.AsiSI.filtered.bed"), val(total_read_count), emit: asiSI_filtered_bed
    path("${sample_id}.intersect.AsiSI.txt")

    script:
    """

    filter_bed_by_AsiSI.py ${sample_id} ${asisi_bed} ${quality_filtered_bed} 
    
    """


}

process count_and_normalise {

    publishDir "${params.outdir}/normalised_dsb_counts"
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(asiSI_filtered_bed), val(total_read_counts)

    output:
    path("${sample_id}.normalised_reads.csv"), emit: normalised_counts_per_sample
    path("${sample_id}.normalised_reads.per_region.csv"), emit: normalised_counts_per_region

    script:
    """

    count_normalise_dsbs.py ${sample_id} ${asiSI_filtered_bed} ${total_read_counts}

    """

}

process collate_count_files {

    publishDir "${params.outdir}/collated_counts"

    input:
    path(summary_statistics_per_sample_list)
    path(summary_statistics_per_region_list)

    output:
    path("per_sample_summary_statistics.csv")
    path("per_region_summary_statistics.csv")

    script:
    """
    # Extract the column names
    grep -E '^#' ${summary_statistics_per_sample_list[0]} > per_sample_summary_statistics.csv
    grep -E '^#' ${summary_statistics_per_region_list[0]} > per_region_summary_statistics.csv

    # Loop through the CSV files and
    # deposit data into a single file.
    cat $summary_statistics_per_sample_list | grep -v -E '^#' >> per_sample_summary_statistics.csv
    cat $summary_statistics_per_region_list | grep -v -E '^#' >> per_region_summary_statistics.csv

    """
}

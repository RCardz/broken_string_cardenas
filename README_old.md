#  Broken String Biosciences Bioinformatician pre-interview coding test

The purpose of this exercise is for you to process some of the outputs of an INDUCE-seq sequencing run in order to describe and interpret the number of breaks that occur at specific sites in the genome

## Introduction

Our patented [INDUCE-seq technology](https://www.nature.com/articles/s41467-022-31702-9) reveals the precise position and frequency of DNA double strand breaks (DSBs) throughout the genome. This approach is unique as it accurately represents DNA break events in true proportions and without experimentally introduced bias. Each read represents a single DSB that has occurred in situ in the cells that have been processed. We can locate where the break has occurred by mapping the read to the human genome. The sequence of the read is not important apart for a mechanism to locate the break. Instead the 5’ end of the read is the exact position where the DSB was labelled.  

As an internal control we often use the well-characterised DIvA (DSB Inducible via AsiSI) cell line, in which treatment with 4-hydroxytamoxifen (4OHT) triggers nuclear localisation of the AsiSI enzyme. This results in DSBs occurring at the AsiSI restriction enzyme sites within the genome. However only a proportion of the approximately 1400 possible AsiSI cut sites predicted by presence of the GCGAT/CGC sequence are actually cut, primarily due to the chromatin state at each possible site.  

Fastqs files were derived from an INDUCE-seq experiment with 16 samples where a proportion of the samples are controls derived from DIvA cells without treatment, and the remainder are DIvA cells that have been treated with 4OHT. Given that INDUCE-seq determines breaks in an unbiased way, the reads representing breaks will be derived from naturally occurring endogenous breaks, in addition to those that are induced by the AsiSI enzyme active only in treated samples. The hypothesis is that treated samples can be distinguished from controls based on the number of breaks occurring at predicted AsiSI sites.  

## Starting Data
 In order to keep the size of the fastqs small and the computation tractable, the reads were down-sampled and filtered to only include those that belong to chr21.
## Starting Data
These fastq files have already been processed to 
1.	Map the reads to chromosome 21
2.	Convert the position of the reads contained in the bam files to genomic intervals stored in a bed file.
3.	Process the bed file so that the coordinates are adjusted to include **just** the break site. The outputs from this process are stored in [breaks](data/breaks/) 

In order to count the number of breaks occuring at AsiSI sites on chr21 in each sample they can be intersected with a bed file that contains the positions of AsiSI sites on chromsome 21: [chr21_AsiSI_sites.t2t.bed](data/chr21_AsiSI_sites.t2t.bed)

## Instructions
Where using Python code try where possible to use advanced features such as
1. A timing decorator for a process
2. List comprehensions
3. Lambda functions

It is not expected that all of these will be implemented, but using these even where not absolutely required will demonstrate your ability to code these features.

### Data processing pipeline
In a workflow manager of your choice write a pipeline to process each sample in parallel through steps 1 and 3 and combine the final outputs into a single file in step 4.
1. **Filter out reads that have a mapping quality of < 30**  
   Use python code to read in the sample bed file and use a generator to yield only those lines where the mapQ (5th column) >= 30. Write these to an output file which will be a filtered bed file.
2. **Intersect each sample break bed file with the AsiSI site bed file**  
   Intersect the breaks remaining after filtering from the previous steps with the AsiSI sites recorded in the chr21_AsiSI_sites.t2t.bed file 
3. **Sum and normalise the counts** 
   Takes the output from the previous step to perform the following
    1. **Sum the number of AsiSI breaks**  
      Each sample will contain zero or more breaks at each of the sites on chr21. Find the sum of the AsiSI breaks per sample.
    2. **Normalize the number of AsiSI breaks**  
      The initial break bed file for each sample will contain the total number of breaks per sample. In order to account for different amounts of starting material, divide the sum of AsiSI breaks (step 3.1) by `total breaks/1000` so that the data consists of the normalised sum AsiSI breaks for each sample. N.B /1000 used to obtain more readable numbers typically > 1.
4. **Collect normalised number of AsiSI breaks**  
   Combine all these outputs into a single file.

### Data Analysis plotting
Take the pipeline outputs and use python code to read in, plot and. interpret the data in order to determine which samples are most likely to represent the control and treated subsets.

## Questions
1.	Which of the samples are likely to be controls or treated?
2.	Are there any you are uncertain of?
3.	Can you explain the samples in the uncertain group?
4.	Of all the possible AsiSI sites described in the chr21_AsiSI_sites.t2t.bed file what is the maximum percentage observed in a single sample?

## Result submission
Please submit your answer and code to a publicly available git repository

#!/usr/bin/python3

"""
    The aim of this script is to intersect two bed files.
    The bed files are:

    1) The primary double strand break (DSB) BED file (E.g. A sample BED)
    2) The Query BED file.

    If an intersection is found between the two BED files
    the region from the primary BED file is written out.
"""

import sys
from functools import wraps
from time import time_ns
from collections import namedtuple, defaultdict

def time_my_function(func):
    "A decorator that records how long a method takes and saves it to a log file."
    @wraps(func) # this allows us to access the __name__ of the method we are timing
    def time_calculation(*args):
        "Print the time it takes for a function to finish processing"
        start_time = time_ns()                  # start time in nanosecond
        function_result = func(*args)           # run method and store result
        total_time = time_ns() - start_time     # work out total time in nanoseconds

        # Save the function's timing to a log file
        log = open(f'{args[0].sample_id}.intersect.AsiSI.txt', 'a', encoding="UTF-8")
        log.write(f"Method {func.__name__} took {total_time} nanoseconds to run.\n")
        log.close()

        return function_result

    return time_calculation


class IntersectBeds:
    """
    The aim of this script is to intersect two bed files,
    a primary and a query BED. If an intersection is found
    the region from the primary BED file is written out.
    """
    
    def __init__(self, sample_id=None, query_bed_path=None, primary_bed_path=None):


        self.sample_id = sample_id

        # Create a namedtuple template
        # this is used to store the 
        # BED records.
        self.bed_record = namedtuple('bed_record', ['chrom', 'start', 'end', 'info'])

        # Create a dictionary using the chromosomes as a Key
        # containing a Set. The Set contains every 
        # base position defined by the query bed file.
        self.create_set_from_query_bed(query_bed_path)

        # Use the query Set to intersect with primary BED file.
        # If a match is found the record from the primary BED
        # file is output.
        self.intersect_primary_bed_with_query_set(primary_bed_path)



    @time_my_function
    def create_set_from_query_bed(self, query_bed_path):
        """
        Extract the start and end regions from the
        BED file. Create integers for every base
        between the start and end for each BED
        record and add to the set.
        """

        # Create a dict to store the sets.
        # A dict is used to handle each 
        # chromosome (i.e. if there was more
        # than just chromosome 21)
        self.query_regions_set = defaultdict(set)
        
        with open(query_bed_path, 'r', encoding="utf-8") as query_bed:

            for bed_record in query_bed:

                # Extract the BED record into a named tuple.
                query_bed_record = self.extract_bed_record(bed_record)
   
                # Generate set from the BED start and end range.
                set_range = set(range(query_bed_record.start, query_bed_record.end))
                
                # Update our set with the regions.
                self.query_regions_set[query_bed_record.chrom].update(set_range)
        
    @time_my_function
    def intersect_primary_bed_with_query_set(self, primary_bed_path) :
        """
        Extract the record from the primary (DSB) BED file. Lookup the BED records' 
        start or end within the query Set. If there is a match, write the 
        BED record to a new file.
        """

        with open(primary_bed_path, 'r', encoding="UTF-8") as sample_bed:
            with open(f'{self.sample_id}.AsiSI.filtered.bed', 'w', encoding='UTF-8') as out_bed:
                
                for line in sample_bed:

                    # Extract the BED record into a named tuple
                    query_bed_record = self.extract_bed_record(line)

                    if (query_bed_record.start or query_bed_record.end) in self.query_regions_set[query_bed_record.chrom]:
                        # BED record start or end is within the query set
                        # write the matching line from the primary (DSB) BED
                        # to an output file.
                        out_bed.write(line)


    def extract_bed_record(self, bed_line):
        """
        Using the line from a BED file, extract the chromosome, start
        and end from the line and store into a tuple. All other information
        in the BED file is unpacked into the info field.
        """

        chrom, start, end, *info = bed_line.split('\t')

        if not info:
            # info field is empty
            # make it equal to None
            info = None


        return self.bed_record(chrom, int(start), int(end), info)


if __name__ == "__main__":
    
    IntersectBeds(sample_id=sys.argv[1], query_bed_path=sys.argv[2], primary_bed_path=sys.argv[3])




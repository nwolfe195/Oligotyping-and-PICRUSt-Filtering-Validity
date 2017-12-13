#!/usr/bin/python
import os
from optparse import OptionParser

def main():
    # Reading in command line arguments
    parser = OptionParser()
    # The OTU file
    parser.add_option("-f", action="store", dest="file")
    # The biom file
    parser.add_option("-b", action="store", dest="biom")
    options,args = parser.parse_args()

    # Get the percentage threshold for future string construction
    threshold = int(options.file.split("_")[0])

    # Run the biom convert command to a more malleable tab separated file
    cmd_convert_from_biom = "biom convert -i "+options.biom+" -o otu_table.txt --to-tsv"
    os.system(cmd_convert_from_biom)

    # Set various working files
    # OTU file of interest
    otu_file = options.file
    # Tab separated biom file created above
    biom_file = "otu_table.txt"
    # Temporary output file, will eventually be deleted
    out_file = "otu_out.txt"
    # Final product biom file, with threshold worked into the name
    delivered_file = "otu_table_merged_yr3_%d.biom" % (threshold)

    # Delete the output file if it already exists
    try:
        os.remove(delivered_file)
    except OSError:
        pass
    
    # Get the OTU ids from the OTU file
    otu_ids = []
    with open(otu_file) as file:
        for line in file:
            line = line.strip()
            otu_ids.append(int(line.split()[0]))
    # Read in the tab separated biom file
    data = []
    with open(biom_file) as file:
        for line in file:
            data.append(line)

    # Open the temporary output file for writing
    out = open(out_file, "w+")
    # Write the header line (data[0] is a comment)
    out.write(data[1])

    # Iterate through each entry in the biom file, keeping only the entries found in the specified OTU file
    for i in range(2,len(data)):
        otu = int(data[i].split()[0])
        if otu in otu_ids:
            out.write(data[i])

    # Remove the tab separated biom input file
    cmd_rm_biom = "rm "+biom_file
    os.system(cmd_rm_biom)
    # Convert the temporary output file to a json based biom file
    cmd_convert_to_biom = "biom convert -i "+out_file+" -o "+delivered_file+"  --table-type=\"OTU table\" --to-json"
    os.system(cmd_convert_to_biom)
    # Remove the tempoary tab separated biom output file
    cmd_rm_out = "rm "+out_file
    #os.system(cmd_rm_out)

if __name__ == "__main__":
    main()

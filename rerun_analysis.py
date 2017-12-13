#!/usr/bin/python

def main():
	# Files to be compared
	# If this script gets used again, could be worth switching these to command line arguments
	# Would mean a lot of minor variable renaming
	file99 = "99_otu_taxonomy.txt"
	file97 = "97_otu_taxonomy.txt"
	
	# Getting sets of the OTU ids
	otu_99_set = set(getIDS(file99))
	otu_97_set = set(getIDS(file97)

	# Use set functions to find the intersect of the two sets
	otu_intersect = (otu_99_set & otu_97_set)
	print "Of the %d found in 99, and the %d found in 97, %d OTUIds were found in both" % (len(otu_99_set), len(otu_97_set), len(otu_intersect))

	# Use set functions to find the difference of the two sts
	otu_97_not_99 = (otu_97_set - otu_99_set)
	print "%d OTUIds from 97 were not found in 99" % (len(otu_97_not_99))

	# Find the number of different taxonomical assignments for the interesect of the two sets
	tax_diffs = getTaxDiff(otu_intersect, file99, file97)
	print "%d differences in taxonomic assignments were found" % (tax_diffs)

def getTaxDiff(intersect, filea, fileb):
	diffCount = 0
	# Get dicitonaries
	dicta = makeDictionary(filea)
	dictb = makeDictionary(fileb)
	
	# Iterate through intersect
	for otu in intersect:
		if otu in dicta and otu in dictb:
			# If they aren't the same, increment
			if dicta[otu] != dictb[otu]:
				diffCount += 1
				#print "otu %d has a discrepency\n%s\n%s" % (otu, dicta[otu], dictb[otu])
	return diffCount

def makeDictionary(data_file):
	dictionary = {}
	# Iterate through each entry in the otu file
	with open(data_file) as file:
		for line in file:
			# Remove extraneous white space
			otu = line.strip().split()
			# Set key value pairs, key is otu (index 0), value is everything else joined together
			dictionary[int(otu[0])] = "".join(otu[1:8])
	return dictionary

def getIDS(input_file):
	ids = []
	# Iterate through each entry in the otu file
	with open(input_file) as file:
		for line in file:
			# Remove extraneous white space
			line = line.strip()
			# Add the id only, converting to an int for speed
			ids.append(int(line.split()[0]))
	return ids



if __name__ == "__main__":
	main()

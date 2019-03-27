from time import sleep

def write_processed_file(inputfilelist, outputfile):
    outfile = open(outputfile, "w")
    for inputfile in inputfilelist:
        infile = open(inputfile, "r")
        for line in infile:
            outfile.write(line.strip()+"\tprocessed\n")
        infile.close()
    outfile.close()

def print_tester(teststring, outputfile):
	outfile = open(outputfile, "w")
	outfile.write(teststring+"\n")
	outfile.close()

def test_tsubmit(T):
	sleep(T)

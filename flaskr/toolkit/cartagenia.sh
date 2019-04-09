function usage
{
	cat <<-__EOF__
		Usage:
			sh cartagenia.sh -f femme.txt -m homme.txt -r reclustering.txt -o outputfile.txt [-h]

		Description:
			CANOES is an algorithm for the detection of rare copy number variants from exome sequencing data.

		Options:
			-f, --femme			Input file femme
			-m, --homme			Input file homme
			-r, --reclustering	Input file reclustering
			-o, --output		Output file merged
			-h, --help			Print this message and exit

		__EOF__
}
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

####################################################################################################################################
# Getting parameters from the input
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ":" tells that the option has a required argument, "::" tells that the option has an optional argument, no ":" tells no argument

ARGS=$(getopt -o "f:m:r:o:h" --long "femme:,homme:,reclustering:,output:,help" -- "$@" 2> /dev/null)

[ $? -ne 0 ] && \
	echo "Error in the argument list." "Use -h or --help to display the help." >&2 && \
	exit 1
eval set -- "$ARGS"
while true  
do
	case "$1" in
		-f|--femme)
			FEMME="$2"
			shift 2 
			;;
		-m|--homme)
			HOMME="$2"
			shift 2 
			;;			
		-r|--reclustering)
			RECLUSTERING="$2"
			shift 2 
			;;
		-o|--output)
			OUTPUT="$2"
			shift 2 
			;;
		-h|--help)
			usage
			exit 0
			;;
		--) shift
			break 
			;;
		*)  echo "Option $1 is not recognized. " "Use -h or --help to display the help." && \
			exit 1
			;;
	esac
done
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


cat $FEMME $HOMME $RECLUSTERING > $OUTPUT


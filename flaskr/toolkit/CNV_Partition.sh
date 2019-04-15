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
			OUTPUTFILE="$2"
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


#!/bin/bash

# /drives/l/Archives/CYTOGENETIQUE/SNP_Illumina/programmes/script.sh

### variables
OUTPUT=$(dirname $OUTPUTFILE)

#### script fonctionne si il y a les 3 fichiers
if [ -f $FEMME ] && [ -f $HOMME ] && [ -f $RECLUSTERING ]; 
then {

###change les espaces en _ et utilise comme séparateur les \t
cat $FEMME | sed '1d' | sed 's/ /_/g' > $OUTPUT/Femmes.txt
cat $HOMME | sed '1d' | sed 's/ /_/g' > $OUTPUT/Hommes.txt
cat $RECLUSTERING | sed '1d' | sed 's/ /_/g' > $OUTPUT/reclustering.txt

##### femmes
while read colum_1 colum_2 colum_3 colum_4 colum_5 colum_6 colum_7 colum_8 colum_9
do

  if [ $colum_8 != "2" ];
	 then {
     if [ $colum_3 == "XY" ];
      then {
        colum_3="X"
	    }
     fi;
     if [ $colum_3 == "X" ];
     then {
		echo -e "$colum_1\t$colum_2\t$colum_3\t$colum_4\t$colum_5\t$colum_6\t\t$colum_7\t$colum_8\t$colum_9" >>  $OUTPUT/reclustering.txt
     }
     fi;
    }
  fi;  
done < $OUTPUT/Femmes.txt


###### hommes
while read colum_1 colum_2 colum_3 colum_4 colum_5 colum_6 colum_7 colum_8 colum_9
do

  if [ $colum_8 != "2" ];
	 then {
     if [ $colum_3 == "XY" ];
      then {
        colum_3="X"
	    }
     fi;
     if [ $colum_3 == "X" ] || [ $colum_3 == "Y" ] ;
     then {
		echo -e "$colum_1\t$colum_2\t$colum_3\t$colum_4\t$colum_5\t$colum_6\t\t$colum_7\t$colum_8\t$colum_9" >> $OUTPUT/reclustering.txt
     }
     fi;
    }
  fi;  
done < $OUTPUT/Hommes.txt



###### supprimer dans la premièer colonne les []
while read colum_1 colum_2 colum_3 colum_4 colum_5 colum_6 colum_7 colum_8 colum_9
do
	var1=$(echo $colum_1 | cut -f1 -d_)
	echo -e "$var1\t$colum_2\t$colum_3\t$colum_4\t$colum_5\t$colum_6\t\t$colum_7\t$colum_8\t$colum_9" >> $OUTPUT/reclustering_correct.txt
done < $OUTPUT/reclustering.txt

### changer les _ en espaces
cat $OUTPUT/reclustering_correct.txt | sed 's/_/ /g' > $OUTPUT/reclustering_correct2.txt 

## ajout de l'entete
sed -i "1i\SampleID_BookmarkType_Chr_Start_End_Size_Author_CreatedDate_Value_Comment" $OUTPUT/reclustering_correct2.txt 
sed 's/_/\t/g' $OUTPUT/reclustering_correct2.txt  > $OUTPUTFILE


rm -rf $OUTPUT/Femmes.txt
rm -rf $OUTPUT/Hommes.txt
rm -rf $OUTPUT/reclustering.txt
rm -rf $OUTPUT/reclustering_correct.txt
rm -rf $OUTPUT/reclustering_correct2.txt 

echo -e "Merge effectué sans erreur\n" ; 

}
else {
	echo -e "Abscence de l'un des fichiers d'entrés\nVérifiez si les fichiers 'Infinium_CYTO_DATE_reclustering_Femmes.txt' , 'Infinium_CYTO_DATE_reclustering_Hommes.txt' et 'Infinium_CYTO_DATE_reclustering.txt' sont bien présents" >> $OUTPUTFILE
}
fi ;




#!/usr/bin/python
# -*- coding: utf-8 -*-

#MINIMUM USAGE:
#python tsvToCanDiD.py -a "DATA/P4552.final.txt,DATA/M7460P.final.txt" -b "P4552,M7460P" -c "configuration.json"

import os,sys,optparse,json

def splitSpace(someList):
	newlist=[]
	for item in someList:
		while item.startswith(" ") or item.startswith("\t"):
			item=item[1:]
		while item.endswith(" ") or item.endswith("\t"):
			item=item[:1]
		newlist.append(item)
	return newlist

def TsvToDico(tsvfiles,filenames,indexkey,renameinfo=False):
	oldHeader={}
	dict_final={}
	if len(tsvfiles) == len(filenames):
		for i in range(0,len(tsvfiles)):
			tsvfile=tsvfiles[i]
			filename=filenames[i]
			dict_entry={}
			with open(tsvfile, 'r') as infile:
				header_index=True
				for nlines in infile:
					ncolonne = nlines.split('\n')
					colonne = ncolonne[0].split('\t')
					if len(colonne)>1:
						if header_index:
							if indexkey=="ALL":
								list_indexKey=colonne
							else:
								list_indexKey=indexkey.split(',')
							list_key=[]
							for keyValue in list_indexKey:
								list_key.append(colonne.index(keyValue))
								header=colonne
								if renameinfo:
									header=header[:-1]+[renameinfo]
								for item in header:
									oldHeader[item]=item
								header_index=False
						else:
							if len(header) == len(colonne):
								list_keyValue=[]
								for i in list_key:
									list_keyValue.append(colonne[i])
								keyName='_'.join(list_keyValue)
								if keyName not in dict_entry:
									dict_entry[keyName]={}
								else:
									print >> sys.stderr,"...\nERROR - keyName is not uniq: "+keyName+" (EXIT)"
									sys.exit()
								for i in range(0,len(colonne)):
									colonneNAME=header[i]
									colonneVALUE=colonne[i]
									if colonneNAME.startswith("CALLING_QUALITY"):
										if colonneVALUE==".":
											colonneVALUE=""
									if colonneNAME not in dict_entry[keyName]:
										dict_entry[keyName][colonneNAME]=colonneVALUE
									else:
										print >> sys.stderr,"WARNING - field is not uniq: "+colonneNAME
							else:
								print >> sys.stderr,"ERROR - header size doesn't match with fiels size (EXIT)"
								sys.exit()
			dict_final[filename]=dict_entry
	else:
		print >> sys.stderr,"ERROR - file list and sample list are not equal in length (EXIT)"
		sys.exit()
	return dict_final,oldHeader

def formatNumber(dict_entry,oldHeader):
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			for colonneName in dict_entry[fileName][keyName]:
				val=dict_entry[fileName][keyName][colonneName]
				if colonneName[0].isdigit():
					new_col="n"+colonneName
					if colonneName in oldHeader:
						origine=oldHeader[colonneName]
						del oldHeader[colonneName]
						colonneName=origine
					oldHeader[new_col]=colonneName
					del dict_entry[fileName][keyName][colonneName]
					dict_entry[fileName][keyName][new_col]=val
	return dict_entry,oldHeader

def replaceValues(dict_entry,dict_replace,oldHeader):
	dict_out={}
	for fileName in dict_entry:
		dict_out[fileName]={}
		for keyName in dict_entry[fileName]:
			dict_out[fileName][keyName]={}
			for colonneName in dict_entry[fileName][keyName]:
				newColtmp=False
				new_col=colonneName
				val=dict_entry[fileName][keyName][colonneName]
				for lettre in dict_replace:
					if colonneName.find(lettre) != -1:
						if newColtmp:
							new_col=newColtmp.replace(lettre, dict_replace[lettre])
						else:
							new_col=colonneName.replace(lettre, dict_replace[lettre])
						newColtmp=new_col
				dict_out[fileName][keyName][new_col]=val
				if colonneName in oldHeader:
					del oldHeader[colonneName]
				if new_col not in oldHeader:
					oldHeader[new_col]=colonneName
	return dict_out,oldHeader

def getHGNCDB(dict_entry,DB_HGNC_file,genekey,HGNCidDefaut):
	DB_HGNC={}
	with open(DB_HGNC_file, 'r') as infile:
		for nlines in infile:
			ncolonne = nlines.split('\n')
			colonne = ncolonne[0].split('\t')
			HGNC_id = colonne[0]
			GENE_NAME = colonne[1]
			if GENE_NAME not in DB_HGNC:
				DB_HGNC[GENE_NAME]=HGNC_id
			else:
				print >> sys.stderr,"WARNING - HGNC id FILE - key is not uniq: "+GENE_NAME
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			if genekey in dict_entry[fileName][keyName]:
				colonneVALUE=dict_entry[fileName][keyName][genekey]
				if colonneVALUE in DB_HGNC:
					HGNC_id=DB_HGNC[colonneVALUE]
					dict_entry[fileName][keyName]["hgnc_id"]=HGNC_id
				else:
					dict_entry[fileName][keyName]["hgnc_id"]=HGNCidDefaut
			else:
				print >> sys.stderr,"WARNING - field "+genekey+" doesn't exist in input file"
	return dict_entry

def trimming(dict_entry,cutbylength):
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			for colonneName in dict_entry[fileName][keyName]:
				dict_entry[fileName][keyName][colonneName]=dict_entry[fileName][keyName][colonneName][:cutbylength]
	return dict_entry

def splitCHROM(dict_entry,chromkey):
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			if chromkey in dict_entry[fileName][keyName]:
				colonneVALUE=dict_entry[fileName][keyName][chromkey]
				if colonneVALUE.startswith("chr"):
					dict_entry[fileName][keyName][chromkey]=colonneVALUE[3:]
			else:
				print >> sys.stderr,"WARNING - field "+chromkey+" doesn't exist in input file"
	return dict_entry

def arrangeCNOMEN(dict_entry):
        for fileName in dict_entry:
                for keyName in dict_entry[fileName]:
                        if "CNOMEN" in dict_entry[fileName][keyName]:
                                if dict_entry[fileName][keyName]["CNOMEN"] == "":
                                        dict_entry[fileName][keyName]["CNOMEN"]="g."+dict_entry[fileName][keyName]["POS"]+dict_entry[fileName][keyName]["REF"]+">"+dict_entry[fileName][keyName]["ALT"]
                        else:
                                print >> sys.stderr,"WARNING - field CNOMEN doesn't exist in input file"
        		if "TNOMEN" in dict_entry[fileName][keyName]:
                                if dict_entry[fileName][keyName]["TNOMEN"] == "":
                                        dict_entry[fileName][keyName]["TNOMEN"]=dict_entry[fileName][keyName]["CHROM"]
			else:
                                print >> sys.stderr,"WARNING - field TNOMEN doesn't exist in input file"
	return dict_entry


def invertDict(alias):
	newAlias={}
	for item in alias:
		if alias[item] not in newAlias:
			newAlias[alias[item]]=[item]
		else:
			newAlias[alias[item]].append(item)
	return newAlias


def changeToAlias(dict_entry,alias,oldHeader):
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			colTodel=[]
			for colonneName in alias:
				isDone=False
				newCol=colonneName
				oldColList=splitSpace(alias[colonneName].split(','))
				for oldCol in oldColList:
					if not isDone:
						if oldCol in dict_entry[fileName][keyName]:
							ColonneVALUE=dict_entry[fileName][keyName][oldCol]
							dict_entry[fileName][keyName][newCol]=ColonneVALUE
							oldHeader[newCol]=oldCol
							if oldCol in oldHeader:
								del oldHeader[oldCol]
							if oldCol not in colTodel:
								colTodel.append(oldCol)
							isDone=True
						else:
							ColonneVALUE=""
							dict_entry[fileName][keyName][newCol]=ColonneVALUE
							oldHeader[newCol]=oldCol
							isDone=True
				if not isDone:
					print >> sys.stderr,"WARNING - No alias found for "+colonneName
					print >> sys.stderr,"ERROR - field "+",".join(oldColList)+" doesn't exist in input file (EXIT)"
					sys.exit()
			for col in colTodel:
				del dict_entry[fileName][keyName][col]
	return dict_entry,oldHeader


def concat_fields(dict_entry,O_concat,oldHeader):
	for colToInsert in O_concat:
		if colToInsert not in oldHeader:
			oldHeader[colToInsert]=colToInsert
		else:
			print >> sys.stderr,"ERROR - field "+colToInsert+" already exit in files, can't be used as concated field name (EXIT)"
			sys.exit()
		for fileName in dict_entry:
			for keyName in dict_entry[fileName]:
				field_values=[]
				for colonneNAME in O_concat[colToInsert]:
					if colonneNAME in dict_entry[fileName][keyName]:
						field_values.append(dict_entry[fileName][keyName][colonneNAME])
					else:
						print >> sys.stderr,"ERROR - field "+colonneNAME+" doesn't exist in input file, can't be used to concat fields (EXIT)"
						sys.exit()
				dict_entry[fileName][keyName][colToInsert]=":".join(field_values)
	return dict_entry,oldHeader

def getSplice(dict_entry,oldHeader):
	if "SPLICE" not in oldHeader:
		oldHeader["SPLICE"]="SPLICE"
	else:
		print >> sys.stderr,"ERROR - field \"SPLICE\" already exit in files, you can't use option --splice (EXIT)"
		sys.exit()
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			if "cNomen" not in dict_entry[fileName][keyName]:
				print >> sys.stderr,"ERROR - field \"cNomen\" doesn't exit in files, you can't use option --splice (EXIT)"
				sys.exit()
			CNOMEN=dict_entry[fileName][keyName]["cNomen"]
			if "+" in CNOMEN or "-" in CNOMEN:
				site=CNOMEN.split("+")[-1].split("-")[-1]
				if site.startswith(("1","2","3")) and site[1].isalpha():
					dict_entry[fileName][keyName]["SPLICE"]="YES"
				else:
					dict_entry[fileName][keyName]["SPLICE"]="NO"
			else:
				dict_entry[fileName][keyName]["SPLICE"]="NO"
	return dict_entry,oldHeader


def checkMandatory(dict_entry,mandatory,oldHeader):
	for fileName in dict_entry:
		for keyName in dict_entry[fileName]:
			for colonneName in mandatory:
				if colonneName in dict_entry[fileName][keyName]:
					colonneVALUE=dict_entry[fileName][keyName][colonneName]
					if colonneVALUE == "":
						dict_entry[fileName][keyName][colonneName]=mandatory[colonneName]
				else:
					dict_entry[fileName][keyName][colonneName]=mandatory[colonneName]
					oldHeader[colonneName]=colonneName
	return dict_entry,oldHeader

def printdict(dict_entry,cle):
	for i in dict_entry:
		for j in dict_entry[i]:
			colonneVALUE=dict_entry[i][j][cle]
			print >> sys.stderr,cle+":\t"+colonneVALUE

def getOption(mandatory,option):
	dict_option={}
	for table in mandatory:
		for item in mandatory[table]:
			if option in mandatory[table][item]:
				if item not in dict_option:
					dict_option[item]=mandatory[table][item][option]
				else:
					print >> sys.stderr,"WARNING: field "+item+" is not uniq in config file"
	return dict_option

def Uniformise(dict_entry):
	Big_HEADER={}
	for filenames in dict_entry:
		i=0
		for keyName in dict_entry[filenames]:
			while i<1:
				i+=1
				for colonneName in dict_entry[filenames][keyName]:
					if colonneName not in Big_HEADER:
						Big_HEADER[colonneName]=1
					else:
						Big_HEADER[colonneName]+=1
	for filenames in dict_entry:
		for keyName in dict_entry[filenames]:
			for colonneName in Big_HEADER:
				if colonneName not in dict_entry[filenames][keyName]:
					dict_entry[filenames][keyName][colonneName]=""
	return dict_entry,Big_HEADER

def catchRegExp(oldHeader,RegExpList):
	dict_RegExp={}
	for RegExp in RegExpList:
		if RegExp.startswith("*") and RegExp.endswith("*"):
			for newColonneNAME in oldHeader:
				colonneNAME=oldHeader[newColonneNAME]
				if colonneNAME.find(RegExp[1:][:-1]) != -1:
					dict_RegExp[newColonneNAME]=None
		elif RegExp.startswith("*"):
			for newColonneNAME in oldHeader:
				colonneNAME=oldHeader[newColonneNAME]
				if colonneNAME.endswith(RegExp[1:]):
					dict_RegExp[newColonneNAME]=None
		elif RegExp.endswith("*"):
			for newColonneNAME in oldHeader:
				colonneNAME=oldHeader[newColonneNAME]
				if colonneNAME.startswith(RegExp[:-1]):
					dict_RegExp[newColonneNAME]=None
		else:
			for newColonneNAME in oldHeader:
				colonneNAME=oldHeader[newColonneNAME]
				if RegExp == colonneNAME:
					dict_RegExp[newColonneNAME]=None
	return dict_RegExp

def priorizeList(dict_entry,Big_HEADER,priorize):
	list_HEADER=[]
	list_entry={}
	for item in priorize:
		if item in Big_HEADER:
			list_HEADER.append(item)
			del Big_HEADER[item]
		else:
			print >> sys.stderr,"field "+item+" doesn't exist in input file"
	for item in Big_HEADER:
		if item not in list_HEADER:
			list_HEADER.append(item)
	for filenames in dict_entry:
		list_file=["\t".join(list_HEADER)]
		for keyName in dict_entry[filenames]:
			list_line=[]
			for colonneName in list_HEADER:
				colonneVALUE=dict_entry[filenames][keyName][colonneName]
				list_line.append(colonneVALUE)
			list_file.append("\t".join(list_line))
		list_entry[filenames]=list_file
	return list_entry


def getOutliers(dicoHeader):
	maxValue=max(dicoHeader.values())
	for colonneNAME in dicoHeader:
		val=dicoHeader[colonneNAME]
		if val!=maxValue:
			print >> sys.stderr,colonneNAME+"\tfind in "+str(val)+"/"+str(maxValue)+" vcf files"

def writeList(list_entry,output,fileExtension=False):
	if not fileExtension:
		fileExtension=".tsv"
	for sample in list_entry:
		outputfile=output+"/"+sample+fileExtension
		with open(outputfile, 'w') as outfile:
			for lines in list_entry[sample]:
				outfile.write(lines+"\n")
		os.chmod(outputfile,0775)

def printList(list_entry):
	no_header=True
	for sample in list_entry:
		if no_header:
			for lines in list_entry[sample]:
				if no_header:
					print "SAMPLE\t"+lines
					no_header=False
				else:
					print sample+"\t"+lines
		else:
			for lines in list_entry[sample][1:]:
				print sample+"\t"+lines

def extractDict(str_entry):
	dict_entry={}
	lst_entry=splitSpace(str_entry.split(','))
	for item in lst_entry:
		splititem=splitSpace(item.split(':'))
		if len(splititem) == 2:
			dict_entry[splititem[0]]=splititem[1]
		else:
			print >> sys.stderr,"WARNING - invalid entry : "+str_entry
	return dict_entry

def removeOfficialFields(list_entry,data):
	official=[]
	for tablename in data:
		if tablename != "Other":
			for colonneNAME in data[tablename]:
				if colonneNAME not in official:
					official.append(colonneNAME)
	for item in official:
		if item in list_entry:
			list_entry.remove(item)
	return list_entry

def getMapping(data,annotation,SampleVariant,Variant,outputMapping):
	if "name" not in annotation:
		annotation["name"]="Annotation_sofware"
	if "version" not in annotation:
		annotation["version"]="-"		
	mandatory=data["field"]
	assembly=data["assembly"]
	program=annotation["name"]

	mandatory["AnnotationVariant_T"]={}
	mandatory["ValidationSampleVariantResult_T"]={}
	for item in Variant:
		mandatory["AnnotationVariant_T"][item]=None
	for item in SampleVariant:
		mandatory["ValidationSampleVariantResult_T"][item]=None

	with open(outputMapping, 'w') as outfile:
		outfile.write("<section>\n")
		outfile.write("\t<program name=\""+program+"\">\n")
		outfile.write("\t\t<header name=\"header\">1</header>\n")
		outfile.write("\t\t<assembly name=\"assembly\">assembly</assembly>\n")
		for field in assembly:
			name=assembly[field]["name"]
			value=assembly[field]["value"]
			outfile.write("\t\t<"+field+" name=\""+name+"\">"+value+"</"+field+">\n")
		outfile.write("\t\t<genome_assembly>assembly</genome_assembly>\n")
		for table in mandatory:
			if table != "Other":
				outfile.write("\t\t<table name=\""+table+"\">\n")
				for item in mandatory[table]:
					outfile.write("\t\t\t<field>"+item+"</field>\n")
				outfile.write("\t\t</table>\n")
		outfile.write("\t</program>\n")
		outfile.write("</section>\n")
	os.chmod(outputMapping,0775)


def getConfig(annotation,calling,outputConfig,serie,setCapture,platform,output,outputMapping,protocol,fileExtension,base):
	if "name" not in annotation:
		annotation["name"]="Annotation_sofware"
	if "name" not in calling:
		calling["name"]="Calling_sofware"
	if "version" not in annotation:
		annotation["version"]="-"		
	if "version" not in calling:
		calling["version"]="-"

	with open(outputConfig, 'w') as outfile:
		outfile.write("<BAPT>\n")
		outfile.write("\t<params name=\"General\">\n")
		outfile.write("\t\t<analysisDirectory>"+output+"</analysisDirectory>\n")
		outfile.write("\t\t<setCapture>"+setCapture+"</setCapture>\n")
		outfile.write("\t\t<serie>"+serie+"</serie>\n")
		outfile.write("\t\t<newSetCapture/>\n")
		outfile.write("\t</params>\n")
		outfile.write("\t<tool name=\"NGSDataToCanDiD\">\n")
		outfile.write("\t\t<params>\n")
		outfile.write("\t\t\t<platform>"+platform+"</platform>\n")
		outfile.write("\t\t\t<protocol>"+protocol+"</protocol>\n")
		outfile.write("\t\t\t<annotation-software>"+annotation["name"]+"</annotation-software>\n")
		outfile.write("\t\t\t<caller-software>"+calling["name"]+"</caller-software>\n")
		outfile.write("\t\t\t<caller.version>"+calling["version"]+"</caller.version>\n")
		outfile.write("\t\t\t<annotation-software.version>"+annotation["version"]+"</annotation-software.version>\n")
		outfile.write("\t\t\t<mapping-file>"+outputMapping+"</mapping-file>\n")
		outfile.write("\t\t\t<CanDiD>"+base+"</CanDiD>\n")
		outfile.write("\t\t\t<extFile>"+fileExtension+"</extFile>\n")
		outfile.write("\t\t</params>\n")
		outfile.write("\t\t<inout>\n")
		outfile.write("\t\t\t<I>"+output+"</I>\n")
		outfile.write("\t\t</inout>\n")
		outfile.write("\t</tool>\n")
		outfile.write("</BAPT>\n")
	os.chmod(outputConfig,0775)


def main():

	#DEFAULT
	O_indexkey=False
	O_renameinfo=False
	O_alias=False
	O_splitchr=False
	O_defaut=False
	O_trimming=False
	O_concat=False
	O_toString=False
	O_reformat=False
	O_SampleVariant=False
	O_Variant=False
	O_priorize=False
	O_splice=False
	O_annotation={}
	O_calling={}

	#OPTIONS
	#---------------------------------------------------------------------------------------------------
	
	usage = "\npython %prog -a <SERIE_A,SERIE_B> -b <SAMPLE_A,SAMPLE_B> -c configfile.json\t[-options]"

	#options principales
	parser = optparse.OptionParser(usage)
	parser.add_option("-a", "--files",type="string",dest="filelist",help="list of tsv files - header correspond to first line")
	parser.add_option("-b", "--samples",type="string",dest="samplelist",help="list of sample names corresponding to the file list")
	parser.add_option("-c", "--config",type="string",dest="configfile",help="json format congfile")
	parser.add_option("-d", "--output",type="string",dest="output",help="Output Folder")
	
	#options secondaires
	group1 = optparse.OptionGroup(parser, "Parameters")
	group1.add_option("-e", "--serie",type="string",dest="serie",default="serie",help="serie/run name [default: %default]")
	group1.add_option("-f", "--setCapture",type="string",dest="setCapture",default="setCapture",help="setCapture/design/manifest name [default: %default]")
	group1.add_option("-g", "--platform",type="string",dest="platform",help="platform/application name")
	group1.add_option("-i", "--protocol",type="string",dest="protocol",default="protocol",help="protocol name [default: %default]")
	group1.add_option("-j", "--database",type="string",dest="database",default="candid",help="database name [default: %default]")

	#options tertiaires
	group2 = optparse.OptionGroup(parser, "Configuration - priority over configfile")
	group2.add_option("--splitchr",type="int",dest="splitchr",help="split <chr> before chromosome number - 0/1")
	group2.add_option("--tostring",type="int",dest="tostring",help="add n before fields who start with a number - 0/1")
	group2.add_option("--trimming",type="int",dest="trimming",help="cut each field to the appropriate size")
	group2.add_option("--index",type="string",dest="index",help="uniq index in tsv file [example: --index=\"CHROM,POS,REF,ALT\"]")
	group2.add_option("--renameinfo",type="string",dest="renameinfo",help="rename last line of a tsv file in whatever you want")
	group2.add_option("--progannot",type="string",dest="progannot",help="annotation program [example: --progannot=\"STARK_annotation:0.9.15\"]")
	group2.add_option("--progcall",type="string",dest="progcall",help="calling program [example: --progcall=\"STARK_calling:0.9.15\"]")
	group2.add_option("--outputconfig",type="string",dest="outputconfig",help="config file name")
	group2.add_option("--outputmapping",type="string",dest="outputmapping",help="mapping file name")

	#options autre
	group3 = optparse.OptionGroup(parser, "Other")
	group3.add_option("-u", "--hgncid",type="string",dest="hgncid",help="hgnc id file")
	group3.add_option("-v", "--verbose",action="store_true",dest="verbose",default=False)
	group3.add_option("-w", "--stdout",action="store_true",dest="stdout",default=False)

	parser.add_option_group(group1)
	parser.add_option_group(group2)
	parser.add_option_group(group3)
	(options,args) = parser.parse_args()




	#OPTION GESTION
	#---------------------------------------------------------------------------------------------------
	
	#OPTION FILELIST
	if options.filelist:
		tsvfiles=splitSpace(options.filelist.split(','))
		for filename in tsvfiles:
			if not os.path.exists(filename):
				print >> sys.stderr,"ERROR - No such file (samplefile): "+filename+" (EXIT)"
				sys.exit()
	else:
		print >> sys.stderr,"ERROR - No files detected (EXIT)"
		print >> sys.stderr,"ERROR - Use -f FILELIST or --files=FILELIST to use a tsv file list"
		sys.exit()


	#OPTION SAMPLELIST
	if options.samplelist:
		filenames=splitSpace(options.samplelist.split(','))
	else:
		filenames=[]
		for item in tsvfiles:
			filename=os.path.basename(item)
			filenames.append(filename)


	#OPTION CONFIGFILE
	if options.configfile:
		if not os.path.exists(options.configfile):
			print >> sys.stderr,"ERROR - No such file (configfile): "+options.configfile+" (EXIT)"
			sys.exit()
		else:
			configFile=options.configfile
			with open(configFile) as json_data_file:
				data = json.load(json_data_file)
	else:
		configFile=None
		print >> sys.stderr,"WARNING - You should use a configfile"
		data={}


	#OPTION OUTPUT
	if not options.stdout:
		if not options.output:
			O_output="RES"
		else:
			O_output=options.output
		if not os.path.exists(O_output):
			os.makedirs(O_output)
		os.chmod(O_output,0775)
		O_outputMapping=O_output+"/MappingFile.xml"
		O_outputConfig=O_output+"/ConfigFile.xml"


	#OPTION OTHER
	if options.hgncid:
		if not os.path.exists(options.hgncid):
			print >> sys.stderr,"WARNING - No such file: "+options.hgncid
			print >> sys.stderr,"WARNING - Use -u HGNC_id_file or --hgncid=HGNC_id_file"
			O_hgncdbfile=False

		else:
			O_hgncdbfile=options.hgncid
	else:
		O_hgncdbfile=False


	#OPTIONS PARAMETERS
	C_serie=options.serie
	C_setCapture=options.setCapture
	C_protocol=options.protocol



	#CONFIGFILE
	#---------------------------------------------------------------------------------------------------
	if "platform" in data:
		C_platform=data["platform"]
	else:
		C_platform="platform"

	if "program" in data:
		if "annotation" in data["program"]:
			O_annotation=data["program"]["annotation"]
		if "calling" in data["program"]:
			O_calling=data["program"]["calling"]
	if "indexkey" in data:
		O_indexkey=data["indexkey"]
	if "baseCandid" in data:
		O_base=data["baseCandid"]

	if "field" in data:
		O_mandatory=data["field"]
		O_config=data["field"]
		O_alias=getOption(O_mandatory,"alias")
		O_defaut=getOption(O_mandatory,"defaut")

	if "Option" in data:
		if "priorize" in data["Option"]:
			O_priorize=data["Option"]["priorize"]
		if "SampleVariant" in data["Option"]:
			O_SampleVariant=data["Option"]["SampleVariant"]
		if "Variant" in data["Option"]:
			O_Variant=data["Option"]["Variant"]
		if "fileExtension" in data["Option"]:
			O_fileExtension=data["Option"]["fileExtension"]			
		if "reformat" in data["Option"]:
			O_reformat=data["Option"]["reformat"]
		if "trimming" in data["Option"]:
			O_trimming=data["Option"]["trimming"]
		if "toString" in data["Option"]:
			O_toString=data["Option"]["toString"]
		if "splitchr" in data["Option"]:
			O_splitchr=data["Option"]["splitchr"]
		if "renameinfo" in data["Option"]:
			O_renameinfo=data["Option"]["renameinfo"]
		if "outputConfig" in data["Option"]:
			O_outputConfig=data["Option"]["outputConfig"]
		if "outputMapping" in data["Option"]:
			O_outputMapping=data["Option"]["outputMapping"]
		if "concat" in data["Option"]:
			O_concat=data["Option"]["concat"]
		if "splice" in data["Option"]:
			O_splice=data["Option"]["splice"]




	#launch analysis
	#---------------------------------------------------------------------------------------------------
	

	if options.verbose:
		print >> sys.stderr,"\n[GLOBAL INFO]"
		print >> sys.stderr,"FILE: "+",".join(tsvfiles)
		print >> sys.stderr,"SAMPLE: "+",".join(filenames)
		print >> sys.stderr,"CONFIG: "+str(configFile)
		print >> sys.stderr,"OUPUT: "+O_output
	#number of steps
	step=1

	if options.platform:
		C_platform=options.platform

	if options.database:
		O_base=options.database

	#TRANSFORM TSV TO DIST
	if options.renameinfo:
		O_renameinfo=options.renameinfo
	if options.index:
		O_indexkey=options.index
	if not O_indexkey:
		O_indexkey="ALL"
	if options.verbose:
		print >> sys.stderr,"\n[RUNNING STEPS]"
		print >> sys.stderr,"Step"+str(step)+" - Transform tsv files to dictionnary"
		print >> sys.stderr,"--renameinfo="+str(O_renameinfo)
		step+=1
	dicof,oldHeader=TsvToDico(tsvfiles,filenames,O_indexkey,O_renameinfo)

	#CONCAT FIELDS IN ONE
	if O_concat:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Concat fields"
			print >> sys.stderr,"--concat="+str(O_concat)
			step+=1
		dicof,oldHeader=concat_fields(dicof,O_concat,oldHeader)

        #a mettre en option!!!
        dicof=arrangeCNOMEN(dicof)

	#RENAME FIELD WITH ALIAS
	if O_alias:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Rename alias"
			print >> sys.stderr,"--alias="+str(O_alias)
			step+=1
		dicof,oldHeader=changeToAlias(dicof,O_alias,oldHeader)
	
	if O_splice:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Get n Splicing site"
			print >> sys.stderr,"--splice="+str(O_splice)
			step+=1
		dicof,oldHeader=getSplice(dicof,oldHeader)

	#SPLIT CHR BEFORE CHROMOSOME NUMBER
	if options.splitchr:
		if options.splitchr == 1:
			O_splitchr=True
		elif options.splitchr == 0:
			O_splitchr=False
		else:
			print >> sys.stderr,"WARNING - invalid integer value: '--splitchr'"
			print >> sys.stderr,"WARNING - Option set to default value: false - Use 1 for true and 0 for false"
	if O_splitchr:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Remove \'chr\'"
			print >> sys.stderr,"--splitchr="+str(O_splitchr)
			step+=1
		dicof=splitCHROM(dicof,"chromosome_number")


	#ADD HGNC ID USING A HGNC ID DB
	if O_hgncdbfile:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Add HGNC id to gene names"
			print >> sys.stderr,"--hgncid="+str(O_hgncdbfile)
			step+=1
		dicof=getHGNCDB(dicof,O_hgncdbfile,"gene_name","")
	

	#ADD DEFAULT VALUE TO A FIELD IF FIELD IS EMPTY
	if O_defaut:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Add default values if value not found"
			print >> sys.stderr,"--defaut="+str(O_defaut)
			step+=1
		dicof,oldHeader=checkMandatory(dicof,O_defaut,oldHeader)


	#TRIMM FIELD NAME BY MAX LENGTH
	if options.trimming:
		O_trimming=options.trimming
	if O_trimming:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Trimm field size"
			print >> sys.stderr,"--trimming="+str(O_trimming)
			step+=1
		dicof=trimming(dicof,O_trimming)
	

	#ADD "n" BEFORE FIELD WHO STATS WITH A NUMBER
	if options.tostring:
		if options.tostring==1:
			O_toString=True
		elif options.tostring==0:
			O_toString=False
		else:
			print >> sys.stderr,"WARNING - invalid integer value: '--tostring'"
			print >> sys.stderr,"WARNING - Option set to default value: false - Use 1 for true and 0 for false"
	if O_toString:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Reformat ambigous column names"
			print >> sys.stderr,"--toString="+str(O_toString)
			step+=1
		dicof,oldHeader=formatNumber(dicof,oldHeader)

	#REPLACE STRING WITH OTHERS IN EACH FIELD NAME
	if O_reformat:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Reformat column names"
			print >> sys.stderr,"--reformat="+str(O_reformat)
			step+=1
		dicof,oldHeader=replaceValues(dicof,O_reformat,oldHeader)


	#CHECK IF ALL FILE HAVE THE SAME NUMBER OF FIELD AND ADD FIELD IF NOT
	if options.verbose:
		print >> sys.stderr,"\nStep"+str(step)+" - Uniformise fields"
		print >> sys.stderr," ----------\n|-OUTLIERS-|\n ----------"
	dicof,HEADER=Uniformise(dicof)
	if options.verbose:
		getOutliers(HEADER)
		step+=1

	#GET FIELD WITH SAMPLE-VARIANT ASSACIATION - FOR MAPPING FILE
	if O_SampleVariant:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Define sample variant annotations"
		SampleVariantListFull=catchRegExp(oldHeader,O_SampleVariant)
		if options.verbose:
			print >> sys.stderr,"--samplevariant="+",".join(SampleVariantListFull)
			step+=1
	else:
		SampleVariantListFull=[]
	SampleVariantList=removeOfficialFields(SampleVariantListFull,data["field"])

	#GET FIELD WITH VARIANT ASSACIATION - FOR MAPPING FILE
	if O_Variant:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Define variant annotations"
		if "*" in O_Variant:
			VariantListFull=[]
			for colonneName in oldHeader:
				if colonneName not in SampleVariantList:
					VariantListFull.append(colonneName)
		else:
			VariantListFull=catchRegExp(oldHeader,O_Variant)
		if options.verbose:	
			print >> sys.stderr,"--variant="+",".join(VariantListFull)
			step+=1
	else:
		VariantListFull=[]
	VariantList=removeOfficialFields(VariantListFull,data["field"])

	#PRIORIZE FIELD DISPLAY IN OUTPUT FILES
	if O_priorize:
		if options.verbose:
			print >> sys.stderr,"\nStep"+str(step)+" - Priorize visualisation"
			print >> sys.stderr,"--priorize="+",".join(O_priorize)
			step+=1
	else:
		O_priorize=[]

	listef=priorizeList(dicof,HEADER,O_priorize)
	
	

	#WRITE RESULTS
	if not options.stdout:

		#WRITE OUTPUT FILE
		if not O_fileExtension:
			O_fileExtension=".tsv"
		writeList(listef,O_output,O_fileExtension)


		#WRITE MAPPING FILE
		if options.outputmapping:
			O_outputMapping=options.outputmapping
		if O_outputMapping:
			if options.progannot:
				tmp_annotation=extractDict(options.progannot)
				for names in tmp_annotation:
					O_annotation["name"]=names
					O_annotation["version"]=tmp_annotation[names]
			getMapping(data,O_annotation,SampleVariantList,VariantList,O_outputMapping)
		

		#WRITE CONFIG FILE
		if options.outputconfig:
			O_outputConfig=options.outputconfig
		if O_outputConfig:
			if options.progannot:
				tmp_annotation=extractDict(options.progannot)
				for names in tmp_annotation:
					O_annotation["name"]=names
					O_annotation["version"]=tmp_annotation[names]
			if options.progcall:
				tmp_calling=extractDict(options.progcall)
				for names in tmp_calling:
					O_calling["name"]=names
					O_calling["version"]=tmp_calling[names]
			getConfig(O_annotation,O_calling,O_outputConfig,C_serie,C_setCapture,C_platform,O_output,O_outputMapping,C_protocol,O_fileExtension,O_base)

	#IF STDOUT OPTION CONCAT FILES AND PRINT RESULTS
	else:
		printList(listef)

	if options.verbose:
		print >> sys.stderr,"\n[END]\n"


if __name__ == '__main__':
	main()



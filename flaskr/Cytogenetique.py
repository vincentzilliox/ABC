import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

Cytogenetique = Blueprint('Cytogenetique', __name__, url_prefix='/Cytogenetique')
UPLOAD_FOLDER = '/uploads'
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')

@Cytogenetique.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		boolean_opt = []
		inputfilelist = []
		for f in request.files.getlist('HOMME'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		HOMME = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('FEMME'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		FEMME = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('RECLUSTERING'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		RECLUSTERING = ','.join(inputfilelist)
		default_opt = ''
		choice_opt = ' -a '+HOMME+' -b '+FEMME+' -c '+RECLUSTERING+' '
		outputfilename=CURRENT_DATE+'.cartagenia.reclustering.txt'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('sh /home1/L/CYTOGENETIQUE/SNP_Illumina/programmes/script.sh' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' -o ' + outputfile, shell=True)
		return redirect(url_for('Cytogenetique.uploaded', filename=outputfilename))
	return render_template('Cytogenetique/upload.html')

@Cytogenetique.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('Cytogenetique/uploaded.html', filename=filename)

@Cytogenetique.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

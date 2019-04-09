import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

Cartagenia = Blueprint('Cartagenia', __name__, url_prefix='/Cartagenia')
UPLOAD_FOLDER = '/uploads'
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')

@Cartagenia.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		boolean_opt = []
		inputfilelist = []
		for f in request.files.getlist('Femmes'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		Femmes = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('Hommes'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		Hommes = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('Reclustering'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		Reclustering = ','.join(inputfilelist)
		default_opt = ''
		choice_opt = ' -f '+Femmes + ' ' + ' -m '+Hommes + ' ' + ' -r '+Reclustering
		outputfilename=CURRENT_DATE+'.cartagenia.reclustering.txt'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('sh /app/flaskr/toolkit/cartagenia.sh' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' -o ' + outputfile, shell=True)
		return redirect(url_for('Cartagenia.uploaded', filename=outputfilename))
	return render_template('Cartagenia/upload.html')

@Cartagenia.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('Cartagenia/uploaded.html', filename=filename)

@Cartagenia.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

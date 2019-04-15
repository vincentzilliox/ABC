import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

CNVPartition = Blueprint('CNVPartition', __name__, url_prefix='/CNVPartition')
UPLOAD_FOLDER = '/uploads'

@CNVPartition.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')
		boolean_opt = []
		inputfilelist = []
		for f in request.files.getlist('ReclusteringFemmes'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		ReclusteringFemmes = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('ReclusteringHommes'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		ReclusteringHommes = ','.join(inputfilelist)
		inputfilelist = []
		for f in request.files.getlist('Reclustering'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		Reclustering = ','.join(inputfilelist)
		default_opt = ''
		choice_opt = ' -f '+ReclusteringFemmes + ' ' + ' -m '+ReclusteringHommes + ' ' + ' -r '+Reclustering
		outputfilename=CURRENT_DATE+'.infinium.reclustering.txt'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('sh /app/flaskr/toolkit/CNV_Partition.sh' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' -o ' + outputfile, shell=True)
		return redirect(url_for('CNVPartition.uploaded', filename=outputfilename))
	return render_template('CNVPartition/upload.html')

@CNVPartition.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('CNVPartition/uploaded.html', filename=filename)

@CNVPartition.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

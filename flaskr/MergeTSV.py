import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

MergeTSV = Blueprint('MergeTSV', __name__, url_prefix='/MergeTSV')
UPLOAD_FOLDER = '/uploads'

@MergeTSV.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')
		boolean_opt = []
		inputfilelist = []
		for f in request.files.getlist('inputfiles'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		inputfiles = ','.join(inputfilelist)
		default_opt = '-c "/app/flaskr/config/configuration.concat.json" --stdout'
		choice_opt = ' -a '+inputfiles
		outputfilename=CURRENT_DATE+'.merged.final.tsv'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('python2.7 /app/flaskr/toolkit/tsvToCanDiD.py' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' > '+outputfile, shell=True)
		return redirect(url_for('MergeTSV.uploaded', filename=outputfilename))
	return render_template('MergeTSV/upload.html')

@MergeTSV.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('MergeTSV/uploaded.html', filename=filename)

@MergeTSV.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

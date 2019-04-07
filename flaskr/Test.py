import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

Test = Blueprint('Test', __name__, url_prefix='/Test')
UPLOAD_FOLDER = '/uploads'
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')

@Test.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		boolean_opt = []
		default_opt = '--help'
		choice_opt = ' '
		outputfilename=CURRENT_DATE+'.merged.final.tsv'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('python2.7 /app/flaskr/toolkit/tsvToCanDiD.py' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' > '+outputfile, shell=True)
		return redirect(url_for('Test.uploaded', filename=outputfilename))
	return render_template('Test/upload.html')

@Test.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('Test/uploaded.html', filename=filename)

@Test.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

Args = Blueprint('Args', __name__, url_prefix='/Args')
UPLOAD_FOLDER = '/uploads'

@Args.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		CURRENT_DATE = datetime.datetime.now().strftime("%F").replace('-','')+'-'+datetime.datetime.now().strftime("%T").replace(':','')
		boolean_opt = []
		inputfilelist = []
		for f in request.files.getlist('File'):
			f.save(os.path.join(UPLOAD_FOLDER, f.filename))
			file_to_process=UPLOAD_FOLDER+'/'+f.filename
			inputfilelist.append(file_to_process)
		File = ','.join(inputfilelist)
		Argument=request.form.get('Argument')
		default_opt = ''
		choice_opt = File + ' ' + Argument
		outputfilename=CURRENT_DATE+'.test_args.txt'
		outputfile=UPLOAD_FOLDER+'/'+outputfilename
		subprocess.call('sh /app/flaskr/toolkit/args_test.sh' + ' ' + default_opt + ' ' + choice_opt + ' ' + " ".join(boolean_opt) + ' > '+outputfile, shell=True)
		return redirect(url_for('Args.uploaded', filename=outputfilename))
	return render_template('Args/upload.html')

@Args.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
	return render_template('Args/uploaded.html', filename=filename)

@Args.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

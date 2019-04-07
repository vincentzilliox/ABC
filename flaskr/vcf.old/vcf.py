import os, subprocess, datetime
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, Response, Blueprint, jsonify, session


UPLOAD_FOLDER = '/uploads'
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace("-","")+"-"+datetime.datetime.now().strftime("%T").replace(":","")

Vcf = Blueprint('Vcf', __name__, url_prefix='/Vcf')

PYTHON_SCRIPT_tsvToCanDiD = os.path.join(vcf.root_path, 'toolkit', 'tsvToCanDiD.py')

@vcf.route("/account")
def accountList():
    return "list of accounts"


@vcf.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'filelist' in request.files:
        
        splitchr = request.form.get('splitchr')
        trimming = request.form.get('trimming')
        cars = request.form.get('cars')

        outputfilename=CURRENT_DATE+".merged.final.tsv"
        outputfile=UPLOAD_FOLDER+"/"+outputfilename
        outputlog=outputfile+".log"
        inputfilelist = []
        for f in request.files.getlist('filelist'):
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            file_to_process=UPLOAD_FOLDER+"/"+f.filename
            inputfilelist.append(file_to_process)

        subprocess.call("python2.7 "+PYTHON_SCRIPT_tsvToCanDiD+" --help &> "+outputfile, shell=True)
        #subprocess.call("python2.7 "+PYTHON_SCRIPT_tsvToCanDiD+" --help &> "+outputlog, shell=True)

        return redirect(url_for('uploaded', filename=outputfilename))
    #return render_template('vcf/upload.html')
    return "vcf upload"


"""
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'filelist' in request.files:
        
        splitchr = request.form.get('splitchr')
        trimming = request.form.get('trimming')
        cars = request.form.get('cars')

        outputfilename=CURRENT_DATE+".merged.final.tsv"
        outputfile=app.config['UPLOAD_FOLDER']+"/"+outputfilename
        outputlog=outputfile+".log"
        inputfilelist = []
        for f in request.files.getlist('filelist'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_to_process=app.config['UPLOAD_FOLDER']+"/"+f.filename
            inputfilelist.append(file_to_process)

        subprocess.call("python2.7 "+PYTHON_SCRIPT_tsvToCanDiD+" --help &> "+outputfile, shell=True)
        #subprocess.call("python2.7 "+PYTHON_SCRIPT_tsvToCanDiD+" --help &> "+outputlog, shell=True)

        return redirect(url_for('uploaded', filename=outputfilename))
    return render_template('vcf/upload.html')

@app.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
    return render_template('vcf/uploaded.html', filename=filename)

@app.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

"""





import os, subprocess, datetime
from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint

vcf = Blueprint('vcf', __name__, url_prefix='/vcf')
UPLOAD_FOLDER = '/uploads'
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace("-","")+"-"+datetime.datetime.now().strftime("%T").replace(":","")
PYTHON_SCRIPT_tsvToCanDiD = os.path.join(vcf.root_path, 'toolkit', 'tsvToCanDiD.py')

@vcf.route("/")
def accountList():
    return "test is ok"

@vcf.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'filelist' in request.files:
        
        #inputoptions
        splitchr = request.form.get('splitchr')
        trimming = request.form.get('trimming')
        cars = request.form.get('cars')

        #inputfiles
        inputfilelist = []
        for f in request.files.getlist('filelist'):
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            file_to_process=UPLOAD_FOLDER+"/"+f.filename
            inputfilelist.append(file_to_process)
        inputfilestr = ",".join(inputfilelist)

        #outputfile
        outputfilename=CURRENT_DATE+".merged.final.tsv"
        outputfile=UPLOAD_FOLDER+"/"+outputfilename
        

        subprocess.call("python2.7 "+PYTHON_SCRIPT_tsvToCanDiD+" --help &> "+outputfile, shell=True)

        return redirect(url_for('vcf.uploaded', filename=outputfilename))
    return render_template('vcf/upload.html')

@vcf.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):
    return render_template('vcf/uploaded.html', filename=filename)

@vcf.route('/upload/<filename>', methods=['GET'])
def getuploaded(filename):
   return send_from_directory(UPLOAD_FOLDER, filename)






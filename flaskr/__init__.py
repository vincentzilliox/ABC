import os
import datetime
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'tsv', 'vcf','csv'])
CURRENT_DATE = datetime.datetime.now().strftime("%F").replace("-","")+"-"+datetime.datetime.now().strftime("%T").replace(":","")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    @app.route('/')
    def home():
        return render_template('home/index.html')


    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST' and 'filelist' in request.files:
            outputfilename=CURRENT_DATE+".merged.final.tsv"
            outputfile=app.config['UPLOAD_FOLDER']+"/"+outputfilename
            outfile = open(outputfile, "w")
            for f in request.files.getlist('filelist'):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                file_to_process=app.config['UPLOAD_FOLDER']+"/"+f.filename
                infile = open(file_to_process, "r")
                for line in infile:
                    outfile.write(line.strip()+"\tprocessed\n")
                infile.close()
            outfile.close()
            return redirect(url_for('uploaded', filename=outputfilename))
        return render_template('vcf/upload.html')

    @app.route('/upload/<filename>')
    def uploaded(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



    return app







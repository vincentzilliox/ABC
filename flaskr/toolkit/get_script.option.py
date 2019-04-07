import json
import os
import re

def getAppPath():
	return "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])+"/"

def loadJson(jsonFile):
	with open(jsonFile) as json_file:
		data = json.load(json_file)
	return data

def buildTool(data, appPath):
	toolTemplate = appPath+"templates/tools.html"
	toolList = [ re.sub('\W+','', x) for x in data.keys() ]
	with open(toolTemplate, "w") as outfile:
		outfile.write("{% extends 'base.html' %}\n{% block tool %}\n")
		for tool in toolList:
			outfile.write("\t<li class=\"nav-item\">\n")
			outfile.write("\t\t<a class=\"nav-link\" href=\"{{ url_for('"+tool+".upload') }}\">"+tool+"</a>\n")
			outfile.write("\t</li>\n")
		outfile.write("{% endblock %}\n")


def buidView(data, appPath):
	for tool in data:

		cleanTool = re.sub('\W+','', tool )
		viewDir=appPath
		viewTemplate=viewDir+cleanTool+".py"
		script=data[tool]["script"]
		script_location=data[tool]["script_location"]
		output=data[tool]["output"]
		output_file_extension=data[tool]["output_file_extension"]
		options=data[tool]["options"]
		#option_list=["--help"]

		if not os.path.exists(viewDir):
			os.makedirs(viewDir)
		with open(viewTemplate, "w") as outfile:
			outfile.write("import os, subprocess, datetime\n")
			outfile.write("from flask import request, redirect, url_for, send_from_directory, render_template, Blueprint\n")
			outfile.write("\n"+cleanTool+" = Blueprint('"+cleanTool+"', __name__, url_prefix='/"+cleanTool+"')\n")
			outfile.write("UPLOAD_FOLDER = '/uploads'\n")
			outfile.write("CURRENT_DATE = datetime.datetime.now().strftime(\"%F\").replace('-','')+'-'+datetime.datetime.now().strftime(\"%T\").replace(':','')\n")
			outfile.write("\n@"+cleanTool+".route('/upload', methods=['GET', 'POST'])\n")
			outfile.write("def upload():\n")
			outfile.write("\tif request.method == 'POST':\n")
			outfile.write("\t\tboolean_opt = []\n")
			
			default_option_list=[]
			choice_option_list=[]
			for opt in options:
				if "name" in opt:
					optname = re.sub('\W+','', opt["name"] )
					if opt["type"] == "file":
						outfile.write("\t\tinputfilelist = []\n")
						outfile.write("\t\tfor f in request.files.getlist('"+optname+"'):\n")
						outfile.write("\t\t\tf.save(os.path.join(UPLOAD_FOLDER, f.filename))\n")
						outfile.write("\t\t\tfile_to_process=UPLOAD_FOLDER+'/'+f.filename\n")
						outfile.write("\t\t\tinputfilelist.append(file_to_process)\n")
						outfile.write("\t\t"+optname+" = ','.join(inputfilelist)\n")
						choice_option_list.append("' "+opt["option"]+" '+"+optname+"+")

					elif opt["type"] == "boolean":
						outfile.write("\t\t"+optname+"=request.form.get('"+optname+"')\n")
						outfile.write("\t\tif "+optname+" == 'Yes' :\n")
						outfile.write("\t\t\tboolean_opt.append('"+opt["option"]+"')\n")

					else:
						outfile.write("\t\t"+optname+"=request.form.get('"+optname+"')\n")
						choice_option_list.append("' "+opt["option"]+" '+"+optname+"+")
				else:
					if "default" in opt:
						default_option_list.append(opt["option"]+" \""+opt["default"]+"\"")
					else:
						default_option_list.append(opt["option"])

			outfile.write("\t\tdefault_opt = '"+" ".join(default_option_list)+"'\n")
			outfile.write("\t\tchoice_opt = "+"".join(choice_option_list)+"' '\n")
			outfile.write("\t\toutputfilename=CURRENT_DATE+'."+output_file_extension+"'\n")
			outfile.write("\t\toutputfile=UPLOAD_FOLDER+'/'+outputfilename\n")

			if output == "stdout":
				outfile.write("\t\tsubprocess.call('"+script+" "+script_location+"' + ' ' + default_opt + ' ' + choice_opt + ' ' + \" \".join(boolean_opt) + ' > '+outputfile, shell=True)\n")
			else:
				outfile.write("\t\tsubprocess.call('"+script+" "+script_location+"' + ' ' + default_opt + ' ' + choice_opt + ' ' + \" \".join(boolean_opt) + ' "+output+" ' + outputfile, shell=True)\n")

			outfile.write("\t\treturn redirect(url_for('"+cleanTool+".uploaded', filename=outputfilename))\n")
			outfile.write("\treturn render_template('"+cleanTool+"/upload.html')\n")
			outfile.write("\n@"+cleanTool+".route('/uploaded/<filename>', methods=['GET', 'POST'])\n")
			outfile.write("def uploaded(filename):\n")
			outfile.write("\treturn render_template('"+cleanTool+"/uploaded.html', filename=filename)\n")
			outfile.write("\n@"+cleanTool+".route('/upload/<filename>', methods=['GET'])\n")
			outfile.write("def getuploaded(filename):\n")
			outfile.write("\treturn send_from_directory(UPLOAD_FOLDER, filename)\n")


def buildTemplate(data, appPath):

	for tool in data:

		cleanTool = re.sub('\W+','', tool )
		TemplateDir=appPath+"templates/"+cleanTool
		TemplateFileUpload=TemplateDir+"/upload.html"
		TemplateFileUploaded=TemplateDir+"/uploaded.html"
		options=data[tool]["options"]


		if not os.path.exists(TemplateDir):
			os.makedirs(TemplateDir)
		with open(TemplateFileUpload, "w") as outfile:
			outfile.write("{% extends 'tools.html' %}\n")
			outfile.write("{% block header %}\n")
			outfile.write("\t<div class=\"jumbotron jumbotron-fluid\" style=\"margin:10px;\">\n")
			outfile.write("\t\t<div class=\"container\">\n")
			outfile.write("\t\t\t<h1 class=\"display-4\"  id=\"color-theme\">{% block title %}"+tool+"{% endblock %}</h1>\n")
			if data[tool]["comment"]:
				outfile.write("\t\t\t<p class=\"lead\">"+data[tool]["comment"]+"</p>\n")
			outfile.write("\t\t</div>\n")
			outfile.write("\t</div>\n")
			outfile.write("{% endblock %}\n")
			outfile.write("{% block content %}\n")
			outfile.write("\t<div id=\"loading\"></div>\n")
			outfile.write("\t<div id=\"content\">\n")
			outfile.write("\t\t<form method=\"POST\" enctype=\"multipart/form-data\">\n")

			for opt in options:
				if "name" in opt:
					optname = re.sub('\W+','', opt["name"])
					outfile.write("\t\t\t<div class=\"row border-bottom\">\n")
					outfile.write("\t\t\t\t<div class=\"col-md-4\">\n")
					if "comment" in opt:
						outfile.write("\t\t\t\t\t<a class=\"font-weight-bold\" data-toggle=\"tooltip\" data-placement=\"top\" title=\""+opt["comment"]+"\">"+opt["name"]+": </a>\n")
					else:
						outfile.write("\t\t\t\t\t<a class=\"font-weight-bold\">"+opt["name"]+": </a>\n")
					outfile.write("\t\t\t\t</div>\n")
					outfile.write("\t\t\t\t<div class=\"col-md-4\">\n")
					if opt["type"] == "file":
						outfile.write("\t\t\t\t\t<input type=\"file\" name=\""+optname+"\" multiple>\n")
					elif opt["type"] == "boolean":
						outfile.write("\t\t\t\t\t<select name=\""+optname+"\">\n")
						for item in ["Yes","No"]:
							outfile.write("\t\t\t\t\t\t<option value=\""+item+"\">"+item+"</option>\n")
						outfile.write("\t\t\t\t\t</select><br>\n")
					else:
						outfile.write("\t\t\t\t\t<select name=\""+optname+"\">\n")
						for item in opt["choice"]:
							outfile.write("\t\t\t\t\t\t<option value=\""+item+"\">"+item+"</option>\n")
						outfile.write("\t\t\t\t\t</select><br>\n")
					outfile.write("\t\t\t\t</div>\n")
					outfile.write("\t\t\t</div>\n")

			outfile.write("\t\t<div class=\"row justify-content-center\">\n")
			outfile.write("\t\t\t<div class=\"col-4\">\n")
			outfile.write("\t\t\t\t<input  class=\"btn btn-primary\" type=\"submit\" value=\"Submit\" onclick=\"loading();\">\n")
			outfile.write("\t\t\t</div>\n")
			outfile.write("\t\t</div>\n")
			outfile.write("\t\t</form>\n")
			outfile.write("\t</div>\n")
			outfile.write("{% endblock %}\n")

		with open(TemplateFileUploaded, "w") as outfile:
			outfile.write("{% extends 'tools.html' %}\n")
			outfile.write("{% block header %}\n")
			outfile.write("\t<div class=\"jumbotron jumbotron-fluid alert-success\" style=\"margin:10px;\">\n")
			outfile.write("\t\t<div class=\"container\">\n")
			outfile.write("\t\t\t<h1 class=\"display-4\">{% block title %}Successfuly uploaded !{% endblock %}</h1>\n")
			outfile.write("\t\t\t<p class=\"lead\">\n")
			outfile.write("\t\t\t\t<a href=\"{{ url_for('"+cleanTool+".getuploaded', filename=filename) }}\">\n")
			outfile.write("\t\t\t\t\t<button class=\"btn btn-primary\">Download</button>\n")
			outfile.write("\t\t\t\t</a>Click to access to the result\n")
			outfile.write("\t\t\t</p>\n")
			outfile.write("\t\t</div>\n")
			outfile.write("\t</div>\n")
			outfile.write("{% endblock %}\n")
			outfile.write("{% block content %}\n")
			outfile.write("\t<div class=\"alert alert-warning alert-dismissible fade show\" role=\"alert\" style=\"margin:10px;\">\n")
			outfile.write("\t\t<strong>Warning</strong>: Please check your results carefully (<strong>beta version</strong>)\n")
			outfile.write("\t\t<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n")
			outfile.write("\t\t\t<span aria-hidden=\"true\">&times;</span>\n")
			outfile.write("\t\t</button>\n")
			outfile.write("\t</div>\n")
			outfile.write("{% endblock %}\n")

def buildInit(appName,data, appPath):
	initFile = appPath+"__init__.py"
	with open(initFile, "w") as outfile:
		outfile.write("from flask import Flask, render_template\n")
		outfile.write("def create_app():\n")
		outfile.write("\tapp = Flask(__name__)\n")
		outfile.write("\t@app.route('/')\n")
		outfile.write("\tdef home():\n")
		outfile.write("\t\treturn render_template('home/index.html')\n")

		for tool in data:
			cleanTool = re.sub('\W+','', tool )
			outfile.write("\tfrom "+appName+"."+cleanTool+" import "+cleanTool+"\n")
			outfile.write("\tapp.register_blueprint("+cleanTool+")\n")

		outfile.write("\treturn app\n")

def delApp():
	pass


appName = "flaskr"
appPath = getAppPath()
data = loadJson(appPath+"config/app.config.json")

buildTool(data, appPath)
buidView(data, appPath)
buildTemplate(data, appPath)
buildInit(appName,data,appPath)


"""
for tool in data:

	cleanTool = re.sub('\W+','', tool )
	websiteTemplate=appPath+"templates/"+cleanTool+"/index.html"
	websiteView=appPath+cleanTool+"/"+cleanTool+".py"
	print(websiteTemplate,websiteView)
"""




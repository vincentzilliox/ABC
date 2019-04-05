import json
import os
import re


def getAppPath():
	return "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])+"/"

def loadJson(jsonFile):
	with open(jsonFile) as json_file:
		data = json.load(json_file)
	return data

appPath = getAppPath()
data = loadJson(appPath+"config/app.config.json")

for tool in data:
	cleanTool = re.sub('\W+','', tool )
	websiteTemplate=appPath+"templates/"+cleanTool+"/index.html"
	websiteView=appPath+cleanTool
<<<<<<< HEAD
	print(websiteTemplate,websiteView)
=======
	print(websiteTemplate,websiteView)
>>>>>>> a30eda84267f0a52558bd8e3abe6240bde8b9ad2

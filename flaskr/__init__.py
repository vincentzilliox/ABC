from flask import Flask, render_template
def create_app():
	app = Flask(__name__)
	@app.route('/')
	def home():
		return render_template('home/index.html')
	from flaskr.MergeTSV import MergeTSV
	app.register_blueprint(MergeTSV)
	from flaskr.Cartagenia import Cartagenia
	app.register_blueprint(Cartagenia)
	from flaskr.Test import Test
	app.register_blueprint(Test)
	return app

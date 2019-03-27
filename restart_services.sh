docker stop flask_app && docker rm flask_app
rm -rf flaskr/__pycache__/*
docker build -t flask-sample-one:latest . && docker run -d --name flask_app -v ${PWD}:/app -p 5000:5000 flask-sample-one

FROM centos:7
MAINTAINER Vincent Zilliox "vzilliox@gmail.com"

RUN yum -y install epel-release python2-setuptools
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip
RUN pip3.6 install Flask pytest coverage shelljob
ENV LC_ALL=en_IE.utf8
ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

RUN mkdir /uploads
#COPY . /app
WORKDIR /app
#RUN pip3.6 install -r requirements.txt

ENTRYPOINT ["python3.6"]
CMD ["-m","flask","run","--host=0.0.0.0"]

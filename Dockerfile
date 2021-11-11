FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /adv
WORKDIR /adv
ADD requirements.txt /adv/
RUN pip install -r requirements.txt
ADD . /adv/
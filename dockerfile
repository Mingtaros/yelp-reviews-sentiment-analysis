FROM tensorflow/tensorflow:latest-gpu

WORKDIR /
ADD ./requirements.txt /
RUN pip3 install -r requirements.txt
RUN rm ./requirements.txt
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

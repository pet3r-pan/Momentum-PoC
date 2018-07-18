FROM ubuntu:latest
MAINTAINER Regio Michelin "regio.michelin@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "Momentum.py", "3001"]
#CMD ["Momentum.py"]
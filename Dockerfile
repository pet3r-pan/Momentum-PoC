FROM tiangolo/uwsgi-nginx-flask:flask
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 443
ENTRYPOINT ["python"]
CMD ["main.py", "3000"]


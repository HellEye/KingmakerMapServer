FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /usr/app/src
COPY requirements.txt  .
EXPOSE 8255
RUN python3.8 -m pip install -r requirements.txt
COPY . .
CMD ["python3.8", "src/KingmakerDB.py"]

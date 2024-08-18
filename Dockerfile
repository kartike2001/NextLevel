FROM python:3.8
WORKDIR /root
COPY . .

RUN pip3 install pymongo bcrypt Flask requests

EXPOSE 3000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD /wait && flask run --host=0.0.0.0 --port=3000

FROM python:3.9

ADD . .

ENV APP_NAME=ForumParser

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]
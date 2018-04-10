FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN python -m nltk.downloader all

CMD [ "python",  "hq_main.py" ]

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# install nltk files
RUN python -m nltk.downloader all
CMD [ "python",  "go.py" ]
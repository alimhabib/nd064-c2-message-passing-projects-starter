
FROM python

RUN mkdir /service
COPY app/ /service/ 

WORKDIR /service
RUN pip install -r requirements.txt 

ENTRYPOINT [ "python", "start.py" ]

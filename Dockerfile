FROM python

WORKDIR /backend

COPY . /backend

ENV PYTHONPATH ./

RUN pip3 install -r requirements.txt

CMD ["python3", "api/src/main.py"]

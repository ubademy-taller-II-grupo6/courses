FROM python
WORKDIR /app
COPY ./api/src/*.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV PORT=$PORT DATABASE_URL=$DATABASE_URL
CMD [ "python3", "main.py" ]
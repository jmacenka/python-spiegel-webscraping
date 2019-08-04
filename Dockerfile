FROM python:3.7-slim-stretch
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","Webscraping_Spiegel.py"]

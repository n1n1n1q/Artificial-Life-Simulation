FROM python:3.11

WORKDIR /
COPY src /src
COPY requirements.txt /
RUN pip install -r requirements.txt

CMD ["python","src/main.py"]
FROM python:buster
WORKDIR /warsnake
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python3", "server.py"]
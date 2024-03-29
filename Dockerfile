FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -e .
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
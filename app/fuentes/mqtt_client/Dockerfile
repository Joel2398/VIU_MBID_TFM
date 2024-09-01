FROM python:3.8

WORKDIR /code

COPY requirments.txt . 

RUN pip install -r requirments.txt 

COPY app.py . 

CMD ["python", "app.py"]
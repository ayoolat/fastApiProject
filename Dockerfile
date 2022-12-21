FROM python:3.9

COPY . /fastApiProject
COPY ./requirements.txt /fastApiProject/requirements.txt
WORKDIR /fastApiProject

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 80
EXPOSE 443
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
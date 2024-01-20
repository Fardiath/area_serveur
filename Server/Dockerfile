FROM python:3.9

WORKDIR /djangoapps

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 777 djangoapps/manage.py

RUN python djangoapps/manage.py makemigrations
RUN python djangoapps/manage.py migrate

CMD ["python", "djangoapps/manage.py", "runserver", "0.0.0.0:8080"]



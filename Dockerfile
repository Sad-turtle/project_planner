FROM python:3.6.1-alpine
WORKDIR /projectPlanner
ADD . /projectPlanner
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]
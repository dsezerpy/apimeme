FROM python:3.11
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app/* /app/
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
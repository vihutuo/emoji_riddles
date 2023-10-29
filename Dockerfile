FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install poetry && pip install --no-build-isolation pendulum

COPY . .

EXPOSE 8080

CMD ["python", "./main.py"]
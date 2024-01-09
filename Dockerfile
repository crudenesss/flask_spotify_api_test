FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY templates templates/

COPY functions.py .

COPY init_classes.py .

COPY commands.py .

COPY main.py .

EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
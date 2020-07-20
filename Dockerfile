FROM 3.7-alpine

WORKDIR /app
COPY . /app
EXPOSE 80
CMD ["python", "main.py"]

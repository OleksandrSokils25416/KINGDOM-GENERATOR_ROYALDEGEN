FROM python:3.11
WORKDIR /app
COPY kingdom1/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY kingdom1/ .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

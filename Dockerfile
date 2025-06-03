FROM python:3.10-slim

# Tạo thư mục làm việc
WORKDIR /app

# Cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code và dữ liệu vào container
COPY . .

# Cổng chạy app
EXPOSE 8000

# Chạy FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
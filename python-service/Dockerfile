FROM python:3.9-slim

WORKDIR /app

# Bağımlılıkları kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm python-service dosyalarını kopyala (app.py, simulator.py vs.)
COPY . .

# Varsayılan komut
CMD ["python", "app.py"]

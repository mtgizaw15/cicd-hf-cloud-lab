# Python 3.10 image
FROM python:3.10-slim

# Függőségek telepítése az OS szinten (face_recognition-hoz szükséges)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár beállítása
WORKDIR /app

# Projekt másolása a konténerbe
COPY . .

# Követelmények másolása és telepítése
RUN pip install --no-cache-dir -r requirements.txt

# Flask szerver indítása
CMD ["python", "run.py"]

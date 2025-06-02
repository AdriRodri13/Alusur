FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 🛠️ Instala netcat para wait-for-db y limpia el caché
RUN apt-get update && apt-get install -y netcat && apt-get clean

# Crea carpeta de trabajo
WORKDIR /app

# Copia dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código
COPY . /app/

# Copia el script de arranque
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "Alusur.wsgi:application", "--bind", "0.0.0.0:8000"]

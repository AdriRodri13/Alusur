# Usa imagen base oficial de Python
FROM python:3.11-slim

# Variables de entorno para evitar escritura de bytecode y para logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Crea entorno virtual
RUN python -m venv /opt/venv

# 🛠️ Instala dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crea carpeta de trabajo
WORKDIR /app

# Copia requirements e instala Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código de la app
COPY . /app/

# Copia el script de arranque
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expone el puerto 8000 (opcional, Railway lo maneja internamente)
EXPOSE 8000

# Usa el script como entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto: arranca el servidor
CMD ["gunicorn", "Alusur.wsgi:application", "--bind", "0.0.0.0:8000"]

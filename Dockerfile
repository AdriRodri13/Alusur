# Usa imagen oficial de Python
FROM python:3.11-slim

# Variables de entorno para evitar preguntas de pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Crea carpeta de trabajo
WORKDIR /app

# Copia dependencias
COPY requirements.txt /app/

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código
COPY . /app/

# Copia el script de arranque
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expone el puerto (opcional en Railway)
EXPOSE 8000

# Usa el entrypoint personalizado
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto para arrancar el servidor
CMD ["gunicorn", "Alusur.wsgi:application", "--bind", "0.0.0.0:8000"]

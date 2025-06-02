#!/bin/bash
set -e

# 🔍 Extrae el host desde DATABASE_URL si DB_HOST no está definido
if [ -z "$DB_HOST" ]; then
    DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|^.*://[^@]+@([^:/]+).*$|\1|')
fi

echo "⏳ Esperando a que la base de datos esté disponible en $DB_HOST:5432..."

# 🕓 Espera hasta que el host esté disponible
until nc -z "$DB_HOST" 5432; do
  echo "⏳ Base de datos no disponible aún. Esperando..."
  sleep 1
done

echo "✅ Base de datos disponible. Ejecutando migraciones..."

# ⚙️ Migraciones y archivos estáticos
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 👤 Crea superusuario si no existe
echo "⚙️  Creando superusuario si no existe..."
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Alusur2025')
" | python manage.py shell

# 🚀 Ejecuta el proceso principal (gunicorn por defecto desde CMD en Dockerfile)
exec "$@"

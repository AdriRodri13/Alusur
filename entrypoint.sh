#!/bin/bash
set -e

echo "⏳ Esperando a que la base de datos esté disponible..."

# Usa nc (netcat) para esperar la base de datos en el puerto 5432
until nc -z "$DB_HOST" 5432; do
  echo "⏳ Base de datos no disponible aún. Esperando..."
  sleep 1
done

echo "✅ Base de datos disponible. Ejecutando migraciones..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "⚙️  Creando superusuario si no existe..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'Alusur2025')" | python manage.py shell

exec "$@"

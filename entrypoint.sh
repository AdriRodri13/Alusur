#!/bin/bash
set -e

# Extrae el host si no está definido explícitamente
if [ -z "$DB_HOST" ]; then
    DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|^.*://[^@]+@([^:/]+).*$|\1|')
fi

echo "⏳ Esperando a que la base de datos esté disponible en $DB_HOST:5432..."

until nc -z "$DB_HOST" 5432; do
  echo "⏳ Base de datos no disponible aún. Esperando..."
  sleep 1
done

echo "✅ Base de datos disponible. Ejecutando migraciones..."

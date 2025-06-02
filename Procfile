release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'Alusur2025')" | python manage.py shell

web: gunicorn Alusur.wsgi:application --log-file - --bind 0.0.0.0:8000

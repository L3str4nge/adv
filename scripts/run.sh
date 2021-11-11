echo "Running migration"
python manage.py migrate

echo "Collect static"
python manage.py collectstatic --noinput

echo "Run server"
python manage.py runserver 0.0.0.0:8000
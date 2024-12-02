pip install -r requirements.txt
echo "Before collectstatic"
python3.9 manage.py collectstatic --noinput
echo "After collectstatic"

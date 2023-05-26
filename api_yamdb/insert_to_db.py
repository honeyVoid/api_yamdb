import os
import django
import csv
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

conn = connections['default']
cursor = conn.cursor()


with open('static/data/genre_title.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute(
            'INSERT INTO reviews_genretitle (genre_id, title_id) VALUES (%s, %s)',
            (row['title_id'], row['genre_id'])
        )

conn.commit()
conn.close()

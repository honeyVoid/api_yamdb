import csv
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


with open(
    'api_yamdb/static/data/category.csv',
    'r',
    newline='',
    encoding='utf-8'
) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute()

conn.commit()
conn.close()
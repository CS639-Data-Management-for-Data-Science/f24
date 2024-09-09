import csv
from pathlib import Path

count = 0

with open(Path('data') / Path('spotify.csv')) as FH:
  csv_file = csv.reader(FH)
  for lines in csv_file:
        count += 1

print(count)

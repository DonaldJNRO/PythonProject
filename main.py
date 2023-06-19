import urllib.request
import json
import os.path
import csv

infile = urllib.request.urlopen('https://api.tfl.gov.uk/StopPoint/490005624S/arrivals')
arrival_times_json = infile.read().decode()
with open("bus-timetable.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
arrival_times = json.loads(arrival_times_json)
print(arrival_times_json)

for arrival in arrival_times:
    destination_name = arrival["destinationName"]
    print(destination_name)

file = "arrival_times.json"

if not os.path.exists(file):
    with open(file, 'w') as file:
        json.dump(arrival_times, file)
        print("File saved successfully.")

else:
    print("File already exists.")


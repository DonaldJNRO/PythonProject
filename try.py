import urllib.request
import json
import csv
import matplotlib.pyplot as plt

csv_file = ('bus-timetable.csv')

infile = urllib.request.urlopen('https://api.tfl.gov.uk/StopPoint/490008645U/arrivals')


class ArrivalTimes:
    def __init__(self, csv_file):
        self._csv_file = csv_file
        self.arrival_times = []

    def fetch_arrival_times(self):
        arrival_times_json = infile.read().decode()
        self.arrival_times = json.loads(arrival_times_json)

    def save_to_csv(self):
        with open(self._csv_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.arrival_times[0].keys())  # Write the header row
            for arrival in self.arrival_times:
                writer.writerow(arrival.values())
        print("File saved successfully.")



    def display_arrival_stats(self):
        destinations = [arrival["destinationName"] for arrival in self.arrival_times]
        destination_counts = {destination: destinations.count(destination) for destination in set(destinations)}
        destinations = list(destination_counts.keys())
        counts = list(destination_counts.values())

        with open(self._csv_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)


        plt.bar(destinations, counts)
        plt.xlabel("Destination")
        plt.ylabel("Count")
        plt.title("Arrival Count by Destination")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()

    def get_csv_file(self):
        return self._csv_file

    def set_csv_file(self, csv_file):
        self._csv_file = csv_file

arrival_times = ArrivalTimes(csv_file)
arrival_times.fetch_arrival_times()

print(json.dumps(arrival_times.arrival_times, indent=4))

arrival_times.save_to_csv()

arrival_times.display_arrival_stats()


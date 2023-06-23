import urllib.request
import json
import csv
import matplotlib.pyplot as plt

class ArrivalTimes:
    def __init__(self,infile):
        self.infile = infile
        self.arrival_times = []

    def fetch_arrival_times(self):
        with urllib.request.urlopen(self.infile) as response:
            arrival_times_json = response.read().decode()
            self.arrival_times = json.loads(arrival_times_json)

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.arrival_times[0].keys())
            for arrival in self.arrival_times:
                writer.writerow(arrival.values())
        print("File saved successfully.")

    def display_arrival_stats(self):
        destinations = [arrival["destinationName"] for arrival in self.arrival_times]
        destination_counts = {destination: destinations.count(destination) for destination in set(destinations)}
        destinations = list(destination_counts.keys())
        counts = list(destination_counts.values())

        plt.bar(destinations, counts)
        plt.xlabel("Destination")
        plt.ylabel("Count")
        plt.title("Arrival Count by Destination")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()

infile = 'https://api.tfl.gov.uk/StopPoint/490005624S/arrivals'

arrival_times = ArrivalTimes(infile)
arrival_times.fetch_arrival_times()

print(json.dumps(arrival_times.arrival_times, indent=4))

csv_filename = "arrival_times.csv"
arrival_times.save_to_csv(csv_filename)

arrival_times.display_arrival_stats()



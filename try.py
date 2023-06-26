import urllib.request
import json
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

csv_file = 'bus-timetable.csv'

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
            print(f"Response from API: {self.arrival_times}")
            writer.writerow(self.arrival_times[0].keys())
            for arrival in self.arrival_times:
                writer.writerow(arrival.values())
        print("File saved successfully.")

    def display_arrival_stats(self):
        if not self.arrival_times:
            print("No arrival times available.")
            return

        print("Bus Information:")
        countdowns = []
        for arrival in self.arrival_times:
            line_name = arrival["lineName"]
            destination_name = arrival["destinationName"]
            expected_arrival = datetime.fromisoformat(arrival["expectedArrival"].replace("Z", "+00:00"))
            countdown = expected_arrival - datetime.now(timezone.utc)
            countdown_minutes = int(countdown.total_seconds() // 60)
            countdowns.append(countdown_minutes)
            print(f"Line: {line_name}")
            print(f"Destination: {destination_name}")
            print(f"Expected Arrival: {expected_arrival.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Countdown: {countdown_minutes} minutes")
            print("-" * 30)

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

        for i, count in enumerate(counts):
            countdown_text = f"{countdowns[i]} min"
            plt.text(destinations[i], count, countdown_text, ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

        min_countdown = min(countdowns)
        if min_countdown > 0:
            next_bus = datetime.now() + timedelta(minutes=min_countdown)
            print(f"The next bus is arriving in {min_countdown} minutes at {next_bus.strftime('%H:%M')}.")

    def get_csv_file(self):
        return self._csv_file

    def set_csv_file(self, csv_file):
        self._csv_file = csv_file


arrival_times = ArrivalTimes(csv_file)
arrival_times.fetch_arrival_times()

print(json.dumps(arrival_times.arrival_times, indent=4))

arrival_times.save_to_csv()

arrival_times.display_arrival_stats()

import urllib.request
import json
import matplotlib.pyplot as plt
from datetime import datetime

class ArrivalTimes:
    def __init__(self):
        self._stop_point_id = ""
        self.arrival_times = []

    def fetch_arrival_times(self):
        url = f"https://api.tfl.gov.uk/StopPoint/{self._stop_point_id}/Arrivals"
        try:
            with urllib.request.urlopen(url) as response:
                arrival_times_json = response.read().decode()
                self.arrival_times = json.loads(arrival_times_json)
        except urllib.error.URLError as e:
            print(f"Failed to fetch arrival times: {e}")

    def display_arrival_times(self):
        if not self.arrival_times:
            print("No arrival times available.")
            return

        print("Arrival Times:")
        next_train_time = None
        for arrival in self.arrival_times:
            line_name = arrival["lineName"]
            destination_name = arrival["destinationName"]
            expected_arrival = datetime.strptime(arrival["expectedArrival"], "%Y-%m-%dT%H:%M:%SZ")
            print(f"Line: {line_name}")
            print(f"Destination: {destination_name}")
            print(f"Expected Arrival: {expected_arrival}")
            print("-" * 30)

            # Check if this train is the next one
            now = datetime.now()
            if expected_arrival > now and (next_train_time is None or expected_arrival < next_train_time):
                next_train_time = expected_arrival

        if next_train_time:
            countdown = next_train_time - datetime.now()
            minutes = int(countdown.total_seconds() // 60)
            seconds = int(countdown.total_seconds() % 60)
            print(f"Next Train in: {minutes} minutes and {seconds} seconds")
        else:
            print("No upcoming trains.")

    def plot_arrival_times(self):
        if not self.arrival_times:
            print("No arrival times available.")
            return

        destinations = [arrival["destinationName"] for arrival in self.arrival_times]
        counts = [destinations.count(destination) for destination in set(destinations)]
        destinations = list(set(destinations))

        plt.bar(destinations, counts)
        plt.xlabel("Destination")
        plt.ylabel("Count")
        plt.title("Arrival Times by Destination")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def get_stop_point_id(self):
        return self._stop_point_id

    def set_stop_point_id(self, stop_point_id):
        self._stop_point_id = stop_point_id


arrival_times = ArrivalTimes()
arrival_times.set_stop_point_id("940GZZLUHBN")
arrival_times.fetch_arrival_times()
arrival_times.display_arrival_times()
arrival_times.plot_arrival_times()

import urllib.request
import json
import matplotlib.pyplot as plt

class ArrivalTimes:
    def __init__(self):
        self._stop_point_id = ""
        self.arrival_times = []

    def fetch_arrival_times(self):
        infile = (f"https://api.tfl.gov.uk/StopPoint/{self._stop_point_id}/Arrivals")
        try:
            with urllib.request.urlopen(infile) as response:
                arrival_times_json = response.read().decode()
                self.arrival_times = json.loads(arrival_times_json)
        except urllib.error.URLError as e:
            print(f"Failed to fetch arrival times: {e}")

    def display_arrival_times(self):
        if not self.arrival_times:
            print("No arrival times available.")
            return

        print("Arrival Times:")
        for arrival in self.arrival_times:
            line_name = arrival["lineName"]
            destination_name = arrival["destinationName"]
            expected_arrival = arrival["expectedArrival"]
            print(f"Line: {line_name}")
            print(f"Destination: {destination_name}")
            print(f"Expected Arrival: {expected_arrival}")
            print("-" * 30)

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

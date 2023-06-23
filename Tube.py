import urllib.request
import json

class TubeStatus:
    def __init__(self, api_url):
        self.api_url = api_url
        self.status_data = []

    def fetch_status(self):
        with urllib.request.urlopen(self.api_url) as response:
            status_json = response.read().decode()
            self.status_data = json.loads(status_json)

    def display_status(self):
        for line in self.status_data:
            line_name = line['name']
            line_status = line['lineStatuses'][0]['statusSeverityDescription']
            print(f"{line_name}: {line_status}")


api_url = 'https://api.tfl.gov.uk/line/mode/tube/status'

tube_status = TubeStatus(api_url)
tube_status.fetch_status()

tube_status.display_status()


"""created to track exercize data"""

from datetime import date, timedelta
import json

class WorkoutTracker:
    """
    Tracks the days the user has exersized
    :self.data: dict with a key in isoformat date and a boolean value
    """
    def __init__(self, filename: str = 'data.json'):
        self.data = {}
        self.filename = filename

    def new_data(self):
        """Create an empty datasheet for the year 2021"""
        current_date = date(2021, 1, 1)
        one_day = timedelta(1)
        while current_date.year != 2022:
            self.data[current_date.isoformat()] = False
            current_date += one_day

    def save_data(self, filename: str = None):
        """write data to the file name saved under self.filename"""
        if filename == None:
            filename = self.filename
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def get_data(self, filename: str = None):
        """get data from the file name saved under self.filename"""
        if filename == None:
            filename = self.filename
        with open(self.filename, 'r') as f:
            self.data = json.load(f)

    def toggle_day(self, day: str):
        """toggle the boolean value of a day"""
        self.data[day] = not self.data[day]

    def print_data(self):
        """Show the data"""
        for key, value in self.data.items():
            print(f'\t{key}: {value},')

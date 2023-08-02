from google_calendar import GoogleCalendar
from tufts_dining import TuftsDining
from datetime import datetime

import re 

def main():
    date = datetime.today().strftime("%Y-%m-%d")
    dining = TuftsDining()
    calendar = GoogleCalendar()
    locations = [0,1]

    for index in locations:
        text = dining.get_data(index, date) 
        if text: 
            location = dining.LOCATIONS[index]
            summary = f"{location[0].split()[0]} Menu"
            event = calendar.create_event(summary=summary, description=text, date=date)
            calendar.insert_event(event)
        else:
            print(f"Not creating event because is not serving food :(")

if __name__ == '__main__':
    main()